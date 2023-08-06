"""
Program to download the list of repository to a file.
One can use:

```
python repos.py
```

to download a list, or can use it as a module
"""

import subprocess
import json
from pprint import pprint

from mirror_gitblit.configuration import load_configuration


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
    print(' '.join(curl))
    create_result = subprocess.run(curl)
    return create_result.returncode == 0


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
    (size, unit) = repo["size"].split()
    size = float(size.replace(",",""))
    if unit == "KB":
        return size * 1000
    if unit == "MB":
        return size * (1000**2)
    if unit == "GB":
        return size * (1000**3)
    return size


def list_gitblit_repositories(argv):
    config = load_configuration(argv[1])
    base_url = config["source_web_url"]
    filename = config["repositories_json"]
    (user, password) = (config["user"], config["password"])
    download_list_of_repo_ok = list_repos(base_url, filename, user, password)
    if download_list_of_repo_ok:
        repos = load_repos(filename)
        # sorted_repos = sorted(repos, key=lambda item: repo_size_to_int(item) )
        print("    Found ", len(repos), "repositories in the list")
        print("    List of repos is downloaded in", filename)
    else:
        print("Cannot download list of repositories!")
    return 0


def cli_list_repos():
    import sys
    list_gitblit_repositories(sys.argv)


########
def clone_mirror_repository(repo, base_url: str, destination:str):
    name = repo['name']
    git_clone = ["git", "clone", "--mirror", f"{base_url}/{name}", destination]
    print('\n   ',' '.join(git_clone))
    git_return = subprocess.run(git_clone)
    summary = {name: {'clone': vars(git_return) }}
    if git_return.returncode == 0:
        print(f'    clone {name} OK')
    else:
        print(f'    clone {name} MAY goes WRONG')
        print(summary)
    return summary


def repo_filter(repo, config):
    try:
        included_repos = config["included_repos"]
        if included_repos:
            return repo["name"] in included_repos
        else:
            return True
    except KeyError:
        return True


def cli_clone_repos():
    import sys, os, shutil

    config = load_configuration(sys.argv[1])
    list_of_repos = load_repos(config["repositories_json"])
    list_of_repos = filter(lambda repo: repo_filter(repo, config), list_of_repos)
    base_url = config["source_base_url"]
    backup_dir = config["backup_dir"]
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    for i, repos in enumerate(list_of_repos):
        destination = f"{backup_dir}/{repos['name']}"
        if os.path.exists(destination):
            shutil.rmtree(destination)
        clone_result = clone_mirror_repository(repos, base_url, destination)
        pprint(clone_result)




if __name__ == "__main__":
    cli_list_repos()