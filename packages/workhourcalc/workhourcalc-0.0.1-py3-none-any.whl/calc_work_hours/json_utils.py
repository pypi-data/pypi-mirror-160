import json
import sys

from jsonschema import validate
import jsonschema

from calc_work_hours import TYPES, EVENT_CLOSE, EVENT_OPEN, DAYS
from calc_work_hours.schema import main_json_schema_structure

""" read the json file from the file path. and also this validates the json file. if its not in json format then
    it will be raise an exception"""


def read_json_file(file_path):
    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
            """ sort the json values from time"""
            for key, value in data.items():
                data[key] = sorted(value, key=lambda i: i['value'])

            return data
    except ValueError as err:
        raise Exception(err)


""" validate the extracted json object in here.
    1. validate the json object using predefined schema
    2. validate the json object with the custom validation according to the requirement"""


def validate_json_file(Json_file_object):
    """validate the json structure using predefined schema"""
    try:
        validate(instance=Json_file_object, schema=main_json_schema_structure)
    except jsonschema.exceptions.ValidationError as err:
        raise Exception("Invalid json format found in json file - " + str(err))

    """validate the nested json data with custom validation rules"""
    try:
        """validated json data with below scenarios.
            1. week cannot start with close event
            2. week cannot end with open event
            3. start and end of the events cannot be same"""

        input_json_nested_data_list = [value for key, value in Json_file_object.items() if len(value) > 0]

        for event_items in input_json_nested_data_list:
            event_items = sorted(event_items, key=lambda i: i['value'])

            err_data_list = [event['type'] for event in event_items if event['type'] not in TYPES]
            if len(err_data_list) > 0:
                raise Exception("Invalid event type found in json file.")

        start_day_list = [event['type'] for event in input_json_nested_data_list[0] if event['type'] in TYPES]
        week_start_event = str(start_day_list[0])
        end_day_list = [event['type'] for event in input_json_nested_data_list[-1] if event['type'] in TYPES]
        week_end_event = str(end_day_list[-1])

        if week_start_event == EVENT_CLOSE or week_end_event == EVENT_OPEN:
            raise Exception("Invalid event type found in starting/ending of the week in json file.")
        if week_start_event == week_end_event:
            raise Exception("Start and end a week with events of distinct types. check the json file")

    except Exception as err:
        print(sys.exc_info())
        raise Exception(err)

    return True
