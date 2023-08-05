from .arg_parser import parse_arguments
import os


def command_generator(account_feature_groups: list) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param account_feature_groups:
    :return:
    """
    # get arguments
    known_args, unknown_args = parse_arguments()

    if type(account_feature_groups[0]) is int:
        process_name = account_feature_groups[0]
    else:
        # get data for constructing behave command (this is messy, but it works)
        process_name = account_feature_groups[0][0]

    # construct the behave command
    results_json_file = os.path.join(known_args.output, f'{process_name}.json')
    user_defined_args = ' '.join('-D {}'.format(arg[0]) for arg in known_args.D) if known_args.D else ''
    unknown_args_formatted = ' '.join(arg for arg in unknown_args)
    tags_formatted = ' '.join('--tags="@{}" '.format(t[0].replace("@", "")) for t in known_args.tags)
    scenarios_formatted = ' '.join(scenario for scenario in account_feature_groups[1])

    command = f'behave {user_defined_args} {unknown_args_formatted} {tags_formatted} {scenarios_formatted}'

    print(command, end='\n\n')
    # r = call(cmd, shell=True)
    return results_json_file
