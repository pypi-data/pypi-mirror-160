from jsonschema import validate, validators, Draft7Validator
from dateutil.parser import parse

def is_datetime_string(validator, value, instance, schema):
    try:
        parse(instance)
    except (ValueError, TypeError) as e:
        raise ValidationError(str(e))

types = {
    "datetime_string": {
        "type": "string",
        "is_datetime_string": {
        }
    }
}

models = {
    "run_application_input": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
            },
            "id": {
                "type": "integer"
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "input": {
                "type": "string"
            },
        },
        "additionalProperties": False,
        "required": ["action", "id"]
    },
    "run_task_input": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
            },
            "id": {
                "type": "integer"
            },
        },
        "additionalProperties": False,
        "required": ["action", "id"]
    },
    "stop_run_input": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
            },
            "id": {
                "type": "integer"
            },
        },
        "additionalProperties": False,
        "required": ["action", "id"]
    },
}

types = {
    "datetime_string": {
        "type": "string",
        "is_datetime_string": {
        }
    }
}

def validate_model(model_name, data):
    MyValidator = validators.extend(
        Draft7Validator,
        validators = {
            'is_datetime_string': is_datetime_string
        }
    )
    schema = {
        "types": types,
        "models": models,
        "$ref": f"#/models/{model_name}"
    }
    my_validator = MyValidator(schema=schema)
    my_validator.validate(data)
