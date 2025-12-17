
import yaml
from src.generator import CustomDumper

data = {
    "summary": "Sum",
    "description": "Desc",
    "operationId": "OpId",
    "tags": ["Tag"],
    "parameters": []
}

print("Dict keys:", list(data.keys()))

yaml_out = yaml.dump(data, Dumper=CustomDumper, sort_keys=False, allow_unicode=True, indent=2, width=float("inf"))
print("\nYAML Output:")
print(yaml_out)
