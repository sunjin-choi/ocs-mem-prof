
from sky_controller.controller import Controller

test_setup_yaml = "./sky_controller/test_configs/setup-cpu.yml"
test_task_yaml = "./sky_controller/test_configs/setup-cpu.yml"

def test_controller():

    env_list = [{"MSG": i} for i in range(6)]

    num_managers = 2
    num_clusters = 4
    polling_interval = 20

    controller = Controller.from_yaml_file_and_env_list(
            setup_yaml_file = test_setup_yaml,
            task_yaml_file = test_task_yaml,
            env_list = env_list,
            num_managers = num_managers,
            num_clusters = num_clusters,
            polling_interval = polling_interval,
            reuse_clusters=True,
            )

    controller.run()

if __name__ == "__main__":
    test_controller()

