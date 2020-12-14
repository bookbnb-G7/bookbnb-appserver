from typing import Any, Dict


def get_error_message(response: Dict[str, Any]):
    return response["detail"]
