# Parts of the code are taken from SpellML library
# I will drop a more details during release
# License Unkown

from git import Repo
from nbox import logger

def get_git_details(folder):
  repo = Repo(folder)

  # check for any uncommited files
  unstaged = {}
  diff = repo.index.diff("HEAD")
  for f in diff:
    path = f.a_path or f.b_path # when new file is added, a_path is None
    unstaged[path] = f.change_type
  logger.warning(f"Uncommited files: {unstaged}")

  # get the remote url
  try:
    remote_url = repo.remote().url
  except ValueError:
    remote_url = None

  # get the size of the repository
  size = None
  for line in repo.git.count_objects("-v").splitlines():
    if line.startswith("size:"):
      size = int(line[len("size:") :].strip())
  if size > (1 << 30):
    logger.warning(f"Repository size over 1GB, you might want to work on it")

  return {
    "remote_url": remote_url,
    "branch": repo.active_branch.name,
    "commit": repo.head.commit.hexsha,
    "unstaged": unstaged,
    "size": size,
  }

