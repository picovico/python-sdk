import six
import pytest

from picovico.cli import driver
from picovico.cli import prompt
from picovico.cli import profile_utils

input_args = ('Enter Application Id provided: ',
            'Enter Device Identifier->[default:{}]: '.format(prompt.DEFAULT_DEVICE_ID),
            'Enter Application Secret: ',
            'Enter Picovico Username: ',
            'Enter Picovico Password: ')
return_args = ('MY_APP_ID', None, 'MY_APP_SECRET',
                    'MY_USERNAME', 'MY_PASSWORD')
return_value = dict(six.moves.zip(input_args, return_args))

class TestCliActions:
    def test_configure(self, mocker):
        profiles = (profile_utils.DEFAULT_PROFILE_NAME, 'NEW')
        mni = mocker.patch('picovico.cli.prompt.configure_prompt')
        mni.return_value = (return_args[0], prompt.DEFAULT_DEVICE_ID)
        mni.side_effect = AssertionError('Application ID is required.')
        with pytest.raises(AssertionError):
            driver.configure()
        mni.side_effect = None
        call_args = dict(zip(('APP_ID', 'DEVICE_ID'), (mni.return_value)))
        mgap = mocker.patch('picovico.cli.profile_utils.get_all_profiles')
        mgap.return_value = (profiles[0],)
        msc = mocker.patch('picovico.cli.profile_utils.set_profile')
        msc.return_value = True
        driver.configure()
        msc.assert_called_with(call_args, profiles[0])
        mgap.return_value = profiles
        driver.configure(profiles[1])
        msc.assert_called_with(call_args, profiles[1])
        mli = mocker.patch('picovico.cli.prompt.configure_login_info')
        mli.return_value = return_args[3:]
        conf_info = driver.configure(login=True)
        call_args.update(dict(zip(('USERNAME', 'PASSWORD'), mli.return_value)))
        msc.assert_called_with(call_args, profiles[0])
        msi = mocker.patch('picovico.cli.prompt.configure_secret_info')
        msi.return_value = return_args[2]
        conf_info = driver.configure(authenticate=True)
        with pytest.raises(AssertionError):
            msc.assert_called_with(call_args, profiles[0])
        call_args.pop('USERNAME')
        call_args.pop('PASSWORD')
        call_args.update(APP_SECRET=msi.return_value)
        msc.assert_called_with(call_args, profiles[0])
