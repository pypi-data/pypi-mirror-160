"""Json schemas for checking of configurations content.
"""
import json
import pathlib

schema_folder = pathlib.Path(__file__).parent / "schemas"
ref_files = ["component.schema.json"]


def load_json(file_path):
    file_path = schema_folder / file_path
    with open(file_path) as json_file:
        schema_text = json_file.read()
    for ref in ref_files:
        schema_text = schema_text.replace(ref, f"file://{schema_folder}/{ref}")
    return json.loads(schema_text)


orchestrations_schema = load_json("orchestrations.schema.json")

transformations_schema = load_json("transformations.schema.json")

datamarts_schema = load_json("datamarts.schema.json")

extractor_schema = load_json("extractor.schema.json")

writer_schema = load_json("writer.schema.json")

project_schema = load_json("project.schema.json")
