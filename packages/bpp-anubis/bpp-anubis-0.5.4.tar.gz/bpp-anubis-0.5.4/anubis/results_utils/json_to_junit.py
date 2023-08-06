import json
from pathlib import Path
from datetime import datetime


def convert_json_to_junit(json_file_path: Path, junit_path: Path):
    with open(json_file_path) as f:
        json_results = json.load(f)

    statuses = [el['status'] for feature in json_results for el in feature['elements'] if el['type'] != 'background']
    passed = statuses.count('passed')
    failed = statuses.count('failed')
    total = passed + failed

    with open(junit_path, 'w+') as f:
        now = datetime.now()

        element_data = []
        total_time = 0
        for feature in json_results:
            for element in feature['elements']:
                element_junit_string = ''
                if element['type'] != 'background':
                    el_name = element['name'].replace('"', '&quot;')
                    el_status = element['status']
                    el_duration = 0
                    el_steps = ''
                    el_error = ''
                    el_tags = ' '.join(['@' + tag for tag in element['tags']])

                    for step in element['steps']:
                        el_duration += step['result']['duration'] if 'result' in step else 0
                        el_steps += '\t\t' + step['keyword'] + ' ' + step['name'] + '\n'

                        # print(step)
                        if 'result' in step and 'status' in step['result'] and step['result']['status'] == 'failed':
                            el_error += f'\t\t<error type="XXX">\n'
                            el_error += "".join(step["result"]["error_message"])\
                                .replace('&', '&amp;')\
                                .replace('<', '&lt;')\
                                .replace('>', '&gt;')\
                                .replace('”', '&quot;')\
                                .replace('‘', '&apos;')

                            el_error += '\n \t\t</error>\n'


                    system_out = (
                        f'\t\t<system-out>\n'
                        '\t\t\t<![CDATA[\n@scenario.begin\n\n' + '\t' + el_tags + '\n\t' + f'Scenario: {el_name}\n'
                        + el_steps + '\n\n@scenario.end\n'
                        '--------------------------------------------------------------------------------\n]]>\n'
                        '\t\t</system-out>\n'
                    )

                    element_junit_string += f'\t<testcase classname="{feature["name"]}" name="{el_name}" status="{el_status}" time="{el_duration}">\n'
                    element_junit_string += el_error
                    element_junit_string += system_out
                    element_junit_string += '\t</testcase>\n'

                    total_time += el_duration
                    element_data.append(element_junit_string)

        f.write(f'<testsuite name="Regression" tests="{total}" errors="{failed}" failures="{failed}" skipped="0" '
                f'time="{total_time}" timestamp="{now.isoformat()}" hostname="N/A">\n')
        for element in element_data:
            f.write(element)

        f.write('</testsuite>')
