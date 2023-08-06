import sys
import json
import requests

def get_api_data(url: str, datastream_id: int, token: str) -> tuple:
    params = {"datastream_id": datastream_id}
    headers = {"Authorization": "Token " + token}
    result = requests.get(url, params=params, headers=headers).json()
    return result, headers

def get_json_data(json_path: str) -> dict:
    with open(json_path) as file:
        json_list = json.load(file)
        return json_list

def normalize_string(string : str, special_chars) -> tuple:
    if string[0].isdigit():
        print(string)
        string = 'n'+string
    for char in special_chars:
        string = string.replace(char, "_")
    return string

def main(datastream_id: int, url: str, token: str, json_path: str, special_chars: str) -> None:
    json_list = get_json_data(json_path)
    json_list_original = json_list.copy()
    result, headers = get_api_data(url, datastream_id, token)
    not_found_api = []
    while True:
        for field in result["results"]:
            found = False
            for target_column in json_list[:]:
                if "adverity_name" in target_column:
                    name = target_column["adverity_name"]
                else:
                    name = target_column["name"]
                if name == field["name"]:
                    found = True
                    json_list.remove(target_column)
                    break
            if not found:
                not_found_api.append(field["name"])
        if result["next"] is None:
            break
        else:
           result = requests.get(result["next"], headers=headers).json()
    if len(json_list) > 0:
        not_found_json = []
        for column in json_list:
            not_found_json.append(column["name"])
        print("Could not find references in Adverity API for " + "\n".join(not_found_json))
    if len(not_found_api) > 0:
        print("Found references in Adverity API which are unmapped by the JSON file: " + "\n".join(not_found_api))
        for field in not_found_api:
            for entry in json_list_original:
                normal_field = normalize_string(field, special_chars)
                if normal_field == entry["name"]:
                    if "adverity_name" in entry:
                        sys.exit("Adverity name already present in " + entry["name"])
                    else:
                        entry["adverity_name"] = field
        json_out = json.dumps(json_list_original, indent=2)
        with open(json_path, "w") as outfile:
            outfile.write(json_out)
        outfile.close()
    


class Parser:
    def __init__(self, datastream_id: int, url: str, token: str, json_path: str, special_chars: str = ",().- %:!#&*§±+=") -> None:
        self.datastream_id = datastream_id
        self.url = url
        self.token = token
        self.json_path = json_path
        self.special_chars = special_chars
    
    def transform(self):
        main(self.datastream_id, self.url, self.token, self.json_path, self.special_chars)
