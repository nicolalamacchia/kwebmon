SITES_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "sites": {"type": "array"},
        "items": {"$ref": "#/$defs/site"}
    },
    "$defs": {
        "site": {
            "type": "object",
            "required": ["url"],
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Website URL"
                },
                "pattern": {
                    "type": "string",
                    "description": ("Python-compatible RegEx pattern to be "
                                    "used to validate website content")
                }
            }
        }
    }
}
