import json

JSON_PATH = r"C:\census-automaps\scripts\name_id_mapping.json"


# return code for group name
# TODO error handling
# TODO mappings: https://api.census.gov/data/2020/dec/ddhca/variables/POPGROUP.json
def get_mapping(group_name):
    with open(JSON_PATH, encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data[group_name]
