# Auto generated file. DO NOT EDIT.

import requests
from functools import partial

from dainik.proto.lmao_pb2 import *

from dainik.yql.rest_pb2 import Echo
from dainik.yql.common import *


# ------ Stub ------ #

class LMAO_Stub:
  def __init__(self, url: str, session: requests.Session = None):
    self.url = url.rstrip("/")
    self.session = session or requests.Session()
    self.status = partial(call_rpc, sess = self.session, url = f"{url}/")
    self.protos = partial(call_rpc, sess = self.session, url = f"{url}/protos")

  def init_run(self, _InitRunRequest: InitRunRequest) -> Run:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "InitRunRequest", base64_string=message_to_b64(_InitRunRequest), rpc_name = "init_run")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _Run = Run() # predefine the output proto
    _Run = b64_to_message(echo_resp.base64_string, _Run)
    return _Run

  def on_log(self, _RunLog: RunLog) -> Acknowledge:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "RunLog", base64_string=message_to_b64(_RunLog), rpc_name = "on_log")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _Acknowledge = Acknowledge() # predefine the output proto
    _Acknowledge = b64_to_message(echo_resp.base64_string, _Acknowledge)
    return _Acknowledge

  def on_save(self, _FileList: FileList) -> Acknowledge:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "FileList", base64_string=message_to_b64(_FileList), rpc_name = "on_save")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _Acknowledge = Acknowledge() # predefine the output proto
    _Acknowledge = b64_to_message(echo_resp.base64_string, _Acknowledge)
    return _Acknowledge

  def on_train_end(self, _Run: Run) -> Acknowledge:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "Run", base64_string=message_to_b64(_Run), rpc_name = "on_train_end")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _Acknowledge = Acknowledge() # predefine the output proto
    _Acknowledge = b64_to_message(echo_resp.base64_string, _Acknowledge)
    return _Acknowledge

  def list_projects(self, _ListProjectsRequest: ListProjectsRequest) -> ListProjectsResponse:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "ListProjectsRequest", base64_string=message_to_b64(_ListProjectsRequest), rpc_name = "list_projects")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _ListProjectsResponse = ListProjectsResponse() # predefine the output proto
    _ListProjectsResponse = b64_to_message(echo_resp.base64_string, _ListProjectsResponse)
    return _ListProjectsResponse

  def list_runs(self, _ListRunsRequest: ListRunsRequest) -> ListRunsResponse:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "ListRunsRequest", base64_string=message_to_b64(_ListRunsRequest), rpc_name = "list_runs")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _ListRunsResponse = ListRunsResponse() # predefine the output proto
    _ListRunsResponse = b64_to_message(echo_resp.base64_string, _ListRunsResponse)
    return _ListRunsResponse

  def get_run_log(self, _Run: Run) -> RunLog:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "Run", base64_string=message_to_b64(_Run), rpc_name = "get_run_log")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _RunLog = RunLog() # predefine the output proto
    _RunLog = b64_to_message(echo_resp.base64_string, _RunLog)
    return _RunLog

  def list_files(self, _Run: Run) -> FileList:
    echo_resp: Echo = call_rpc(
      self.session,
      f"{self.url}/predict",
      Echo(message = "Run", base64_string=message_to_b64(_Run), rpc_name = "list_files")
    )

    if echo_resp.base64_string == "":
      # something else happened and we don't have a proto_data, so print the message
      print("\n> Server side error:")
      for l in echo_resp.message.splitlines():
        print(l)
      print("\n")
      return None
    
    _FileList = FileList() # predefine the output proto
    _FileList = b64_to_message(echo_resp.base64_string, _FileList)
    return _FileList


# ------ End Stub ------ #