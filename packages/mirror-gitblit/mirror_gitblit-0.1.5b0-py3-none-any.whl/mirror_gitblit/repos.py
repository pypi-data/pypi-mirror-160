"""
Module to mirror gitblit repos

A Repository is a dictionary with this structure:

```
{
    "name":"javascript-vorlesung/asciidoctor-stylesheet-factory.git",
    "description":"Clone of asciidoctor-stylesheet-factory from github",
    "owners":["hbui"],
    "lastChange":"2018-11-28T15:26:47Z",
    "lastChangeAuthor":"Hong-Phuc Bui",
    "hasCommits":true,
    "showRemoteBranches":false,
    "useIncrementalPushTags":false,"
    accessRestriction":"VIEW",
    "authorizationControl":"NAMED",
    "allowAuthenticated":false,
    "isFrozen":false,
    "federationStrategy":"FEDERATE_THIS",
    "federationSets":[],
    "isFederated":false,
    "skipSizeCalculation":false,
    "skipSummaryMetrics":false,
    "isBare":true,
    "isMirror":false,
    "HEAD":"refs/heads/master",
    "availableRefs":["refs/heads/master"],
    "indexedBranches":[],
    "size":"892 KB",
    "preReceiveScripts":[],
    "postReceiveScripts":[],
    "mailingLists":[],
    "customFields":{},
    "projectPath":"javascript-vorlesung",
    "allowForks":true,
    "verifyCommitter":false,
    "gcThreshold":"500k",
    "gcPeriod":7,
    "maxActivityCommits":0,
    "metricAuthorExclusions":[],
    "commitMessageRenderer":"PLAIN",
    "acceptNewPatchsets":true,
    "acceptNewTickets":true,
    "requireApproval":false,
    "mergeTo":"master",
    "mergeType":"MERGE_ALWAYS",
    "lastGC":"1970-01-01T00:00:00Z"
}
```


"""
import os.path
import shutil
import subprocess
import json
import logging
import pprint
from typing import Callable


logger = logging.getLogger(__name__)

def make_curl_cmd(base_url:str, output_file_name:str, user:str = None, password:str = None):
    """
        Make curl command line.
    """
    authentication = None
    if user is not None:
        authentication = user
        if password is not None:
            authentication += ':' + password
        
    if authentication is not None:
        curl = ['curl',
                '--output', f"{output_file_name}",
                '--user', authentication,
                '-H', 'Accept-Language: en',
                '-X', 'GET',
                f'{base_url}/rpc/?req=LIST_REPOSITORIES']
    else:
        curl = ['curl',
                '--output', f"{output_file_name}",
                '-H', 'Accept-Language: en',
                '-X', 'GET',
                f'{base_url}/rpc/?req=LIST_REPOSITORIES']
    return curl


def list_repos(base_url: str, output_file_name: str, user:str, password:str):
    """
        downloads a list of repository in `source_base_url`. This function need
        the program `curl`.
        :arg base_url base url of gitblit server, it all parts of server before rpc
        :arg user user name to login
        :arg password password to login
    """
    curl = make_curl_cmd(base_url, output_file_name, user, password)
    logger.info(' '.join(curl))
    create_result = subprocess.run(curl)
    if create_result.returncode == 0:
        logger.info(f'    curl {curl[-1]} OK')
        return True
    else:
        logger.info(f'    curl {curl[-1]} FAIL')
        return False


def load_repos(repos_file_name: str):
    """
        loads a JSON-File, which describes repositories of a Gitblit Server.
        :arg repos_file_name
    """
    with open(repos_file_name, 'r') as f:
        data = json.load(f)
    data_as_list = []
    for k,v in data.items():
        data_as_list.append(v)
    return sorted(data_as_list, key=lambda repo:repo["name"])


def repo_size_to_int(repo):
    """
        convert given Size to bytes
    """
    (size, unit) = repo["size"].split()
    size = float(size.replace(",",""))
    if unit == "KB":
        return size * 1000
    if unit == "MB":
        return size * (1000**2)
    if unit == "GB":
        return size * (1000**3)
    return size


def check_valid_destination(destination:str):
    if os.path.isfile(destination):
        raise RuntimeError(f"path {destination} is a file")
    if os.path.isdir(destination) and len(os.listdir(destination)) != 0:
        raise RuntimeError(f"path {destination} is a directory and not empty")


def clone_mirror_repository(repo, base_url: str, destination:str):
    """
    execute the command
    
    `git clone --mirror {base_url}/{repo_name} {destination}`

    :param repo: A repository
    :param base_url: Base URL of the remote
    :param destination: where to mirror the repository
    """
    try:
        check_valid_destination(destination)
        name = repo['name']
        git_clone = ["git", "clone", "--mirror", f"{base_url}/{name}", destination]
        logger.info(' '.join(git_clone))
        git_return = subprocess.run(git_clone)
        summary = {name: {'clone': vars(git_return) }}
        if git_return.returncode == 0:
            logger.info(f'    clone {name} OK')
        else:
            logger.error(f'    clone {name} MAY goes WRONG')
            logger.error(summary)
        return summary
    except RuntimeError as ex:
        logger.error(ex)


def clone_repos(repositories_json: str, base_url: str, backup_dir:str, repo_filter:Callable=None, remove_existing_destination:bool=False):
    """
    Mirror all repositories listed in a JSON-File.


    :param repositories_json: A JSON-File points to a list of repositories
    :param base_url: the base-URL to remote server, for example `ssh://backup@{server}.{domain}.{tld}:{port}`
    :param backup_dir: the directory, where all repositories are mirrored.
    :param repo_filter: an optional  filter function to filter only to-be-cloned repositorie from the given list
    :param remove_existing_destination: remove the destination directory if this parameter is set to True and the directory
    exists.
    """

    list_of_repos = load_repos(repositories_json)
    if repo_filter:
        list_of_repos = filter(lambda repo: repo_filter(repo), list_of_repos)
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    for i, repos in enumerate(list_of_repos):
        destination = f"{backup_dir}/{repos['name']}"
        if os.path.exists(destination) and remove_existing_destination:
            shutil.rmtree(destination)
        clone_result = clone_mirror_repository(repos, base_url, destination)
        if logger.level == logging.INFO:
            info = pprint.pformat(clone_result)
            logger.info(info)


def update_repository(local_repo_dir):
    if not (os.path.exists(local_repo_dir) and os.path.isdir(local_repo_dir) ):
        raise RuntimeError(f"{local_repo_dir} does not exist or is not a directory")
    git_update = ["git", "-C", local_repo_dir, "remote", "update"]
    logger.info(" ".join(git_update))
    git_return = subprocess.run(git_update)
    summary = {local_repo_dir: {'update': vars(git_return) }}
    if git_return.returncode == 0:
        logger.info(f'    update repository {local_repo_dir} OK')
    else:
        logger.info(f'    update repository {local_repo_dir} MAY goes WRONG')
        logger.info(summary)
    return summary


def update_or_clone_repository(repo, base_url: str, destination:str):
    try:
       return update_repository(destination)
    except RuntimeError:
        return clone_mirror_repository(repo, base_url, destination)


# Some common filter
def repo_filter(repo, included_repos:[str] =[], exclude_repos:[str] = []):
    repo_name = repo["name"]
    if included_repos:
        return repo_name in included_repos
    else:
        if exclude_repos:
            return repo_name not in exclude_repos
        else:
            return True








