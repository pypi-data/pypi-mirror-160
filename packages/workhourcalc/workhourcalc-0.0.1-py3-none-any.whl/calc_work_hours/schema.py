result_schema = {'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': [], 'saturday': [],
                 'sunday': []}

main_json_schema_structure = {
    "type": "object",
    "properties": {
        "monday": {
            "type": "array",
            "items": {}
        },
        "tuesday": {
            "type": "array",
            "items": {}
        },
        "wednesday": {
            "type": "array",
            "items": {}
        },
        "thursday": {
            "type": "array",
            "items": {}
        },
        "friday": {
            "type": "array",
            "items": {}
        },
        "saturday": {
            "type": "array",
            "items": {}
        },
        "sunday": {
            "type": "array",
            "items": {}
        }
    },
    "required": [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]
}
