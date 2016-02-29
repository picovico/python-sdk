from . import profile_utils
from . import prompt



def prepare_api_object(profile_name, session=False):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    profile = profile_utils.get_profile(profile_name, info=True)
    api = PicovicoAPI(profile.APP_ID, profile.DEVICE_ID)
    if session:
        sess = profile_utils.get_session_info()
        if sess and sess.PROFILE == profile.NAME:
            api.set_access_tokens(sess.access_key, sess.ACCESS_TOKEN)
        else:
            auth_names = profile_utils.get_auth_names(profile.NAME)
            if not auth_names:
                prompt.show_no_session(profile.NAME)
            action = {
                profile_utils.LOGIN_INFO: 'login',
                profile_utils.AUTHENTICATE_INFO: 'authenticate',
            }.get(auth_names, None)
            if not all(getattr(profile, k, None) for k in auth_names):
                prompt.show_no_session(profile.NAME)
            else:
                arguments = {k.lower(): getattr(profile, k) for k in auth_names}
                api = auth_action(action, profile, **arguments)
    return api
    
def auth_action(funcname, profile_name, **kwargs):
    profile_name = getattr(profile_name, 'NAME', profile_name)
    api = prepare_api_object(profile_name)
    getattr(api, funcname)(**kwargs)
    if api.is_authorized():
        data = {
            'ACCESS_KEY': api.access_key,
            'ACCESS_TOKEN': api.access_token,
            'PROFILE': profile_name
        }
        file_utils.write_to_session_file(data)
    return api
    

