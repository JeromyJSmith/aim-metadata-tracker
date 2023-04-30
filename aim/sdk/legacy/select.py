from typing import Optional

from aim.sdk.repo import Repo
from aim.sdk.legacy.deprecation_warning import deprecated


@deprecated
def select_metrics(search_statement: str, repo_path: Optional[str] = None):
    repo = Repo.default_repo() if repo_path is None else Repo.from_path(repo_path)
    return repo.query_metrics(search_statement) if repo else None


@deprecated
def select_runs(expression: Optional[str] = None, repo_path: Optional[str] = None):
    repo = Repo.default_repo() if repo_path is None else Repo.from_path(repo_path)
    return repo.query_runs(expression) if repo else None
