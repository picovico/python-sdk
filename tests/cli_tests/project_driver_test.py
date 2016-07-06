import itertools
import pytest
import six
from picovico import PicovicoAPI
from picovico.cli import project_driver as pv_project_driver
from picovico import project as pv_project

def create_comb_com(ch):
    for l in ch:
        d = l[0].copy() 
        if isinstance(l[1], tuple):
            d.update(dict(l[1]))
        else:
            d.update(l[1])
        yield d

def project_arg(command, *args):
    # b = {'project': command}
    yield command
    comb_arg = six.moves.zip(args, args)
    i = 1
    c = []
    while i <= len(list(comb_arg)):
        c.append(itertools.combinations(comb_arg, i))
        i += 1
    ch = itertools.chain(*[itertools.product((command,), cc) for cc in c])
    # , itertools.product((b,), three_comb), itertools.product((b,), two_comb), itertools.product((b,), four_comb))
    for g in create_comb_com(ch):
        yield g

def project_begin_arg():
    return project_arg({'project': 'begin'}, 'style', 'name', 'quality', 'privacy')

def final_yield(comand, other):
    for b in itertools.product(comand, other):
        d = b[0].copy()
        d.update(b[1])
        yield d

def for_photo_music_one(comp_arg, comp, com):
    # combine_arg = comp_arg[:2]
    if comp == 'photo':
        comp_arg += ('caption',)
    # for c in comp_arg:
        # if c not in combine_arg:
            # if comp == 'photo':
                # cc = get_comp(comp, (c, 'caption'))
            # else:
                # cc = get_comp(comp, c)
        # else:
    cc = get_comp(comp, *comp_arg)
    return final_yield(com, cc)

def for_photo_music_url(comp_arg, comp,com):
    combine_arg = comp_arg[:2]
    return for_photo_music_one(combine_arg, comp, com)

def for_photo_music_id(comp_arg, comp,com):
    combine_arg = comp_arg[2:3]
    return for_photo_music_one(combine_arg, comp, com)

def for_photo_music_filename(comp_arg, comp,com):
    combine_arg = comp_arg[3:4]
    return for_photo_music_one(combine_arg, comp, com)

# def for_photo_music(comp_arg, comp, com):
    # for ss in for_photo_music_id(comp_arg,comp,com):
        # yield ss
    # for ss in for_photo_music_filename(comp_arg,comp,com):
        # yield ss
    
    
def get_comp(c, *args):
    return project_arg({'component': c}.copy(), *args)

def project_define_arg(comp, what=None):
    comm = {'project': 'define'}
    com = project_arg(comm, 'style', 'name', 'quality', 'privacy')
    component_arg = pv_project_driver.project_components.get(comp)
    if comp in ('music' and 'photo'):
        to_get = {
            'id': for_photo_music_id,
            'filename': for_photo_music_filename,
            'url': for_photo_music_url
        }.get(what, for_photo_music_id)
        return to_get(component_arg, comp, com)
    else:
        cc = get_comp(comp, *component_arg)
        return final_yield(com, cc)

def check_define_arg(pobj, parg):
    meths = []
    for k in parg:
        if k != 'project':
            meths =  pv_project_driver.prepare_method_args(**parg)
    for m in meths:
        getattr(pobj, m.METHOD).assert_called_with(**m.ARGUMENTS)
    
class TestProjectDriver:
    @pytest.mark.parametrize('video_id,video_data', itertools.product((None, 'vid'), (None, {'vid': True})))
    def test_get_project_api(self, mocker, video_id, video_data):
        mapi = mocker.Mock(spec=PicovicoAPI)
        mapi.project = mocker.Mock(return_value='Project')
        mocker.patch('picovico.cli.project_driver.pv_cli_utils.prepare_api_object', return_value=mapi)
        mocker.patch('picovico.cli.project_driver.file_utils.read_from_project_file', return_value=video_data)
        mpv = mocker.patch('picovico.cli.project_driver.populate_vdd_to_project')
        pv_project_driver.get_project_api('Hello', video=video_id)
        if not video_data:
            mpv.assert_not_called()
        else:
            mpv.assert_called_with(mapi.project, True)
        
    
    def test_prepare_text_method_args(self):
        with pytest.raises(AssertionError):
            pv_project_driver.prepare_text_method_args()
        tb = pv_project_driver.prepare_text_method_args(title='Hello')
        assert tb.METHOD == 'add_text'    
        assert tb.ARGUMENTS and tb.ARGUMENTS['title'] == 'Hello' 
        assert not all(tb.ARGUMENTS.values())
        tb = pv_project_driver.prepare_text_method_args(title='Hello', body='There')
        assert all(tb.ARGUMENTS.values())
        
    @pytest.mark.parametrize('keyarg', ({'id': 'some_id'}, {'filename': 'some_file'}, {'url': 'some_url'}))
    def test_prepare_photo_music_method_args(self, keyarg):
        pma = pv_project_driver.prepare_photo_method_args(**keyarg)
        meth_name = 'add_photo'
        if 'url' in keyarg or 'filename' in keyarg:
            meth_name = 'add_photo_url' if 'url' in keyarg else 'add_photo_file'
        assert pma.METHOD == meth_name
        keyarg.update(caption='caption')
        pma = pv_project_driver.prepare_photo_method_args(**keyarg)
        assert pma.ARGUMENTS['caption'] == 'caption'
        if 'id' in keyarg:
            keyarg.update(url='some_url')
            with pytest.raises(AssertionError):
                pv_project_driver._prepare_common_args(**keyarg)

    @pytest.mark.parametrize('comp', pv_project.Vdd._fields)
    def test_prepare_common_method_with_args(self, comp):
        assert not pv_project_driver.prepare_common_methods_with_args()
        arg = {comp: '{}_value'.format(comp)}
        tpc = pv_project_driver.prepare_common_methods_with_args(**arg)
        if comp in ('assets', 'credits'):
            assert not tpc
        
    @pytest.mark.parametrize('parg', project_begin_arg())
    def test_project_begin(self, parg, mocker):
        gpa = mocker.patch('picovico.cli.project_driver.get_project_api')
        mocker.patch('picovico.cli.project_driver.save_project_data')
        mapi = mocker.Mock(spec=PicovicoAPI)
        gpa.return_value = mapi
        s = pv_project_driver.project_cli_action(**parg)
        mapi.project.begin.assert_called_once_with(parg.get('name', None))
        for k in parg:
            if k != 'project':
                d = {'value': parg[k]}
                meth = getattr(mapi.project, 'set_{}'.format(k))
                meth.assert_called_with(**d)
    
    @pytest.mark.parametrize('parg', project_define_arg('text'))
    def test_project_define_text(self, parg, mocker):
        gpa = mocker.patch('picovico.cli.project_driver.get_project_api')
        mocker.patch('picovico.cli.project_driver.save_project_data')
        mapi = mocker.Mock(spec=PicovicoAPI)
        gpa.return_value = mapi
        mwarn = mocker.patch('picovico.cli.project_driver.prompt.show_warning')
        if 'component' in parg and not any(k in parg and parg[k] for k in ('title', 'body')):
            with pytest.raises(AssertionError):
                pv_project_driver.project_cli_action(**parg)
                assert mwarn.called
        else:
            s = pv_project_driver.project_cli_action(**parg)
            check_define_arg(mapi.project, parg)

    @pytest.mark.parametrize('parg', itertools.chain(project_define_arg('photo'), project_define_arg('photo', 'filename'), project_define_arg('photo', 'url')))
    def test_project_define_photo(self, parg, mocker):
        gpa = mocker.patch('picovico.cli.project_driver.get_project_api')
        mocker.patch('picovico.cli.project_driver.save_project_data')
        mapi = mocker.Mock(spec=PicovicoAPI)
        gpa.return_value = mapi
        mwarn = mocker.patch('picovico.cli.project_driver.prompt.show_warning')
        if 'component' in parg and not any(k in parg and parg[k] for k in ('url', 'filename', 'id')):
            with pytest.raises(AssertionError):
                pv_project_driver.project_cli_action(**parg)
                assert mwarn.called
        else:
            s = pv_project_driver.project_cli_action(**parg)
            check_define_arg(mapi.project, parg)
        #for k in parg:
            #if k != 'project':
                #d = {'value': parg[k]}
                #meth = getattr(mapi.project, 'set_{}'.format(k))
                #meth.assert_called_with(**d)
