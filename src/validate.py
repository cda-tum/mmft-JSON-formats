from argparse import ArgumentParser
from utils import is_valid_file
from mmft_model import MMFTDataModel
from pydantic import ValidationError

def main():
    parser = ArgumentParser(description="JSON Schema Generation")
    parser.add_argument("filename", help="Output file for the JSON schema", type=lambda f: is_valid_file(parser, f))
    args = parser.parse_args()

    with open(args.filename, "r") as file:
        content = file.read()
        try:
            MMFTDataModel.model_validate_json(content)
            valid = True
        except ValidationError as e:
            errors = e
            valid = False

        if valid:
            print('File is valid.')
        else: 
            print('File is invalid.')
            print(errors)

if __name__ == "__main__":
    main()
