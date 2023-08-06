import modify_input_json

input_file_path = './c1algo1/data/input/randomized_professors.json'
header = 'professors'
output_file_path = './c1algo1/data/input/sample_input.json'

modify_input_json.set_input(input_file_path, header, output_file_path)