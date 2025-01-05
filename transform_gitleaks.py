import subprocess
import json
import sys
from typing import List, Union
from pydantic import BaseModel

class Finding(BaseModel):
   filename: str
   line_range: str
   description: str

class TransformedOutput(BaseModel):
   findings: List[Finding]

class ErrorOutput(BaseModel):
   exit_code: int
   error_message: str

def run_gitleaks(command: List[str]) -> bool:
   try:
       print(f"Running Gitleaks command: {' '.join(command)}")
       result = subprocess.run(command, capture_output=True, text=True)
       return result.returncode in [0, 1]
   except subprocess.CalledProcessError:
       return False

def transform_output(input_path: str) -> Union[TransformedOutput, ErrorOutput]:
   try:
       with open(input_path, 'r') as file:
           raw_data = json.load(file)
       
       findings = [
           Finding(
               filename=finding['File'],
               line_range=f"{finding['StartLine']}-{finding['EndLine']}",
               description=finding['Description']
           )
           for finding in raw_data
       ]
       
       return TransformedOutput(findings=findings)
   except Exception as e:
       return ErrorOutput(exit_code=1, error_message=str(e))

def main() -> None:
   input_path = "/code/output.json"
   gitleaks_args = sys.argv[1:]
   
   if not run_gitleaks(gitleaks_args):
       error = ErrorOutput(exit_code=2, error_message="Gitleaks execution failed")
       print(json.dumps(error.model_dump(), indent=4))
       sys.exit(2)
   
   result = transform_output(input_path)
   print(json.dumps(result.model_dump(), indent=4))
   
   if isinstance(result, ErrorOutput):
       sys.exit(result.exit_code)

if __name__ == "__main__":
   main()