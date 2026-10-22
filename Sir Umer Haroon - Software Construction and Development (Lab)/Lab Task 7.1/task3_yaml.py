import json
from typing import Any, Dict
import yaml


def load_config(filename):
    with open(filename, "r") as file:
        return yaml.safe_load(file)


def yaml_to_json(yaml_filename, json_filename):
    config_data = load_config(yaml_filename)
    with open(json_filename, "w") as json_file:
        json.dump(config_data, json_file, indent=2)


config = load_config("config.yaml")
print(f"Debug mode: {config.get('debug')}")
print(f"Minimum GPA: {config.get('min_gpa')}\n")
print("Students:")
for student in config.get("students", []):
    print(student)
print(f"\nType of students: {type(config.get('students'))}")
yaml_to_json("config.yaml", "config_from_yaml.json")