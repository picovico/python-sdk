import pytest

from picovico import exceptions as pv_exceptions
from picovico import decorators as pv_decorator
from picovico.components import PicovicoStyle

def mock_objs(mocker):
    check = mocker.MagicMock()
    check_func = mocker.MagicMock()
    check_func.__name__ = 'mocked_func'
    return check, check_func

class TestPicovicoDecorators:
    def test_not_implemented(self, pv_mocks):
        check, check_func = mock_objs(pv_mocks.OBJ)
        check.component = 'style'
        check_decorator = pv_decorator.pv_not_implemented(('video',))
        with pytest.raises(NotImplementedError):
            check_decorator(check_func)(check)
        check_decorator = pv_decorator.pv_not_implemented(('style',))
        check_decorator(check_func)(check)

    def test_project_check_begin(self, pv_mocks):
        check, check_func = mock_objs(pv_mocks.OBJ)
        check.video = False
        check_decorator = pv_decorator.pv_project_check_begin(check_func)
        with pytest.raises(pv_exceptions.PicovicoProjectNotAllowed):
            check_decorator(check)
        check.video = True
        check_decorator(check)
        

    def test_auth_required(self, pv_mocks):
        mocker = pv_mocks.OBJ
        check, check_func = mock_objs(mocker)
        check.is_authorized.return_value = True
        
