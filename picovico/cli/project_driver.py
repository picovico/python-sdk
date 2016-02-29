import six

from . import utils as pv_utility
from . import profile_utils
from .. import project as pv_project

def get_project_command():
    subcommands = ('begin', 'define', 'render', 'preview', 'discard', 'save')
    project_components = ('name', 'quality', 'style', 'photo', 'music', 'credits')    
    subcommands = {
        'begin': project_components[:3],
        'define': project_components,
        'render': None,
        'preview': None,
        'discard': None,
        'save': None,
    }
    
    command = {
        'command': 'project',
        'options': None,
        'subcommands': [],
        'sub_title': 'project commands',
        'sub_dest': 'project',
        'sub_extras': {}
    }
    for k, v in six.iteritems(subcommands):
        com_ = {'command': k}
        if v:
            com_['options'] = [{'name': '-{}'.format(l), 'required': False} for l in v]
            #com_['group_name'] = 'project {} group'.format(k)
        com = profile_utils._create_namedtuple('SubCommand', com_)
        command['subcommands'].append(com)
    return command

def get_project_cli_commands():
    command = get_project_command()
    return (profile_utils._create_namedtuple('CliCommandsConfig', command),)

#def map_project_command():
    #mappings = {
        #'begin': 'begin_video',
        #'render': 'render_video',
        #'preview': 'preview_video',
        #'save': 'save_video',
        #'discard': 'discard_video',
        #'define': 'define_video'
    #}
    
def project_cli_action(profile, **kwargs):
    project_action = kwargs.get('project')
    api = pv_utility.prepare_api_object(profile_name=profile, session=True)
    action = getattr(api.project, project_action)
    action(**kwargs)
