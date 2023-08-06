import re
from uuid import uuid4
from datetime import datetime, timezone

from typing import Dict, Any, Union

from dainik.proto.lmao_pb2 import Record

def get_random_id(n=10):
  return str(uuid4()).replace("-", "")[:n]

def get_timestamp():
  return int(datetime.now(timezone.utc).timestamp())

def get_record(k: str, v: Union[int, float, str]) -> Record:
  _tv = type(v)
  assert _tv in [int, float, str], f"[key = {k}] '{_tv}' is not a valid type"
  _vt = {
    int: Record.DataType.INTEGER,
    float: Record.DataType.FLOAT,
    str: Record.DataType.STRING,
  }[_tv]
  record = Record(key = k, value_type = _vt)
  if _tv == int:
    record.integer_data.append(v)
  elif _tv == float:
    record.float_data.append(v)
  elif _tv == str:
    record.string_data.append(v)
  return record


def split_iw(x: str):
  pat = r"([\w\-\s]+)@(\w{8})"
  out = re.findall(pat, x)
  if not out:
    raise ValueError(f"Incorrect instance_id {x}")
  id_or_name, workspace_id = out[0]
  return id_or_name, workspace_id
