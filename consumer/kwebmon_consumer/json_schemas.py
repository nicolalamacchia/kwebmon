MESSAGE_KEY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "url": {
            "description": "Target website URL",
            "type": "string"
        },
        "pattern": {
            "description": ("Python-compatible RegEx pattern used to validate "
                            "website content"),
            "type": ["string", "null"]
        }
    },
    "required": ["url", "pattern"]
}

MESSAGE_VALUE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "utc_completed_at": {
            "description": "Timestamp (ISO-8601) of the last check",
            "type": "string"
        },
        "response_time": {
            "description": "Website response time",
            "type": "number",
            "minimum": 0
        },
        "status_code": {
            "description": "Website response HTTP status code",
            "type": "number"
        },
        "error": {
            "description": ("Error returned in case of failure while checking "
                            " the website health"),
            "type": "string"
        },
        "is_valid_content": {
            "description": ("True if the website textual content contains a "
                            "specified pattern"),
            "type": "boolean"
        },
    },
    "required": ["utc_completed_at"]
}
