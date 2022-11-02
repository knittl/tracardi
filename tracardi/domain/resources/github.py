import re
from typing import Optional

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.networks import AnyHttpUrl

GITHUB_DEFAULT_API_URL = 'https://api.github.com'


def _is_valid_github_identifier(value: str):
    regex = re.compile('^[a-zA-Z0-9-]+$')
    for part in value.split('-'):
        if not regex.match(part):
            return False
    return True


def _validate(value: str, error_message):
    if not _is_valid_github_identifier(value):
        raise ValueError(error_message)
    return value


class GitHub(BaseModel):
    api_url: AnyHttpUrl
    personal_access_token: Optional[str] = None
    owner: str
    repo: str

    @validator("api_url")
    def normalize_url(cls, value):
        return value.rstrip('/')

    @validator("owner")
    def owner_must_be_valid(cls, value):
        return _validate(value, 'Invalid GitHub owner: ' + value)

    @validator("repo")
    def repo_must_be_valid(cls, value):
        return _validate(value, 'Invalid GitHub repo: ' + value)

    def get_repo_url(self):
        return f'{self.api_url}/repos/{self.owner}/{self.repo}'
