from sky_controller.job import Job
import threading


class JobPool:
    def __init__(self):
        self.jobs = []
        self.lock = threading.RLock()

    def add_job(self, job):
        # with self.lock:
        self.jobs.append(job)

    def add_jobs(self, jobs):
        self.jobs += jobs

    def get_next_job(self):
        with self.lock:
            return self.jobs.pop(0) if self.jobs else None

    def has_jobs(self):
        with self.lock:
            return len(self.jobs) > 0

    def is_empty(self):
        with self.lock:
            return len(self.jobs) == 0
