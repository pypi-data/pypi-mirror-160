class SearchSpaceExhausted(Exception):
  pass

class BaseSampler(object):
  """This is the base class for all the samplers"""
  def __init__(self) -> None:
    super().__init__()

  def build_search_space(self) -> None:
    """Subclass and overwrite your logic to build the search space as per your definitions. Default is No-Op"""
    pass
    

  def sample(self) -> dict:
    """Subclass and overwrite your logic to get one sample of data, this should return a
    dictionary of parameters to be used for the experiment"""
    raise NotImplementedError("Subclass must implement abstract method")

  def update(self) -> None:
    """Subclass and overwrite your logic to update any kind of internal state of the sampler, ex.
    grid search can double check with the NBX-Servers if everything is fine or not. Gets called
    after every sample returned. By default is a No-Op"""
    pass

  def __iter__(self) -> None:
    try:
      while True:
          yield self.sample()
    except SearchSpaceExhausted:
      return
