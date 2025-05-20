from __future__ import annotations

import datetime as dt
from typing import Any

import jsonpickle.pickler
import jsonpickle.unpickler

# override the default pickler/unpickler to better handle some types


class Pickler(jsonpickle.pickler.Pickler):  # type: ignore[misc] # jsonpickle/jsonpickle#441
    def _flatten(self, obj: object) -> Any | None:
        if isinstance(obj, dt.datetime) and not obj.utcoffset():
            # naive datetimes or UTC datetimes can be stored directly
            return obj
        if isinstance(obj, bytes):
            return obj
        return super(Pickler, self)._flatten(obj)


class Unpickler(jsonpickle.unpickler.Unpickler):  # type: ignore[misc] # jsonpickle/jsonpickle#441
    pass


def encode(value: object) -> Any | None:
    return Pickler().flatten(value)


def decode(value: object) -> Any | None:
    return Unpickler().restore(value)
