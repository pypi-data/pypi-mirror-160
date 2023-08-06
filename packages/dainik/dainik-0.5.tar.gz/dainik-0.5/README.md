# nimblebox-lmao

Logging, Monitoring, Alerting &amp; Observability

## Usage

For protobuf generation:
- `sh gen.sh` will generate all the required files, but will also (⚠️) overwrite your `lmao_server.py` file.
- `sh update_proto.sh` to only update the proto message definitions

For running the server:
- `python3 -m uvicorn:server app` to run the server, it will connect to the backend on it's own

For running the clients:
- `python3 -m clients.new` will do a complete run which includes `init`, `on_log`, `on_save` and `on_train_end` APIs
- `python3 -m clients.stat --help` will tell more about getting the data from the DB
- `python3 -m clients.logs --help` will tell more about getting the logs from the DB

## Dev

```
git clone ...
cd nimblebox-lmao/
git submodule init
git submodule update --remote
```
