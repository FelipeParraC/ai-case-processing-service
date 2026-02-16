from datetime import date, datetime
from uuid import UUID


def to_json_serializable(obj):

    if isinstance(obj, (date, datetime)):
        return obj.isoformat()

    if isinstance(obj, UUID):
        return str(obj)

    if isinstance(obj, dict):
        return {
            key: to_json_serializable(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            to_json_serializable(item)
            for item in obj
        ]

    return obj
