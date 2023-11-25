import json
import argparse

# import parser

class Patient:
    def __init__(self,name,start,duration):
        self.name=name
        self.start=start
        self.duration = duration

    def to_ob(self):
        return {
            'name' : self.name,
            'start' : self.start,
            'duration' : self.duration
        }
    
    @classmethod
    def from_ob(cls, data):
        return cls(name=data['name'], start=data['start'], duration=data['duration'])
    
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Process three parameters from the command line.')

    parser.add_argument('--param1', type=str, help='Name')
    parser.add_argument('--param2', type=str, help='Start Time')
    parser.add_argument('--param3', type=str, help='End Time')

    args = parser.parse_args()

    # Access the values of the parameters
    param1_value = args.param1
    param2_value = args.param2
    param3_value = args.param3

    p = Patient(param1_value,param2_value,param3_value)

    dt=read_json_file("../data/appointments.json")
    newData = p.to_ob()

    dt.update(newData)
    write_json_file("../data/appointments.json", dt)


if __name__=="__main__":
    main()
