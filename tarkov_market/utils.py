import json
from typing import Any


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()


def _to_json(obj: Any) -> str:
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)
