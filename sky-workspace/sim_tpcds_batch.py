
from sky_controller.controller import Controller

test_setup_yaml = "./sky-config/db_cache_sim/setup.yml"
test_task_yaml = "./sky-config/db_cache_sim/run_tpcds.yml"

def test_controller():

    query_list = range(1, 100)

    env_list = [{"QUERY_NAME": i, "SCALE": 1, "RNGSEED": 0, "CSV_SUFFIX": "n2-standard-16"} for i in query_list]

    num_managers = 20
    num_clusters = 20
    polling_interval = 120

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

