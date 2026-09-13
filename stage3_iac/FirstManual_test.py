import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from iac_generator import IaCGenerator

generator = IaCGenerator()

# 1. AWS
with open("stage3_iac/mock_inputs/mapped_spec_aws.json") as f:
    aws_spec = json.load(f)
generator.generate(aws_spec, "output/terraform_outputs/test_aws")

# 2.Azure
with open("stage3_iac/mock_inputs/mapped_spec_azure.json") as f:
    azure_spec = json.load(f)
generator.generate(azure_spec, "output/terraform_outputs/test_azure")

print("ALL GENERATIONS COMPLETE!")