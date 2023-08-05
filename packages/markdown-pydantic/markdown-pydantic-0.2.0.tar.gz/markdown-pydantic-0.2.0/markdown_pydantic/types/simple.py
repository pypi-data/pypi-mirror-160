from __future__ import annotations
from typing import Dict, Literal, Union
from typing import Any, Optional

# Alias types
TitleT = Optional[str] # Perhaps display a warning if missing.
DescriptionT = Optional[str]  # Perhaps display a warning if missing.

# Simple types
TypeT = Optional[str]  # Literal["object", "string"]
DefaultT = Optional[Union[str, list[str], Dict[str, Any]]]
MinimumT = Optional[Union[int, float]]
MaximumT = Optional[Union[int, float]]
PropertyEnumT = Optional[list[str]]
PatternT = Optional[str]
ReferenceT = dict[Literal["$ref"], str]

# Composite types
AnyOfT = Optional[list[Any]]
AllOfT = Optional[list[Any]]
AdditionalPropertiesT = Optional[Any]
JsonDataT = dict[str, Any]