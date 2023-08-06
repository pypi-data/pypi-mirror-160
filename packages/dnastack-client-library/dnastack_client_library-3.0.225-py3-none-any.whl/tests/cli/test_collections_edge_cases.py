from dnastack.common.environments import flag, env
from tests.cli.auth_utils import handle_device_code_flow
from tests.cli.base import CliTestCase


class TestEndToEnd(CliTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.prepare_for_device_code_flow(email_env_var_name='E2E_STAGING_AUTH_DEVICE_CODE_TEST_EMAIL',
                                          token_env_var_name='E2E_STAGING_AUTH_DEVICE_CODE_TEST_TOKEN')

    def test_182678656(self):
        """
        https://www.pivotaltracker.com/story/show/182678656

        When using the "dnastack collections query" command after initializing with the "dnastack use" command,
        there should not be an additional auth prompt if the target per-collection data-connect endpoint is registered.
        """

        handle_device_code_flow(['python', '-m', 'dnastack', 'use', 'explorer.alpha.dnastack.com'],
                                self._email,
                                self._token)
        self.simple_invoke('collections',
                           'query',
                           '-c', 'explorer-staging-controlled-collection',
                           'SELECT 1')
