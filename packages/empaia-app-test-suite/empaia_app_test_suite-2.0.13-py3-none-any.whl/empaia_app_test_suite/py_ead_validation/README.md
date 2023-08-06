# Py EAD Validation

## Code Style

```bash
sudo apt update
sudo apt install python3-venv python3-pip
cd py-ead-validation
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

```bash
isort .
black .
pycodestyle *.py
pylint .
```

## Usage

### Command Line Interface

```bash
$ python -m py_ead_validation -h
usage: __main__.py [-h] [--config-file CONFIG_FILE] [--enable-legacy-support] ead_file ead_schema_dir namespaces_dir ead_settings_file

EAD Validator

positional arguments:
  ead_file              Path to an EAD file to be validated
  ead_schema_dir        Path to a directory containing EAD schema files
  namespaces_dir        Path to a directory containing namespace files
  ead_settings_file     Path to an ead-settings file

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        Path to a config file that should additionally be validated against the given EAD
  --enable-legacy-support
                        Include allowed legacy schemas
```

### Python Package

```python
from py_ead_validation.ead_validator import validate_ead


ead = {
    "$schema": "https://developer.empaia.org/schema/ead-app-schema-draft-3.json",
    "name": "Test App",
    "name_short": "TestApp",
    "namespace": "org.empaia.vendor_name.ta.v1",
    "description": "EAD for testing purposes",
    "configuration": {
        "threshold": {
            "type": "float",
            "storage": "global",
            "optional": True,
        },
        "count": {
            "type": "integer",
            "storage": "global",
            "optional": False,
        }
    },
    "inputs": {
        "my_wsi": {"type": "wsi"},
        "my_rectangle": {
            "type": "rectangle",
            "reference": "inputs.my_wsi",
            "classes": ["org.empaia.global.v1.classes.roi"],
        },
    },
    "outputs": {
        "my_rectangle": {
            "type": "rectangle",
            "reference": "inputs.my_wsi",
        },
        "my_classification": {"type": "class", "reference": "outputs.my_rectangle"},
    },
}

# raises EadValidationError unless compliant
validate_ead(ead)

# raises EadValidationError unless compliant but including legacy EAD versions
validate_ead(ead, enable_legacy_support=True)

# EADs with configuration section can be validated together with a given config
config = {"threshold": 0.75, "count": 3}

# can raise EadValidationError or ConfigValidationError
# ...either without legacy EAD version support
validate_ead_with_config(ead, config)
# ...or with legacy EAD version support
validate_ead_with_config(ead, config, enable_legacy_support=True)

# configs must match exactly the ead's configuration section
validate_ead_with_config(ead, {"threshold": True, "count": 3}) # ConfigValidationError (wrong type)
validate_ead_with_config(ead, {"something": 42, "count": 100}) # ConfigValidationError (unrelated entry)
validate_ead_with_config(ead, {"threshold": 0.75})             # ConfigValidationError (missing entry)
```
