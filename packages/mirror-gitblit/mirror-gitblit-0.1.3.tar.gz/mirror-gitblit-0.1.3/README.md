# Scripts to make backup of gitblit

This package requires at least python 3.6.

## Configuration file

A configuration-file is needed for listing and cloning repositories of a
gitblit server. Below is a template of a configuration file. Value of
parameters are written in `{` and `}`.

```toml
# Content of configuration.toml

# [authentication against http interface]
# username
user = "{user}"

# password
password = "your-secret-method"

# [server information]
# Web-interface base url. This is used to get information about repositories
source_web_url = "https://{host}.{domain}.{tld}/gitblit"

# The Base-URL to Remote-Server for git. This is used to construct the
# first argument of git clone
source_base_url = "ssh://{user}@{host}.{domain}.{tld}:{port}"

# [output]
# where to save the list of repositories
repositories_json = "/tmp/repos.json"

# where to clone repositories
backup_dir = "/tmp/backup"

# only clone these repos; clone all repositories in `repositories_json` 
# if this parameter is empty or does not exist
included_repos = [
    "awesome-project.git",
    "games/nicegame.git",
    "latex/codeanatomy.git"
]
```

## List all Repositories: `list-gitblit-repos configuration.toml`

The command `list-gitblit-repos` lists all repositories of Server configured by
variable `[source_web_url]`. It expects one argument, which points to a configuration
file. Result is the file named in `[repositories_json]`.

As an alternative, once can also use a browser to create a List of repositories:

1. login with an (admin) account in Gitblit
2. Open a Browser Console on the same session
3. In the Console Prompt once can use the function `fetch()` like

```javascript
var repos = {}; /* create a global variable, just for experiment */
fetch("https://{host}.{domain}.{tld}/gitblit/rpc/?req=LIST_REPOSITORIES")
  .then(result => result.json()).then(json => repos = json)
```
   to get list of repository.

4. The list of repository can be found in network-Tab



## Clone all Repository: `clone-gitblit-repos configuration.toml`


1. Configuration parameters in `configuration.toml` can be reused or modified.
2. Call `clone-gitblit-repos configuration.toml`

## Restore repository to new server
 
Subject of change!

