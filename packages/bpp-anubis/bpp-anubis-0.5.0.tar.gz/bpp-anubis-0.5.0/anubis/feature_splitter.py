import glob
import subprocess
from random import shuffle


def get_test_paths(unit, feature_dir, processes, accounts=None):
    paths = __get_paths(feature_dir, unit)
    result = __get_path_groups(paths, processes, accounts)
    return result


def __get_path_groups(paths, num_split, accounts=None, section=None):
    # split as evenly as possible
    inc = -(-len(paths) // num_split)

    # group the paths
    path_groups = [paths[i:i + inc] for i in range(0, len(paths), inc)]
    shuffle(path_groups)

    if accounts:
        return list(zip(accounts, path_groups))

    return list(zip(list(range(len(path_groups))), path_groups))


def __get_paths(feature_dir, unit):
    feature_paths = glob.glob(f'{feature_dir}/**/*.feature', recursive=True)

    if unit.lower() == 'scenario':
        scenario_paths = subprocess.run(
            [f'grep -irn "Scenario.*:" {" ".join(feature_paths)} | sed s/": .*"/""/'],
            shell=True,
            capture_output=True
        ).stdout.replace(b'\n', b' ').decode('utf-8').split()
        return scenario_paths

    return feature_paths
