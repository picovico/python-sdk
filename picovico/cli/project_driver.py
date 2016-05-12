import itertools

import six

from picovico.cli import utils as pv_cli_utils
from picovico.cli import profile_utils
from picovico.cli import file_utils
from picovico.cli import prompt
from picovico.cli import decorators as pv_cli_decorators
from picovico import project as pv_project

project_components = {
    'text': ('title', 'body'),
    'photo': ('url', 'thumb', 'id', 'filename'),
    'music': ('url', 'preview', 'id', 'filename'),
    'credit': ('content',)
}    
define_components = [a for a in pv_project.Vdd._fields if a not in ('assets', 'credits')]
subcommands = {
    'begin': define_components,
    'define': itertools.chain(define_components, ('video',)),
    'render': ('video',),
    'preview': ('video',),
    'discard': ('video',),
    'save': ('video',),
    'close': None,
}

def get_project_command():
    command = {
        'command': 'project',
        'options': None,
        'subcommands': [],
        'sub_title': 'project commands',
        'sub_dest': 'project',
        'sub_extras': {}
    }
    define_subcommand = []
    for comp, val in project_components.items():
        com_ = {'command': comp}
        if val:
            com_['options'] = [{'name': '-{}'.format(l), 'required': False} for l in val]
        com = profile_utils._create_namedtuple('SubCommand', com_)
        define_subcommand.append(com)
    for k, v in six.iteritems(subcommands):
        com_ = {'command': k}
        if v:
            com_['options'] = [{'name': '-{}'.format(l), 'required': False} for l in v]
            #com_['group_name'] = 'project {} group'.format(k)
        if k == 'define':
            com_.update(sub_title='define_components')
            com_.update(sub_dest='component')
            com_.update(sub_extras={})
            com_.update(subcommands=define_subcommand)
        com = profile_utils._create_namedtuple('SubCommand', com_)
        command['subcommands'].append(com)
    return command

def get_project_cli_commands():
    command = get_project_command()
    return (profile_utils._create_namedtuple('CliCommandsConfig', command),)

def _prepare_method_args(meth_name, **kwargs):
    val = {'method': meth_name}
    val.update(arguments=kwargs)
    return profile_utils._create_namedtuple('MethodArgs', val)

def _prepare_text_args(**kwargs):
    title = kwargs.get('title', None)
    body = kwargs.get('body', None)
    assert any((title, body)), 'Either title or body is required.'
    return title, body
    
def prepare_text_method_args(**kwargs):
    title, body = _prepare_text_args(**kwargs)
    return _prepare_method_args('add_text', title=title, body=body)

def _prepare_common_args(**kwargs):
    _id = kwargs.get('id')
    _file = kwargs.get('filename')
    _url = kwargs.get('url')
    checks = iter((_id, _file, _url))
    assert any(checks) and not any(checks), 'Ensure only one of id, file or url is given.'
    return _id, _file, _url 

def prepare_photo_method_args(**kwargs):
    photo_id, photo_file, photo_url = _prepare_common_args(**kwargs)
    photo_thumb = kwargs.get('thumb')
    photo_caption = kwargs.get('caption')
    meth_name = 'add_photo'
    if photo_url:
        meth_name += '_url'
        return _prepare_method_args(meth_name, url=photo_url, thumbnail=photo_thumb, caption=photo_caption)
    elif photo_file:
        meth_name += '_file'
        return _prepare_method_args(meth_name, filename=photo_file, caption=photo_caption)
    elif photo_id:
        return _prepare_method_args(meth_name, photo_id=photo_id, caption=photo_caption)
    
def prepare_music_method_args(**kwargs):
    music_id, music_file, music_url = _prepare_common_args(**kwargs)
    music_preview = kwargs.get('preview')
    meth_name = 'add_music'
    if music_url:
        meth_name += '_url'
        return _prepare_method_args(meth_name, url=music_url, preview=music_preview)
    elif music_file:
        meth_name += '_file'
        return _prepare_method_args(meth_name, filename=music_file)
    elif music_id:
        return _prepare_method_args(meth_name, music_id=music_id)
    #return ('add_music', music_id=music_id, body=body)
def _prepare_credit_args(**kwargs):
    content = kwargs.get('content')
    assert content, 'Credit content should be "name,value" format.'
    content = content.split(',')
    assert len(content) == 2 and all(content), 'Make sure credit content is "name,value" format.'
    return content[0], content[1]

def prepare_credit_method_args(**kwargs):
    name, value = _prepare_credit_args(**kwargs)
    return _prepare_method_args('add_credit', name=name, value=value)

def prepare_common_methods_with_args(**kwargs):
    methods = []
    for comp in define_components:
        val = kwargs.get(comp, None)
        if val:
            meth_name = 'set_{}'.format(comp)
            methods.append(_prepare_method_args(meth_name, value=val))
    return methods

def prepare_method_args(**kwargs):
    component_methods = {
        'music': prepare_music_method_args,
        'photo': prepare_photo_method_args,
        'text': prepare_text_method_args,
        'credit': prepare_credit_method_args
    }
    meth_args = prepare_common_methods_with_args(**kwargs)
    component = kwargs.get('component', None)
    if component and component in component_methods:
        meth_args.append(component_methods.get(component)(**kwargs))
    return meth_args

def _check_assertion(func, **kwargs):
    try:
        return func(**kwargs)
    except AssertionError as e:
        prompt.show_warning(e.args[0], True)


def check_photo_music_component(**kwargs):
    _check_assertion(_prepare_common_args, **kwargs)

def check_credit_component(**kwargs):
    _check_assertion(_prepare_credit_args, **kwargs)

def check_text_component(**kwargs):
    _check_assertion(_prepare_text_args, **kwargs)

def check_component_args(**kwargs):
    component = kwargs.get('component')
    comp_map = {
        'text': check_text_component,
        'music': check_photo_music_component,
        'photo': check_photo_music_component,
        'credit': check_credit_component
    }
    comp_func = comp_map.get(component, None)
    if comp_func:
        comp_func(**kwargs)
    
def populate_vdd_to_project(project_obj, vdd):
    assert vdd and isinstance(vdd, dict), 'Video Data object should be dictionary.'
    assets = vdd.pop('assets')
    credits = vdd.pop('credits')
    if assets:
        project_obj._add_assets(assets)
    if credits:
        project_obj._add_credits(credits)
    for key in vdd:
        add_attr = getattr(project_obj, 'add_{}'.format(key), None)
        attr = getattr(project_obj, 'set_{}'.format(key), add_attr) 
        if attr and vdd[key]:
            arg = vdd[key]
            if 'value' in arg and arg['value']:
                attr(**arg)

def get_project_api(profile, **kwargs):
    api = pv_cli_utils.prepare_api_object(profile_name=profile, session=True)
    video_id = kwargs.get('video', None)
    project_data = file_utils.read_from_project_file() or {}
    if not video_id:
        video_id = ''.join(project_data.keys()) if len(project_data) == 1 else None
    data = project_data.get(video_id, None)
    api.project.video = video_id
    if data:
        populate_vdd_to_project(api.project, data)
    return api

def project_save_format(project):
    project_format = {project.video: {}}
    for attr in pv_project.Vdd._fields:
        inside = {}
        if attr not in ('credits', 'assets'):
            inside[attr] = {'value': getattr(project.vdd, attr)}
        project_format[project.video].update(inside)
    project_format[project.video].update(credits=project.vdd.credits)
    project_format[project.video].update(assets=project.vdd.assets)
    return project_format

def save_project_data(project):
    new_data = project_save_format(project)
    file_utils.write_to_project_file(new_data)

def close():
    file_utils.delete_project_file()

@pv_cli_decorators.pv_cli_check_project_begin
def project_cli_action(profile=None, **kwargs):
    project_action = kwargs.get('project')
    methods = []
    if project_action == 'close':
        return None
    api = get_project_api(profile, **kwargs)
    if project_action in ('define', 'begin'):
        if project_action == 'define':
            check_component_args(**kwargs)
        else:
            api.project.begin(kwargs.get('name', None))
        methods = prepare_method_args(**kwargs)
    else:
        getattr(api.project, project_action)()
    for act in methods:
        action = getattr(api.project, act.METHOD)
        action(**act.ARGUMENTS)
    save_project_data(api.project)
    #action = getattr(api.project, project_action)
    #arguments = prepare_from_kwargs(**kwargs)
    #action(**kwargs)

def finalize_project_action(**kwargs):
    project_data = file_utils.read_from_project_file() or {}
    video_id = ''.join(project_data.keys()) if len(project_data) == 1 else None
    act = kwargs.get('project')
    if act.startswith(('render', 'close')):
        close()
    prompt.show_project_action_success(act, video_id, kwargs.get('profile_name'))
        
