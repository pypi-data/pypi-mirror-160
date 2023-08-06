# Dainik

`Dainik` is a client library for NimbleBox.ai LMAO (Logging, Monitoring, Alerts and Observability) service.

## Usage

```python
from dainik import Dainik

# initialise the client object
dk = Dainik()

# initialise the run
dk.init(
  "california",
  config = {
    "model_name": "qual",
    "config": {
      "batch_size": 32,
      "n_steps": n_steps,
      "optimizer": "adam",
    }
  },
)

for epoch in range(10):
  log = {
    "loss": 1 / epoch,
    "accuracy": epoch,
  }
  dk.log(log, step = epoch)

  # optionally log metrics directly
  dk.metrics.f1_score(
    x = [[1, 2, 3]],
    y = [[1, 2, 1]],
    step = epoch
  )

  # log files for tracking as well, wildcards work as well!
  dk.save_files([f"./checkpoint-{epoch}/*"])

dk.end() # send signal to sleep
```

## Dev

Due to the current structure the source code for this is only available for NimbleBox.ai engineers. This is spun out of a much larger monorepo which contains the logic for server and client together which helps us work on this faster. 
