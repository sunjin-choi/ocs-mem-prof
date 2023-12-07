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
    ):
        self.id = manager_id
        self.cluster_names = cluster_names
        self.job_pool = job_pool
        self.job_setup = job_setup
        self.controller = controller
        self.polling_interval = polling_interval
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._schedule_job_fifo, daemon=True)

    def start(self):
        """Start the watchdog thread."""
        self.thread.start()

        for cluster_name in self.cluster_names:
            self._launch_cluster(cluster_name)

    def stop(self):
        """Stop the watchdog thread."""
        self._stop_event.set()
        self.thread.join()

    def _schedule_job_fifo(self):
        """Poll the cluster status periodically."""
        while not self._stop_event.is_set():
            try:
                for cluster_name in self.cluster_names:
                    # poll job status
                    job_status = sky.job_status(
                        cluster_name=cluster_name, job_ids=None, stream_logs=False
                    )

                    # if job status is empty and job pool is not empty, pipe a job to the cluster
                    cluster_wait_jobs_incomplete = (
                        job_status == {None: None} and not self.job_pool.is_empty()
                    )
                    # if job status is not empty, move to the next cluster
                    cluster_running = job_status != {None: None}
                    # if job status is empty and job pool is empty, break and signal controller to stop
                    all_jobs_complete = (
                        job_status == {None: None} and self.job_pool.is_empty()
                    )

                    if cluster_wait_jobs_incomplete:
                        self._pipe_job_to_cluster(
                            cluster_name, self.job_pool.get_next_job()
                        )
                    elif cluster_running:
                        continue
                    elif all_jobs_complete:
                        self.controller.signal_done(self.id)
                        self._stop_event.set()
                        break

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
                dry_run=False,
                down=False,
                stream_logs=False,
                backend=None,
                detach_run=True,
            )
        else:
            # skip if job is a setup job
            pass

    def _launch_cluster(self, cluster_name: str):
        if self.job_setup.job_type == JobType.SETUP:
            sky.launch(
                task=self.job_setup.task,
                cluster_name=cluster_name,
                stream_logs=False,
                detach_setup=True,
                detach_run=True,
            )
        else:
            self.stop()
            raise ValueError("Job setup is not a setup job.")
