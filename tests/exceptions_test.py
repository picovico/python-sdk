import pytest

from picovico import exceptions

class TestPicovicoException:
    def test_raise_valid_exception(self, messages):
        server_error = messages.ERROR.SERVER
        auth_error = messages.ERROR.AUTH
        notfound_error = messages.ERROR.NOTFOUND
        some_error = messages.ERROR.RANDOM
        bad_error = messages.ERROR.BAD
        with pytest.raises(exceptions.PicovicoServerError) as excinfo:
            exceptions.raise_valid_exceptions(status_code=501, **server_error)
        assert excinfo.value.status >= 500
        with pytest.raises(exceptions.PicovicoNotFound) as excinfo:
            exceptions.raise_valid_exceptions(status_code=404, **notfound_error)
        assert excinfo.value.status == 404
        with pytest.raises(exceptions.PicovicoUnauthorized) as excinfo:
            exceptions.raise_valid_exceptions(status_code=401, **auth_error)
        assert excinfo.value.status == 401
        with pytest.raises(exceptions.PicovicoRequestError) as excinfo:
            exceptions.raise_valid_exceptions(status_code=400, **bad_error)
        assert excinfo.value.status == 400
        with pytest.raises(exceptions.PicovicoRequestError) as excinfo:
            exceptions.raise_valid_exceptions(status_code=415, **some_error)
        assert excinfo.value.status == 415
