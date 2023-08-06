import os
import re

from json import dumps
from typing import Dict, Any, List, Union
from nbox.utils import logger, ENVVARS as env
from nbox import Instance
from nbox.auth import secret
from requests import Session

import dainik.utils as U
from dainik.lmao_client import *
from dainik.proto.lmao_pb2 import AgentDetails
from dainik.git_utils import get_git_details

class Dainik():
  def __init__(self, instance_id: str = "Common@3oausmqp", *, local: bool = False) -> None:
    if not local:
      self._create_connection(instance_id)
    else:
      self.lmao = LMAO_Stub(url = "http://127.0.0.1:8080", session = Session())
    self._initialized = False
    self.nbx_job_folder = env.NBOX_JOB_FOLDER("")

  def _create_connection(self, instance_id):
    # prepare the URL
    id_or_name, workspace_id = U.split_iw(instance_id)
    logger.info(f"id_or_name: {id_or_name}")
    logger.info(f"workspace_id: {workspace_id}")
    instance = Instance(id_or_name, workspace_id)
    try:
      open_data = instance.open_data
    except AttributeError:
      raise Exception(f"Is instance '{instance.project_id}' running?")
    url = f"https://server-{open_data['url']}.build.nimblebox.ai/"
    logger.info(f"URL: {url}")
    
    # create a session with the auth header
    _session = Session()
    _session.headers.update({
      "NBX-TOKEN": open_data["token"],
      "X-NBX-USERNAME": secret.get("username"),
    })

    # define the stub
    self.lmao = LMAO_Stub(url = url, session = _session)

  def init(self, project_name: str, config: Dict[str, Any],):
    logger.info(f"Creating new run: {project_name}")

    # this is the config value that is used to store data on the plaform, user cannot be allowed to have
    # like a full access to config values
    log_config = {
      "user_config": config
    }
    
    # check if the current folder from where this code is being executed has a .git folder
    # NOTE: in case of NBX-Jobs the current folder ("./") is expected to contain git by default
    git_details = None
    if os.path.exists(".git"):
      git_details = get_git_details("./")
    log_config["git"] = git_details

    # continue as before
    self.project_name = project_name
    self.config = config
    self._agent_details = AgentDetails(
      nbx_job_id="jj_guvernr",
      nbx_run_id=U.get_random_id(4),
    )
    self.run = self.lmao.init_run(
      _InitRunRequest = InitRunRequest(
        agent_details=self._agent_details,
        created_at = U.get_timestamp(),
        project_id = self.project_name,
        config = dumps(self.config),
      )
    )

    logger.info(f"Assigned ID: {self.run.run_id}")
    self._initialized = True

  def log(self, y: Dict[str, Union[int, float, str]], step = None):
    logger.info(f"Logging: {y.keys()}")
    if not self._initialized:
      raise Exception("Run not initialized, call init() first")

    step = step if step is not None else U.get_timestamp()
    if step < 0:
      raise Exception("Step must be <= 0")
    run_log = RunLog(run_id = self.run.run_id)
    for k,v in y.items():
      record = U.get_record(k, v)
      record.step = step
      run_log.data.append(record)
    
    ack = self.lmao.on_log(_RunLog = run_log)
    if not ack.success:
      logger.error("  >> Server Error")
      for l in ack.message.splitlines():
        logger.error("  " + l)
      raise Exception("Server Error")
  
  def save_file(self, files: List[str]):
    logger.info(f"Saving files: {files}")
    if not self._initialized:
      raise Exception("Run not initialized, call init() first")

    file_list = FileList(run_id=self.run.run_id)
    for f in files:
      # remove path till env.NBOX_JOB_FOLDER, input can contain full path or part of it
      f = os.path.abspath(f)
      assert os.path.exists(f)
      f = re.sub(self.nbx_job_folder, "", f)
      file_list.files.append(File(
        name = f,
        created_at = int(os.path.getctime(f)),
        is_input=False
      ))
    ack = self.lmao.on_save(_FileList = file_list)
    if not ack.success:
      logger.error("  >> Server Error")
      for l in ack.message.splitlines():
        logger.error("  " + l)
      raise Exception("Server Error")

  def end(self):
    logger.info("Ending run")
    ack = self.lmao.on_train_end(_Run = Run(run_id=self.run.run_id,))
    if not ack.success:
      logger.error("  >> Server Error")
      for l in ack.message.splitlines():
        logger.error("  " + l)
      raise Exception("Server Error")
