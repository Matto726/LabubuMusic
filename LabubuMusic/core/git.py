import asyncio
import shlex
from typing import Tuple
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
import config
from ..logging import log_factory

async def install_dependencies(command: str) -> Tuple[str, str, int, int]:
    args = shlex.split(command)
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    return (
        out.decode("utf-8", "replace").strip(),
        err.decode("utf-8", "replace").strip(),
        proc.returncode,
        proc.pid,
    )

def update_upstream():
    repo_url = config.UPSTREAM_REPO
    
    if config.GIT_TOKEN:
        try:
            
            parts = repo_url.split("https://")
            domain_path = parts[1]
            user = domain_path.split("/")[1]
            
            clean_url = repo_url.replace("https://", "")
            if "github.com" in clean_url:
                git_user = clean_url.split("/")[1]
                authenticated_url = f"https://{git_user}:{config.GIT_TOKEN}@{clean_url}"
            else:
                authenticated_url = repo_url
        except Exception:
            authenticated_url = repo_url
    else:
        authenticated_url = config.UPSTREAM_REPO

    try:
        current_repo = Repo()
        log_factory("LabubuMusic").info("VPS Deployer: Git Client Found.")
    except GitCommandError:
        log_factory("LabubuMusic").warning("Git Command Error encountered.")
    except InvalidGitRepositoryError:
        current_repo = Repo.init()
        
        if "origin" in current_repo.remotes:
            remote = current_repo.remote("origin")
        else:
            remote = current_repo.create_remote("origin", authenticated_url)
            
        remote.fetch()

        current_repo.create_head(
            config.UPSTREAM_BRANCH,
            remote.refs[config.UPSTREAM_BRANCH],
        )
        current_repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(
            remote.refs[config.UPSTREAM_BRANCH]
        )
        current_repo.heads[config.UPSTREAM_BRANCH].checkout(True)
        
        try:
            remote.pull(config.UPSTREAM_BRANCH)
        except GitCommandError:
            current_repo.git.reset("--hard", "FETCH_HEAD")
            
        loop = asyncio.get_event_loop()
        loop.run_until_complete(install_dependencies("pip3 install --no-cache-dir -r requirements.txt"))
        
        log_factory("LabubuMusic").info("Upstream updates fetched successfully.")