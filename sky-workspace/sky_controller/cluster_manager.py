from enum import Enum
import threading
import time
from typing import List
import sky
from sky_controller.job import JobType
from sky_controller.job import Job
from sky_controller.job_pool import JobPool


class ClusterManagerStatus(Enum):
    RUNNING = 0
    DONE = 1
    ABORT = 2


class ClusterManager:
    def __init__(
        self,
        manager_id: int,
        controller,
        cluster_names: List[str],
        job_setup: Job,
        job_pool: JobPool,
        polling_interval: int,
        reuse_clusters: bool = False,
    ):
        self.id = manager_id
        self.cluster_names = cluster_names
        self.job_pool = job_pool
        self.job_setup = job_setup
        self.controller = controller
        self.polling_interval = polling_interval
        self.reuse_clusters = reuse_clusters
        self._stop_event = threading.Event()

        self.thread = threading.Thread(target=self._schedule_job_fifo, daemon=True)

    def start(self):
        """Start the watchdog thread."""
        self.thread.start()

    def stop(self):
        """Stop the watchdog thread."""
        self._stop_event.set()
        self.thread.join()

    def _schedule_job_fifo(self):
        """Poll the cluster status periodically."""
        # if not self.reuse_clusters:
        for cluster_name in self.cluster_names:
            self._launch_cluster(cluster_name)

        while not self._stop_event.is_set():
            try:
                for cluster_name in self.cluster_names:
                    # get latest job info
                    (job_status,) = sky.job_status(
                        cluster_name=cluster_name, job_ids=None, stream_logs=False
                    ).values()

                    job_succeeded = str(job_status) == "JobStatus.SUCCEEDED"
                    job_running = str(job_status) == "JobStatus.RUNNING"
                    job_failed = str(job_status) == "JobStatus.FAILED"

                    # if job status is empty and job pool is not empty, pipe a job to the cluster
                    cluster_wait_jobs_incomplete = (
                        job_succeeded and not self.job_pool.is_empty()
                    )
                    # if job status is not empty, move to the next cluster
                    cluster_running = job_running
                    # if job status is empty and job pool is empty, break and signal controller to stop
                    cluster_done = job_succeeded and self.job_pool.is_empty()

                    if self._stop_event.is_set():
                        break

                    # print how many jobs left in the pool
                    print(f"{len(self.job_pool.jobs)} jobs left in the pool.")

                    if cluster_wait_jobs_incomplete:
                        print(f"Piping a job to cluster {cluster_name}.")
                        self._pipe_job_to_cluster(
                            cluster_name, self.job_pool.get_next_job()
                        )
                    elif cluster_running:
                        print(f"Cluster {cluster_name} is running.")
                        continue
                    elif cluster_done:
                        print(f"Cluster {cluster_name} is done.")
                        self.controller.signal_done(self.id)
                        # self._stop_event.set()
                        # break
                        return
                    elif job_failed:
                        print(f"Job failed.")
                        self.controller.signal_abort(self.id)
                        # self._stop_event.set()
                        # break
                        return

            except ValueError as e:
                print(f"Cluster not found: {e}")
                self.controller.signal_abort(self.id)
                self.stop()
            except sky.exceptions.ClusterNotUpError as e:
                self._launch_cluster(cluster_name, self.setup_info)
            except Exception as e:
                print(f"Error polling cluster status: {e}")
                self.controller.signal_abort(self.id)
                self.stop()

            time.sleep(self.polling_interval)

    def _pipe_job_to_cluster(self, cluster_name: str, job: Job):
        """Pipe a job to a cluster."""
        if job.job_type == JobType.EXEC:
            sky.exec(
                task=job.task,
                cluster_name=cluster_name,
                dryrun=False,
                down=False,
                stream_logs=False,
                backend=None,
                detach_run=True,
            )
            print(f"Piped job {job.name} to cluster {cluster_name}.")
        else:
            # skip if job is a setup job
            pass

    def _launch_cluster(self, cluster_name: str):
        if self.job_setup.job_type == JobType.SETUP:
            sky.launch(
                task=self.job_setup.task,
                cluster_name=cluster_name,
                idle_minutes_to_autostop=5,
                down=True,
                stream_logs=False,
                detach_setup=True,
                detach_run=True,
            )
        else:
            self.stop()
            raise ValueError("Job setup is not a setup job.")
