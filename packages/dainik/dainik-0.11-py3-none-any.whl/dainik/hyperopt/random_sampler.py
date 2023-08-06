import numpy as np
from typing import Dict, List, Union
from pydantic import BaseModel

from dainik.hyperopt.base import BaseSampler

class RandomParameter(BaseModel):
  """Create a parameters to be sampled. Provide either ``x`` or ``a`` ` and ``b``.

  Args:
    x (List[Union[int, float, str]]): This is the possible list of values for this parameter.
    a (Union[float, int]): This is the lower bound of the random distribution.
    b (Union[float, int]): This is the upper bound of the random distribution.
    dist (str, optional): This is the distribution to use. Defaults to "uniform".
  """
  x: List[Union[int, float, str]] = []
  a: Union[float, int] = None
  b: Union[float, int] = None
  dist: str = "uniform"


class RandomSampler(BaseSampler):
  applicable_distributions = [
    "uniform", "normal", "beta", "poisson",
    # "lognormal",  "gamma", "weibull",
  ]

  def __init__(self, params: Dict[str, RandomParameter], n_runs: int = 10, seed: int = 4) -> None:
    super().__init__()

    # sanity checks
    param_to_chose = set()
    for k, param in params.items():
      assert param.dist in self.applicable_distributions, f"Distribution {param.dist} is not supported"
      if param.x:
        assert param.a is None and param.b is None, "Cannot specify x and a/b"
        param_to_chose.add(k)
      else:
        assert param.a is not None and param.b is not None, "Either specify x or must specify a/b"
        assert param.a < param.b, "a must be smaller than b"
        param.a = max(0.1, param.a)
        assert param.a > 0, "a must be positive"
        assert param.b > 0, "b must be positive"

    self.params = params
    self.n_runs = n_runs
    self.seed = seed
    self.rng = np.random.RandomState(seed)
    self.param_to_chose = param_to_chose

  def sample(self) -> dict:
    ret_params = {}
    for k, param in self.params.items():
      if k in self.param_to_chose:
        # this is based on a predetermined list of events
        if param.dist == "uniform":
          # this is the default so just sample, add and continue
          v = self.rng.choice(param.x)
          ret_params[k] = v
          continue
        
        elif param.dist == "normal":
          p = self.rng.normal(0, 1, size = len(param.x))
        elif param.dist == "beta":
          p = self.rng.beta(0, 1, size = len(param.x))
        elif param.dist == "poisson":
          p = self.rng.poisson(size = len(param.x))

        # force normalise distribution
        p = p.astype(np.float32)
        if p.min() < 0:
          p -= p.min()
        p /= p.sum()
        v = self.rng.choice(a = param.x, p = p)
      else:
        # this is based on a random distribution
        if param.dist == "uniform":
          v = self.rng.uniform(param.a, param.b)
        elif param.dist == "normal":
          v = self.rng.normal(param.a, param.b)
        elif param.dist == "beta":
          v = self.rng.beta(param.a, param.b)
        elif param.dist == "poisson":
          v = self.rng.poisson(param.a)
      ret_params[k] = v
    return ret_params

  def __iter__(self):
    for _ in range(self.n_runs):
      yield self.sample()
