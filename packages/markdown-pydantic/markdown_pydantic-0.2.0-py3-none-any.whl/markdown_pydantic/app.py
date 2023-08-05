"""Script for executing generting of the schema"""
import argparse
import importlib
from types import ModuleType
from typing import Type

from pydantic import BaseModel

from markdown_pydantic.files import load_json_file
from markdown_pydantic.models.core import Schema
from markdown_pydantic.types.simple import JsonDataT


def import_pydantic_model(module_path: str) -> ModuleType:
    """Import a pydantic model from a path"""
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as error:
        print("God Damn 👮‍♂️, import error:", error)
        raise error
    return module


def get_module_and_class_name(model_path: str) -> tuple[str, str]:
    """
    Get module and class name from a model_path.
    """
    module, class_name = model_path.rsplit(".", 1)
    return (module, class_name)


def get_schema_from_model(model_path: str) -> JsonDataT:
    """
    Get the schema from the model path

    Where, model_path is defined as follows:

    model_path = "module.submodule.submodule.ClassName"
    """
    module_path, class_name = get_module_and_class_name(model_path)
    module = import_pydantic_model(module_path)
    ModelClass = getattr(module, class_name)
    return ModelClass.schema()


def define_arguments():
    """Define arguments for the script"""
    parser = argparse.ArgumentParser(
        description="Transform a config schema into a Markdown document."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to the input JSON file.",
    )
    group.add_argument(
        "-m",
        "--model",
        type=str,
        help="Path to the model class, e.g. markdown_pydantic.models.core.Definition",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output Markdown file.",
        required=True,
    )
    return parser.parse_args()


def run():
    """Run the script"""
    args = define_arguments()
    if args.input:
        model_schema = load_json_file(args.input)
    else:
        model_schema = get_schema_from_model(args.model)

    output_path = args.output

    schema = Schema(**model_schema)

    schema.save_to_md(output_path)

    print(f"Schema saved to {args.output}")


if __name__ == "__main__":
    run()
