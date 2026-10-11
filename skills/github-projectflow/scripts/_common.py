"""Shared helpers for the gh-projectflow scripts. Not an entry point."""
import json
import re
import subprocess
import sys
from pathlib import Path
from shutil import which

REQUIRED_STATUSES = ["Todo", "In Progress", "Done", "Blocked"]
STATUS_COLORS = {"Todo": "GRAY", "In Progress": "YELLOW", "Done": "GREEN", "Blocked": "RED"}
CONFIG_FILE = ".github/projectflow.json"


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd, check=True):
    """Run a command list, return CompletedProcess."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        die(f"{' '.join(cmd)}\n{r.stderr.strip()}")
    return r


def gh(*args, check=True):
    return run(["gh", *args], check=check)


def gh_json(*args, check=True):
    return json.loads(gh(*args, check=check).stdout)


def gh_text(*args, check=True):
    """Run gh and return stripped stdout (for plain-string output such as --jq)."""
    return gh(*args, check=check).stdout.strip()


def require_gh():
    if which("gh") is None:
        die("gh CLI is not installed. Install: https://cli.github.com")
    r = gh("auth", "status", check=False)
    if r.returncode != 0:
        die("gh is not logged in. Run: gh auth login")
    # Classic tokens list their scopes; Project v2 needs the write 'project' scope.
    m = re.search(r"Token scopes:(.*)", r.stdout + r.stderr)
    if m and "'project'" not in m.group(1):
        die("gh token is missing the 'project' scope. Run: gh auth refresh -s project")


def repo_info():
    """Repo info: owner, name, whether the owner is an organization."""
    info = gh_json("repo", "view", "--json", "owner,name,isInOrganization")
    return {
        "owner": info["owner"]["login"],
        "repo": info["name"],
        "is_org": info["isInOrganization"],
    }


def _scope(is_org):
    return "organization" if is_org else "user"


def _paginate_projects(var_decl, root_selector, root_key, variables):
    """Page through projectsV2 under a GraphQL root (user/organization/repository)."""
    q = ("query(" + var_decl + ",$after:String){ " + root_selector + "{ "
         "projectsV2(first:50, after:$after){ pageInfo{ hasNextPage endCursor } "
         "nodes{ number title shortDescription url } } } }")
    nodes, after = [], None
    while True:
        args = ["api", "graphql", "-f", f"query={q}"]
        for k, v in variables.items():
            args += ["-f", f"{k}={v}"]
        if after:
            args += ["-f", f"after={after}"]
        data = gh_json(*args)
        try:
            page = data["data"][root_key]["projectsV2"]
        except (KeyError, TypeError):
            break
        nodes += [n for n in page["nodes"] if n]
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return nodes


def list_repo_projects(owner, repo):
    """List the Project v2 boards linked to THIS repo (paginated)."""
    return _paginate_projects("$o:String!,$r:String!", "repository(owner:$o, name:$r)",
                              "repository", {"o": owner, "r": repo})


def get_project(owner, number, is_org):
    """Fetch a project + its Status field. Return (project_node, status_field_or_None)."""
    scope = _scope(is_org)
    q = ("query($o:String!,$n:Int!){ " + scope + "(login:$o){ projectV2(number:$n){ id url "
         "fields(first:50){ nodes{ __typename ... on ProjectV2SingleSelectField{ "
         "id name options{ id name color description } } } } } } }")
    data = gh_json("api", "graphql", "-f", f"query={q}", "-f", f"o={owner}", "-F", f"n={number}")
    try:
        proj = data["data"][scope]["projectV2"]
    except (KeyError, TypeError):
        proj = None
    if not proj:
        die(f"Project #{number} not found under {owner}.")
    status_field = None
    for f in proj["fields"]["nodes"]:
        if f.get("__typename") == "ProjectV2SingleSelectField" and f.get("name") == "Status":
            status_field = f
            break
    return proj, status_field


def _option_literal(name, color, description=""):
    return "{name:%s,color:%s,description:%s}" % (
        json.dumps(name), color, json.dumps(description))


def ensure_status_field(project_id, status_field):
    """Create the Status field, or add missing options while PRESERVING existing ones.

    updateProjectV2Field replaces the whole option list, so existing options
    must be re-sent together with the new ones.
    """
    if status_field:
        existing = status_field["options"]
        have = {o["name"] for o in existing}
        missing = [s for s in REQUIRED_STATUSES if s not in have]
        if not missing:
            return status_field
        opts = [_option_literal(o["name"], o.get("color") or "GRAY", o.get("description") or "")
                for o in existing]
        opts += [_option_literal(s, STATUS_COLORS[s]) for s in missing]
        q = ("mutation($f:ID!){ updateProjectV2Field(input:{fieldId:$f, "
             "singleSelectOptions:[" + ",".join(opts) + "]}){ projectV2Field{ "
             "... on ProjectV2SingleSelectField{ id name options{ id name color description } } } } }")
        data = gh_json("api", "graphql", "-f", f"query={q}", "-f", f"f={status_field['id']}")
        return data["data"]["updateProjectV2Field"]["projectV2Field"]
    opts = [_option_literal(s, STATUS_COLORS[s]) for s in REQUIRED_STATUSES]
    q = ("mutation($p:ID!){ createProjectV2Field(input:{projectId:$p, dataType:SINGLE_SELECT, "
         'name:"Status", singleSelectOptions:[' + ",".join(opts) + "]}){ projectV2Field{ "
         "... on ProjectV2SingleSelectField{ id name options{ id name color description } } } } }")
    data = gh_json("api", "graphql", "-f", f"query={q}", "-f", f"p={project_id}")
    return data["data"]["createProjectV2Field"]["projectV2Field"]


def repo_root():
    """Repo root directory (git toplevel), falling back to cwd."""
    r = run(["git", "rev-parse", "--show-toplevel"], check=False)
    return r.stdout.strip() if r.returncode == 0 else "."


def load_config():
    """Read .github/projectflow.json from the repo root. Return dict or None."""
    path = Path(repo_root()) / CONFIG_FILE
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_config(data):
    """Write .github/projectflow.json under the repo root. Return the path."""
    path = Path(repo_root()) / CONFIG_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
