# Gitleaks Integration

A Docker tool that combines Gitleaks secret detection with Python output processing.

## Components

### 1. Python Script (`transform_gitleaks.py`)
- Runs Gitleaks with provided arguments
- Transforms output to specified JSON format
- Uses Pydantic for data modeling
- Handles errors with structured output

### 2. Dockerfile
- Multi-stage build using:
  - `zricethezav/gitleaks:latest`
  - `python:3.10-alpine3.16`

## Usage

1. Build the image:
```bash
docker build -t gitleaks-python .
```

2. Run a scan:
```bash
docker run -v $(pwd):/code gitleaks-python gitleaks detect --no-git --report-path /code/output.json /code/
```

## Output Format

Success:
```json
{
    "findings": [
        {
            "filename": "example.tf",
            "line_range": "10-10",
            "description": "AWS Access Key"
        }
    ]
}
```

Error:
```json
{
    "exit_code": 2,
    "error_message": "Gitleaks execution failed"
}
```

## Requirements
- Docker
- Repository to scan
