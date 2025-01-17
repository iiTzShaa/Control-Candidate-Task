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

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/iiTzShaa/Control-Candidate-Task.git
cd Control-Candidate-Task
```

2. Build the Docker image:
```bash
docker build -t gitleaks-integration .
```

3. Set up test environment (optional):
```bash
# Create test directory
mkdir tests
cd tests

# Clone test repository
git clone https://github.com/atrull/fake-public-secrets.git
cd ..
```

4. Run a scan:
```bash
# Scan current directory
docker run -v $(pwd):/code gitleaks-integration gitleaks detect --no-git --report-path /code/output.json /code/

# Or scan test repository (if you set it up)
docker run -v $(pwd)/tests/fake-public-secrets:/code gitleaks-integration gitleaks detect --no-git --report-path /code/output.json /code/
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
