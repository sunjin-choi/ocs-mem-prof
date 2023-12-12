

from sky_controller.controller import Controller

test_setup_yaml = "./sky-config/db_cache_sim/setup.yml"
test_task_yaml = "./sky-config/db_cache_sim/run_prim.yml"

def test_controller():

    query_names = [
        "single-column_aggregation_group_by",
        "equijoin",
        "range_scan",
        "cross_join",
        "distinct",
        "full_scan",
        "sort_order_by",
    ]
    # tbl_sizes = [1000, 2500, 5000, 10000]
    tbl_sizes = [1000, 10000]
    # modes = lambda tbl_size: f"ubmark_{tbl_size}"

    # env_list = [{"QUERY_NAME": i, "SCALE": 1, "RNGSEED": 0, "CSV_SUFFIX": "n2-standard-16"} for i in query_list]
    env_list = [{"QUERY_NAME": i, "SCALE": 1, "RNGSEED": 0, "CSV_SUFFIX": "n2-standard-16", "DATA_SUFFIX": "_1_4",
                 "TBL_SIZE": j, "NUM_SAMPLES": "1000000"} for i in query_names for j in tbl_sizes]

    num_managers = 7
    num_clusters = num_managers
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

