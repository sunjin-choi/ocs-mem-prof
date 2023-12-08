import sky
from dataclasses import dataclass
import threading
import yaml
from enum import Enum


def _dict_to_str(d):
    return "__".join(f"{k}_{v}" for k, v in d.items())


class JobType(Enum):
    SETUP = 0
    EXEC = 1


@dataclass
class Job:
    """Job class
    Described with name and environment variables
    """

    name: str
    task: sky.Task
    job_type: JobType
    env_override: dict

    def __post_init__(self):
        """Override environment variables"""
        if self.env_override is not {}:
            self.task.update_envs(self.env_override)

    @classmethod
    def from_yaml(cls, yaml_file, job_type):
        """Create a Job from a yaml file with environment variables override"""
        task = sky.Task.from_yaml(yaml_file)
        job_name = f"{task.name}"
        return cls(name=job_name, task=task, job_type=job_type, env_override={})

    @classmethod
    def from_yaml_with_envs_override(cls, yaml_file, job_type, env_override):
        """Create a Job from a yaml file with environment variables override"""
        task = sky.Task.from_yaml(yaml_file)
        job_name = (
            f"{task.name}_{_dict_to_str(env_override)}" if env_override else task.name
        )
        return cls(
            name=job_name, task=task, job_type=job_type, env_override=env_override
        )
