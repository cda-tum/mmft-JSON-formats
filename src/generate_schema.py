from argparse import ArgumentParser
from mmft_model import MMFTDataModel
import json


def main():
    parser = ArgumentParser(description="JSON Schema Generation")
    parser.add_argument("filename", help="Output file for the JSON schema")
    args = parser.parse_args()

    data_model_schema = MMFTDataModel.model_json_schema()
    content = json.dumps(data_model_schema, indent=4)
    with open(args.filename, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main()
