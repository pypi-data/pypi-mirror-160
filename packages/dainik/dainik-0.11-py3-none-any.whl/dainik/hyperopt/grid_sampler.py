from itertools import product
from typing import Union
from pydantic import BaseModel

from nbox import logger
from dainik.hyperopt.base import BaseSampler, SearchSpaceExhausted
from dainik.hyperopt.opt_types import _v0_data, List, Tuple, Dict

class GridParameter(BaseModel):
  data: Union[_v0_data, List[_v0_data], Tuple[_v0_data]]


class GridSampler(BaseSampler):
  def __init__(self, params: Dict[str, GridParameter]) -> None:
    super().__init__()
    self.params = params

    # do sanity checks on the values like they are all iterable or not
    keys = []
    values = []
    total_possible_combinations = 1
    for k,v in self.params.items():
      v = v.data
      if isinstance(v, (int, float, str)):
        # this usually means some constant value
        keys.append(k)
        values.append([v])
        continue
      keys.append(k)
      values.append(v)
      total_possible_combinations *= len(v)
    
    if total_possible_combinations > 100:
      logger.warning(f"Total possible combinations: {total_possible_combinations}")
      logger.warning(f"This is above the guard rail of 100 combinations.")

    # now we can build the search space, which is an array of all the possible states
    # this key_indexes contains to which array is current sample referring to
    self._keys = keys
    self._values = product(*values)

  def sample(self) -> dict:
    ret_params = {}
    try:
      values = next(self._values)
    except StopIteration:
      raise SearchSpaceExhausted("Search space exhausted")
    for k,v in zip(self._keys, values):
      ret_params[k] = v
    return ret_params

