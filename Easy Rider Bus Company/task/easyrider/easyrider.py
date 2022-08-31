import json
from collections import defaultdict


class OpenJSon:
    error_result_dict = {}

    def __init__(self, input_json):
        self.input = input_json

    # check if a line has one start and one end stop
    def check_start_stop(self):

        bus_id = [i['bus_id'] for i in json.loads(self.input)]
        stop_type = [i['stop_type'] for i in json.loads(self.input)]

        dict_of_lines = defaultdict(set)

        for bus_id_item, stop_type_item in zip(bus_id, stop_type):
            dict_of_lines[bus_id_item].update(stop_type_item)

        switcher = True
        for key, value in dict_of_lines.items():
            if 'S' in value and 'F' in value:
                continue
            else:
                switcher = False
                print(f'There is no start or end stop for the line: {key}.')
                break

        if switcher:
            start_stops, transfer_stops, finish_stops, stops_on_demand = self.count_stops_type()

            print('On demand stops test:')
            wrong_stop_type = list()
            for stop in stops_on_demand:
                if (stop in start_stops) or (stop in transfer_stops) or (stop in finish_stops):
                    wrong_stop_type.append(stop)
                else:
                    continue

            if wrong_stop_type:
                print(f'Wrong stop type: {sorted(wrong_stop_type)}')
            else:
                print('OK')

    def count_stops_type(self):
        start_stops = list()
        transfer_stops = list()
        finish_stops = list()
        stops_on_demand = list()
        all_stops = [line['stop_name'] for line in json.loads(self.input)]

        freq_dict = {}
        for stop in all_stops:
            # set the default value to 0
            freq_dict.setdefault(stop, 0)
            # increment the value by 1
            freq_dict[stop] += 1

        for stop, freq in freq_dict.items():
            if freq > 1:
                transfer_stops.append(stop)

        for line in json.loads(self.input):
            if line['stop_type'] == 'S' and line['stop_name'] not in start_stops:
                start_stops.append(line['stop_name'])
            elif line['stop_type'] == 'F' and line['stop_name'] not in finish_stops:
                finish_stops.append(line['stop_name'])
            elif line['stop_type'] == 'O' and line['stop_name'] not in stops_on_demand:
                stops_on_demand.append(line['stop_name'])

        return start_stops, transfer_stops, finish_stops, stops_on_demand


if __name__ == '__main__':
    file1 = OpenJSon(input())
    file1.check_start_stop()
