import sys

from calc_work_hours import DAYS
from calc_work_hours.schema import result_schema
from calc_work_hours.utils import format_time, format_time_range, format_output

"""" implement calculate work hours in here. first refactor the code and setup the json with correct events.
    then implement the working hours interval with human readable format"""


class CalculateWorkHours:
    """ create the init method for the class
    """

    def __init__(self, json_data):
        self.refactored_schema = None
        self.data = json_data

    """
    refactor the json object according to the below rules.
    1. if sequence of opening/closing time are not matched(for example, two sequence closing events) 
    then raise an exception
    2. sort event values
    3.if opening time is in the specified day(let's say Monday) and the related closing event in the next day(Tuesday) 
    then the closing event must be moved to the previous day(Monday)"""

    def refactor_input_json_with_correct_data(self):
        try:

            validated_json_data = self.data

            """ iterate with DAYS and refactor the json object"""
            for day in DAYS:
                if len(validated_json_data[day]) == 0:
                    result_schema[day] = []
                else:

                    previous_type = None

                    """ sort the validated json object"""
                    unsorted_list = validated_json_data[day]
                    sorted_events_list = sorted(unsorted_list, key=lambda i: i['value'])

                    for event in sorted_events_list:
                        if sorted_events_list.index(event) == 0:
                            if event['type'] == 'open':
                                previous_type = event['type']
                                result_schema[day].append(event)
                            else:
                                """ sort the validated json object"""
                                previous_day_data = validated_json_data[DAYS[DAYS.index(day) - 1]]
                                previous_day_data = sorted(previous_day_data, key=lambda i: i['value'])
                                previous_day_last_event = previous_day_data[- 1]

                                if previous_day_last_event["type"] == event['type']:
                                    raise Exception(f'Cannot have two consecutive "{event["type"]}" times.')
                                else:
                                    previous_type = event['type']
                                    result_schema[DAYS[DAYS.index(day) - 1]].append(event)
                        else:
                            if previous_type == event['type']:
                                raise Exception(f'Cannot have two consecutive "{event["type"]}" times.')
                            else:
                                previous_type = event['type']
                                result_schema[day].append(event)

            self.refactored_schema = result_schema

            return result_schema
        except Exception as error:
            print(sys.exc_info())
            raise Exception(error)

    """
        format the refactored data in human readable format using below util functions
        format_time,format_time_range,format_output
        """

    def working_hours_in_human_readable_format(self):
        try:
            refactored_data = self.refactored_schema

            work_hours_dict = dict()

            for day, events in refactored_data.items():
                opening_time = None
                formatted_times_list = []
                for event in events:

                    if event['type'] == 'open':
                        opening_time = format_time(event['value'])
                    else:
                        closing_time = format_time(event['value'])

                        formatted_time = format_time_range(opening_time, closing_time)
                        formatted_times_list.append(formatted_time)

                work_hours_dict[day] = formatted_times_list

            formatted_output = format_output(work_hours_dict)

            return formatted_output

        except Exception as error:
            print(sys.exc_info())
            raise Exception(error)
