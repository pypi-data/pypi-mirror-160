import json
import yaml

from markdown_pydantic.types.simple import JsonDataT


def write_to_file(file_path: str, content: str) -> None:
    """Writes content into a file"""
    with open(file_path, "w") as f:
        f.write(content)


def to_yaml(json_data: JsonDataT) -> str:
    """Serialises JSON data into YAML data"""
    return yaml.dump(json_data, default_flow_style=False)


def save_to_yaml(json_data: JsonDataT, yaml_path: str = "test.yaml"):
    """Saves JSON data into a YAML file"""
    yaml_data = to_yaml(json_data)
    write_to_file(yaml_path, yaml_data)
    print(f"Saved {yaml_path}")


def load_json_file(file_path: str) -> JsonDataT:
    """Loads a json file and returns the contents as a dictionary"""
    with open(file_path, "r") as f:
        return json.load(f)


def read_file(file_path: str) -> str:
    """Reads a file and returns the contents"""
    with open(file_path, "r") as f:
        return f.read()
