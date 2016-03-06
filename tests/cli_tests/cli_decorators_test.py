import pytest

from picovico.cli import prompt, decorators as cli_dec
from picovico.cli.profile_utils import DEFAULT_PROFILE_NAME

class TestPVCLIDecorators:
    @pytest.mark.parametrize('action,profile', [(k,v) for k in ('configure', 'noconfigure') for v in (DEFAULT_PROFILE_NAME, 'NO_DEFAULT')])
    def test_check_configure(self, mocker, action, profile):
        mock_func = mocker.MagicMock()
        mock_func.__name__ = 'mocked_func'
        config_check = cli_dec.pv_cli_check_configure(mock_func)
        argument = {
            'action': action
        }
        if profile != DEFAULT_PROFILE_NAME:
            argument['profile'] = profile
        mock_get_profile = mocker.patch('picovico.cli.decorators.profile_utils.get_profile')
        mock_get_profile.return_value = True
        msw = mocker.patch('picovico.cli.decorators.prompt.show_warning')
        config_check(**argument)
        assert not msw.called
        mock_func.assert_called_with(action, profile)
        if action != 'configure':
            mock_get_profile.side_effect = AssertionError
            config_check(**argument)
            msw.assert_called_with(prompt.NO_PROFILE_MSG, stop=True)
