from typing import Dict, List
import sky
from sky_controller.job import Job, JobType
from sky_controller.job_pool import JobPool
from sky_controller.cluster_manager import ClusterManager, ClusterManagerStatus
import signal
import threading
import time
import multiprocessing

# For multiprocessing
def add_job_to_pool(job_pool, task_yaml_file, env):
    job = Job.from_yaml_with_envs_override(task_yaml_file, JobType.EXEC, env)
    job_pool.add_job(job)

class Controller:
    def __init__(
        self,
        job_setup: Job,
        job_pool: JobPool,
        num_managers: int,
        num_clusters: int,
        polling_interval: int,
        reuse_clusters: bool = False,
    ):
        self.job_setup = job_setup
        self.job_pool = job_pool
        self.polling_interval = polling_interval

        self.cluster_managers = []
        self.manager_status = {}

        # num clusters should be greater than or equal to num managers
        # and also divisible by num managers
        if num_clusters < num_managers:
            raise ValueError(
                "Number of clusters cannot be greater than number of managers."
            )
        if num_clusters % num_managers != 0:
            raise ValueError(
                "Number of clusters must be divisible by number of managers."
            )

        clusters_per_manager = num_clusters // num_managers
        for i in range(num_managers):
            # Calculate the range of clusters for this manager
            start_idx = i * clusters_per_manager
            end_idx = start_idx + clusters_per_manager

            # Generate cluster names for this manager
            cluster_names = [
                f"{job_setup.name}-mgr-{i}-cluster-{j}"
                for j in range(start_idx, end_idx)
            ]

            mgr = ClusterManager(
                manager_id=i,
                controller=self,
                cluster_names=cluster_names,
                job_setup=job_setup,
                job_pool=job_pool,
                polling_interval=polling_interval,
                reuse_clusters=reuse_clusters,
            )
            self.add_cluster_manager(mgr)

        self.exit_event = threading.Event()
        signal.signal(signal.SIGINT, self._handle_sigint)

    @classmethod
    def from_yaml_file_and_env_list(
        cls,
        setup_yaml_file: str,
        task_yaml_file: str,
        env_list: List[Dict],
        num_managers: int,
        num_clusters: int,
        polling_interval: int,
        reuse_clusters: bool = False,
    ):
        job_setup = Job.from_yaml(setup_yaml_file, JobType.SETUP)

        job_pool = JobPool()
        # for env in env_list:
        #     job_pool.add_job(
        #         Job.from_yaml_with_envs_override(task_yaml_file, JobType.EXEC, env)
        #     )

        # Create a list of arguments for each job to be added
        args_list = [(job_pool, task_yaml_file, env) for env in env_list]

        # Create a pool of worker processes
        with multiprocessing.Pool() as pool:
            # Use pool.starmap to execute the add_job_to_pool function in parallel
            pool.starmap(add_job_to_pool, args_list)

        return cls(
            job_setup,
            job_pool,
            num_managers,
            num_clusters,
            polling_interval,
            reuse_clusters,
        )

    def run(self):
        """Run the controller."""
        self.start_all_managers()
        while not self.exit_event.is_set():
            if self._check_all_done():
                break
            time.sleep(30)  # Wait for a signal to exit

        self.abort()

    def _handle_sigint(self, signum, frame):
        """Handle Ctrl+C (SIGINT) signal."""
        print("Ctrl+C detected, stopping all managers and exiting.")
        self.abort()

    def add_cluster_manager(self, cluster_manager):
        self.cluster_managers.append(cluster_manager)
        self.manager_status[cluster_manager.id] = ClusterManagerStatus.RUNNING

    def start_all_managers(self):
        for manager in self.cluster_managers:
            manager.start()

    def stop_all_managers(self):
        for manager in self.cluster_managers:
            manager.stop()

    def abort(self):
        self.stop_all_managers()
        self.exit_event.set()

    """
    Subscriber methods
    """

    def signal_done(self, manager_id):
        self.manager_status[manager_id] = ClusterManagerStatus.DONE
        # self._check_all_done()

    def signal_abort(self, manager_id):
        self.manager_status[manager_id] = ClusterManagerStatus.ABORT
        print(f"Manager {manager_id} aborted. Stopping all managers and exiting.")
        self.abort()

    def _check_all_done(self):
        """Check if all managers are done."""
        # if all(
        #     status == ClusterManagerStatus.DONE
        #     for status in self.manager_status.values()
        # ):
        #     print("All managers are done. Exiting.")
        #     self.abort()

        return all(
            status == ClusterManagerStatus.DONE
            for status in self.manager_status.values()
        )


# # Example usage
# controller = Controller()
# controller.add_cluster_manager(ClusterManager(1, ["cluster-1"], controller.job_pool, controller, {}))
# # Add more managers as needed
# controller.run()
