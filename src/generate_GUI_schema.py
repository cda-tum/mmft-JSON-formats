from argparse import ArgumentParser
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, Union
from enum import Enum
import mmft_model
import json

config = ConfigDict(
    strict=True, extra="forbid", validate_assignment=True, alias_generator=to_camel
)

class GUIDataModel(BaseModel):
    model_config = config

    network: mmft_model.Network
    simulation: mmft_model.Simulation = None
    results: Optional[list[Union[mmft_model.BasicResult, mmft_model.ExtensiveResult]]] = None
    settings: Optional[mmft_model.Settings] = None
    log: Optional[str] = Field(
        default=None,
        description="contains the entire designer log output at the time of export",
    )

def main():
    parser = ArgumentParser(description="JSON Schema Generation")
    parser.add_argument("filename", help="Output file for the JSON schema")
    args = parser.parse_args()

    data_model_schema = GUIDataModel.model_json_schema()
    content = json.dumps(data_model_schema, indent=4)
    with open(args.filename, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main()
