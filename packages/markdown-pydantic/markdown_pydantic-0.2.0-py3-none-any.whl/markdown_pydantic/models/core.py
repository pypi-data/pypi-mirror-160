from __future__ import annotations
import json
import re
from typing import Any, Literal, Optional

from pydantic import BaseModel

from markdown_pydantic.files import to_yaml
from markdown_pydantic.types.simple import (
    AdditionalPropertiesT,
    AllOfT,
    AnyOfT,
    DefaultT,
    DescriptionT,
    JsonDataT,
    MaximumT,
    MinimumT,
    PatternT,
    PropertyEnumT,
    ReferenceT,
    TitleT,
    TypeT,
)


class Yaml:
    # Protocol
    ...
    # def yaml_data()


class Reference:
    """
    Logic that encapsulates translation, resolution of the `$ref` property.

    Example:

    "vpc": { "$ref": "#/definitions/VPCDefinition" },

    "vpc: Reference({ "$ref": "#/definitions/VPCDefinition" })
    > vps: VPCDefinition
    """

    _reference: dict[Literal["$ref"], str]

    def __init__(self, reference: ReferenceT) -> None:
        self._reference = reference
        self.value = reference["$ref"]

    def __str__(self) -> str:
        return self.value.split("/")[-1]


class RawProperty(BaseModel):
    """
    Class which represents a basic property of a schema and its associated properties present inside the JSON.
    """

    # The ones we know about.
    additionalProperties: AdditionalPropertiesT
    allOf: AllOfT
    anyOf: AnyOfT
    default: DefaultT = None
    description: DescriptionT = "No description 😢"
    enum: PropertyEnumT = None
    maximum: MaximumT
    minimum: MinimumT
    pattern: PatternT
    title: TitleT
    type: TypeT

    # Any other fields.
    extra: dict[str, Any] = {}

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.save_extra(data)

    def save_extra(self, data: Any):
        """Save extra parameters that are not a field of the model"""
        for key, value in data.items():
            if key not in self.extra and key not in self.__dict__:
                self.extra[key] = value


class Property(RawProperty):
    """
    Enriches the basic properties with fields and methods helpful for working with schemas.
    """

    is_required: bool = False
    ref: Optional[str]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if data.get("$ref"):
            self.ref = str(Reference({"$ref": data["$ref"]}))

    def _extract_definition(self, reference: str) -> list[str]:
        """Extracts definition names from references"""
        reference_content = json.dumps(reference)
        definitions = re.findall(r"#/definitions\W*(\w+)", reference_content)
        return definitions

    @property
    def reference(self) -> Optional[str]:
        """Returns the reference of the property"""
        if not any([self.allOf, self.anyOf, self.additionalProperties]):
            return None

        ref_type = "Unknown"
        reference = []

        if self.allOf:
            reference = self._extract_definition(self.allOf)
            ref_type = "Required"
        if self.anyOf:
            reference = self._extract_definition(self.anyOf)
            ref_type = "AnyOf"
        if self.additionalProperties:
            reference = self._extract_definition(self.additionalProperties)
            ref_type = "Optional"
        return f"{{{ref_type} {'/'.join(reference)}}}"

    @property
    def yaml_type(self) -> str:
        """
        Returns the type of the property.
        """
        prefix = "Required" if self.is_required else "Optional"
        type = self.type.capitalize() if self.type else "Unknown"
        return f"{{{prefix} {type}}}" or "string"

    def yaml_definition(self) -> str:
        """
        Returns the definition of the property.
        """
        return self.reference or self.yaml_type


class RawDefinition(BaseModel):
    """
    Defines basic/raw properties of a schema definition.
    """
    description: Optional[str]
    title: str
    type: str
    properties: dict[str, Property]
    required: list[str] = []


class Definition(RawDefinition):
    """
    Enriches the basic fields and methods helpful for working with definitions.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._set_required_properties()

    def _set_required_properties(self):
        """
        Sets required attribute to true for required properties.
        """
        for property_key in self.required:
            self.properties[property_key].is_required = True

    def yaml_block(self) -> str:
        """
        Returns a yaml codeblock describing fields on the definition.
        """
        return f"```yaml\n{self.to_yaml()}```"

    def yaml_data(self) -> JsonDataT:
        """
        Returns the yaml data for a definition.
        """
        # For each property, get the yaml data.
        yaml_data: JsonDataT = {}
        for property_key, property_value in self.properties.items():
            yaml_data[property_key] = property_value.yaml_definition()
        return yaml_data

    def to_yaml(self) -> str:
        """
        Returns the yaml representation of the schema.
        """
        return to_yaml(self.yaml_data())


class Schema(Definition):
    """
    Wraps instructions on how to load, validate, manage, transform and serialise a schema.

    Schema class can be associate with a parrent class for the execution of the yaml transformation.
    """

    definitions: Optional[dict[str, Definition]] = None

    @property
    def _definitions_in_yaml(self) -> dict[str, JsonDataT]:
        """
        Returns a list of all definitions in yaml format.
        """
        if not self.definitions:
            return {}

        yamls = {}
        for definition_key, definition_value in self.definitions.items():
            yamls[definition_key] = definition_value.to_yaml()
        return yamls

    def generate_markdown(self) -> str:
        """
        Returns the markdown representation of the schema.
        """
        from markdown_pydantic import templates
        return templates.schema_to_markdown(self)

    def save_to_md(self, file_path: str) -> None:
        """Saves the schema to a markdown file"""
        # Get the main schema yaml form.

        markdown_content = self.generate_markdown()

        with open(file_path, "w") as file:
            file.write(markdown_content)

    @classmethod
    def from_json(cls, json_data: JsonDataT) -> Schema:
        return cls(**json_data)
