from markdown_pydantic.models.core import Definition, Schema


def render_section(definition: Definition, title: str) -> str:
    output: list[str] = [title]

    # Add schema description.
    if definition.description:
        output.append(definition.description)

    # Add YAML block.
    output.append(definition.yaml_block())

    # Return a full string.
    return "\n\n".join(output)


def schema_to_markdown(schema: Schema) -> str:
    # Render the main schema definition
    output = [render_section(schema, f"# {schema.title}")]

    if schema.definitions:
        output.append("## Definitions")

        # Render each definition.
        for definition in schema.definitions.values():
            def_section = render_section(definition, f"### {definition.title}")
            output.append(def_section)

    return "\n\n".join(output)
