import json

READ_JSON_PATH = r"C:\census-automaps\scripts\config\popgroup.json"
WRITE_JSON_PATH = r"C:\census-automaps\scripts\config\name_id_mapping2.json"
FILTER_STRING = "alone or in any combination"


def read_json_data():
    read_json_data = None
    with open(READ_JSON_PATH, encoding="utf-8") as read_json_file:
        read_json_data = json.load(read_json_file)

    return read_json_data


def parse_ancestries(mapping, json_data):
    ancestries = json_data["values"]["item"]
    for ancestry_id in ancestries:
        ancestry = ancestries[ancestry_id]
        try:
            int_ancestry_id = int(ancestry_id)
            if FILTER_STRING in ancestry or (
                int_ancestry_id > 4014 and int_ancestry_id < 4051
            ):
                # print(ancestry)
                ancestry_short = ancestry.replace(" alone or in any combination", "")
                print(ancestry_short)
                mapping[ancestry] = ancestry_id
        except ValueError:
            if FILTER_STRING in ancestry:
                # print(ancestry)
                ancestry_short = ancestry.replace(" alone or in any combination", "")
                print(ancestry_short)
                mapping[ancestry] = ancestry_id


def write_json_data(mapping):
    with open(WRITE_JSON_PATH, "w", encoding="utf-8") as write_json_file:
        json.dump(mapping, write_json_file, indent=4)


def generate_mapping():
    mapping = {}
    json_data = read_json_data()
    parse_ancestries(mapping, json_data)
    write_json_data(mapping)


if __name__ == "__main__":
    generate_mapping()
