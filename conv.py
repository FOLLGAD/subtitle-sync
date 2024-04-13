import json, sys, ast

input_lines = sys.stdin.readlines()
data = "".join(input_lines)
data = ast.literal_eval(data)

# Convert tuples into arrays
for chunk in data['chunks']:
    chunk['timestamp'] = list(chunk['timestamp'])

# Displaying the converted JSON
data_json = json.dumps(data, ensure_ascii=False, indent=2)
print(data_json)
