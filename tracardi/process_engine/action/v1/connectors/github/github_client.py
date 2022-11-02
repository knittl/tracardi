import aiohttp

from tracardi.domain.resources.github import GitHub
from tracardi.process_engine.action.v1.connectors.github.model.config import Configuration
from tracardi.service.tracardi_http_client import HttpClient


def _normalize_issue_id(issue_id):
    return issue_id.lstrip('#')


class GitHubClient:
    resource: GitHub
    config: Configuration

    def __init__(self, resource, config, console):
        self.resource = resource
        self.config = config
        self.console = console

    def _get_auth_header(self):
        return 'Bearer ' + self.resource.personal_access_token

    def _make_headers(self):
        return {
            'accept': 'application/vnd.github+json',
            'authorization': self._get_auth_header()
        }

    async def list_issues(self):
        url = f'{self.resource.get_repo_url()}/issues'
        self.console.log(f'Getting issues from {url}')

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        async with HttpClient(2, 200, timeout=timeout) as client:
            async with client.request(
                    method='GET',
                    url=url,
                    headers=self._make_headers(),
            ) as response:
                return {
                    'status': response.status,
                    'body': await response.json()
                }

    async def get_issue(self, issue_id):
        issue_id = _normalize_issue_id(issue_id)
        url = f'{self.resource.get_repo_url()}/issues/{issue_id}'
        self.console.log(f'Getting issue details from {url}')

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        async with HttpClient(2, 200, timeout=timeout) as client:
            async with client.request(
                    method='GET',
                    url=url,
                    headers=self._make_headers(),
            ) as response:
                return {
                    'status': response.status,
                    'body': await response.json()
                }
