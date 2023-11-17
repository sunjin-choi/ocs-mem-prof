import argparse
import os
import tempfile
from ruamel.yaml import YAML
from multiprocessing import Process
from pathlib import Path


# # Function to run the sky launch command
# def run_command(new_instance_type, temp_config_path):
#     os.system(f'sky launch -c sunjin-tpcds-{new_instance_type} {temp_config_path} -i 5 -y -d')

def create_new_yaml(config_path, new_instance_type, output_dir):
    # Load the YAML file
    yaml = YAML()
    with open(config_path, 'r') as file:
        config = yaml.load(file)

    # Modify the instance_type
    config['resources']['instance_type'] = new_instance_type

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write to a real file in the specified output directory
    # add new_instance_type as suffix to the file name before extension using Path
    output_file_path = Path(output_dir) / f"{Path(config_path).stem}-{new_instance_type}{Path(config_path).suffix}"
    # output_file_path = os.path.join(output_dir, os.path.basename(config_path) + f'-{new_instance_type}')

    with open(output_file_path, 'w') as file:
        yaml.dump(config, file)

    return output_file_path

def main():
    parser = argparse.ArgumentParser(description='Batch sky launch with different instance types.')
    parser.add_argument('config_path', type=str, help='Path to the YAML configuration file.')
    parser.add_argument('instance_types_path', type=str, help='Path to the file containing instance types.')
    args = parser.parse_args()

    # Read instance types from the file
    with open(args.instance_types_path, 'r') as file:
        instance_types = [line.strip() for line in file.readlines() if line.strip()]

    # create a new yaml in the same directory as config_path
    output_dir = os.path.dirname(args.config_path)
    for instance_type in instance_types:
        create_new_yaml(args.config_path, instance_type, output_dir)

    # # Create and start a separate process for each instance type
    # processes = []
    # for instance_type in instance_types:
    #     config_path = modify_yaml_and_launch(args.config_path, instance_type, "generated")
    #     process = Process(target=run_command, args=(instance_type,config_path,))
    #     process.start()
    #     processes.append(process)
    #
    # # Wait for all processes to complete
    # for process in processes:
    #     process.join()

if __name__ == '__main__':
    main()
