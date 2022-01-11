# Basic - python version

## Pre-reqs
- Python3 is available. 
- macos dependency   
  ```bash
  brew install autoconf automake libtool`
  pip3 install --upgrade pip
  ```

## Installation
### Setup Environment
```bash
python3 -m venv ./venv
```

### Install Dependencies
```bash
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

## Execute
### bot
```bash
python3 ./bot/chatbot.py
```
### Test 
```bash
python -m pytest tests
```

### Coverage report 
```bash
coverage run -m pytest tests
coverage report -m
```


## BOT Capabilities
- Supported Actions
  - Form - Ranged Numeric input
  - Form - Options with synonyms
  - Form - User Entry


## TODO:
- [] ability to provide BOT File 
- [] action `FormOption` handle response that does not include any synonyms
- [] function `getEntity` , handle FHIR Data in more generic manner
- [] step `utter_ProvideSummary` ,add ability to add response in tracker 
- [] Dockarize Setup
- [] Goodbye action utterance should not be captured in response.

## Next Layers
- [] RestAPI Layer
- [] Split `form config` into its own file/Class
- [] Add DB persistence
- [] Dockerize
- [] Deploy to AWS
- [] FHIR – evaluate HAPI/IBM FHIR model lib for dynamic data extraction
- [] Evaluate workflow engine approach like Cadence Workflow
- [] Evaluate OSS Rasa (Packaged ML/AI solution)