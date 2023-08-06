"""
Module to mirror gitblit repos

A Repository is a dictionary with this structure:

```json
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


class Gitblit:

    def __init__(self, source_web_url:str, curl_credentials_file:str, source_base_url:str, repository_json:str, backup_dir:str):
        """
        Doc.

        :param source_web_url: URl to Web-interface of gitblit-server, for example `https://{host}.{domain}.{tld}/gitblit`

        :param source_base_url: the base-URL to remote gitblit, for example `ssh://backup@{server}.{domain}.{tld}:{port}`
        :param repository_json: JSON-File, where repositories of this server are listed.
        :param backup_dir: the directory, where mirrored repositories are saved.
        """
        self._repository_json = repository_json
        self._source_web_url = source_web_url
        self._source_base_url = source_base_url
        self._curl_credentials_file = curl_credentials_file
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        self._backup_dir = backup_dir

    def make_curl_cmd(self) -> [str]:
        """
        Make cUrl command

        :return: a list of String, represents the cUrl command, which is ready to be used in `subprocess.run()`
        """

        if self._curl_credentials_file is not None:
            curl = ['curl',
                    '--output', f"{self._repository_json}",
                    #'--user', authentication,
                    '--netrc-file', self._curl_credentials_file,
                    '-H', 'Accept-Language: en',
                    '-X', 'GET',
                    f'{self._source_web_url}/rpc/?req=LIST_REPOSITORIES']
        else:
            curl = ['curl',
                    '--output', f"{self._repository_json}",
                    '-H', 'Accept-Language: en',
                    '-X', 'GET',
                    f'{self._source_web_url}/rpc/?req=LIST_REPOSITORIES']
        return curl

    def list_repositories(self):
        """
        download the list of repositories and save it to a file named by attribute `self.repository_json`
        """
        curl = self.make_curl_cmd()
        logger.info(' '.join(curl))
        create_result = subprocess.run(curl)
        if create_result.returncode == 0:
            logger.info(f'    curl {curl[-1]} OK')
            return True
        else:
            logger.error(f'    curl {curl[-1]} FAIL')
            return False

    def load_repos(self) -> [str]:
        """
        loads a JSON-File, which describes repositories of a Gitblit Server.
        """
        with open(self._repository_json, 'r') as f:
            data = json.load(f)
        data_as_list = []
        for k,v in data.items():
            data_as_list.append(v)
        return sorted(data_as_list, key=lambda repo:repo["name"])

    def clone_repos(self, repo_filter:Callable=None, remove_existing_destination:bool=False):
        """
        Mirror all repositories listed in `self._repositories_json`

        :param repo_filter: an optional  filter function to filter only to-be-cloned repositorie from the given list
        :param remove_existing_destination: remove the destination directory if this parameter is set to True and the directory
        exists.
        """
        list_of_repos = self.load_repos()
        if repo_filter:
            list_of_repos = filter(lambda repo: repo_filter(repo), list_of_repos)

        for i, repos in enumerate(list_of_repos):
            try:
                summary = self._clone_mirror_repository(repos, remove_existing_destination)
                logger.info(pprint.pformat(summary))
            except RuntimeError as ex:
                logger.error(ex)

    def _clone_mirror_repository(self, repo, remove_existing_destination:bool):
        """
        execute the command

        `git clone --mirror {base_url}/{repo_name} {destination}`

        :param repo: A repository
        :param remove_existing_destination: if the local repository in backup-dir is removed before clone
        """
        name = repo['name']
        destination = f'{self._backup_dir}/{name}'
        if os.path.exists(destination) and remove_existing_destination:
            shutil.rmtree(destination)
        self._check_valid_destination(destination)
        git_clone = ["git", "clone", "--mirror", f"{self._source_base_url}/{name}", destination]
        logger.info(' '.join(git_clone))
        git_return = subprocess.run(git_clone)
        summary = {"name": name, 'clone': vars(git_return) }
        if git_return.returncode == 0:
            logger.info(f'    clone {name} OK')
        else:
            logger.error(f'    clone {name} MAY goes WRONG')
            logger.error(summary)
        return summary


    @staticmethod
    def _check_valid_destination(destination:str):
        if os.path.isfile(destination):
            raise RuntimeError(f"path {destination} is a file")
        if os.path.isdir(destination) and len(os.listdir(destination)) != 0:
            raise RuntimeError(f"path {destination} is a directory and not empty")

    def update_repos(self, repo_filter:Callable=None ):
        """
        Update all repositories in :param repositories_json:.

        :param repo_filter: filter to check if a repository should be cloned
        """
        list_of_repos = self.load_repos()
        if repo_filter:
            list_of_repos = filter(lambda repo: repo_filter(repo), list_of_repos)

        for i, repo in enumerate(list_of_repos):
            try:
                self._update_repository(repo)
            except RuntimeError:
                self._clone_mirror_repository(repo, False)

    def _update_repository(self, repo):
        local_repo_dir = f"{self._backup_dir}/{repo['name']}"
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
            logger.error(pprint.pformat(summary))
        return summary



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


def inclusive_exclusive_filter(repo, included_repos:[str] =[], exclude_repos:[str] = []):
    repo_name = repo["name"]
    if included_repos:
        return repo_name in included_repos
    else:
        if exclude_repos:
            return repo_name not in exclude_repos
        else:
            return True















