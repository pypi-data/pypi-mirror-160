import sys, os, shutil
from pprint import pprint
from mirror_gitblit.configuration import load_configuration
from mirror_gitblit.repos import list_repos, \
    load_repos, \
    clone_mirror_repository, \
    update_or_clone_repository, \
    repo_filter


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


def list_repos():
    config = load_configuration(sys.argv[1])
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






def update_repos():
    config = load_configuration(sys.argv[1])
    list_of_repos = load_repos(config["repositories_json"])
    list_of_repos = filter(lambda repo: repo_filter(repo, config), list_of_repos)
    base_url = config["source_base_url"]
    backup_dir = config["backup_dir"]
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    for i, repos in enumerate(list_of_repos):
        destination = f"{backup_dir}/{repos['name']}"
        update_result = update_or_clone_repository(repos, base_url, destination)
        pprint(update_result)


if __name__ == "__main__":
    update_repos()


