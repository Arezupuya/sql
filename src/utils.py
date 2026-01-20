import json
from datetime import datetime

def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def print_json(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))
