from calc_work_hours.controller import CalculateWorkHours
from calc_work_hours.json_utils import read_json_file, validate_json_file

""" function which user needs to use to get the working hours intervals in human readable format"""


def calculate_working_hours(json_file_path):
    data = read_json_file(file_path=json_file_path)
    isValidated = validate_json_file(Json_file_object=data)

    if isValidated:
        calc_hours_work = CalculateWorkHours(json_data=data)
        calc_hours_work.refactor_input_json_with_correct_data()
        formatted_output = calc_hours_work.working_hours_in_human_readable_format()

        return formatted_output
