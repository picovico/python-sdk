import pytest

from picovico import exceptions

class TestPicovicoException:
    def test_raise_valid_exception(self, pv_messages):
        server_error = pv_messages.ERROR.SERVER
        auth_error = pv_messages.ERROR.AUTH
        notfound_error = pv_messages.ERROR.NOTFOUND
        some_error = pv_messages.ERROR.RANDOM
        bad_error = pv_messages.ERROR.BAD
        with pytest.raises(exceptions.PicovicoServerError) as excinfo:
            exceptions.raise_valid_error(status_code=501, **server_error)
        assert excinfo.value.status >= 500
        with pytest.raises(exceptions.PicovicoNotFound) as excinfo:
            exceptions.raise_valid_error(status_code=404, **notfound_error)
        assert excinfo.value.status == 404
        with pytest.raises(exceptions.PicovicoUnauthorized) as excinfo:
            exceptions.raise_valid_error(status_code=401, **auth_error)
        assert excinfo.value.status == 401
        with pytest.raises(exceptions.PicovicoRequestError) as excinfo:
            exceptions.raise_valid_error(status_code=400, **bad_error)
        assert excinfo.value.status == 400
        with pytest.raises(exceptions.PicovicoRequestError) as excinfo:
            exceptions.raise_valid_error(status_code=415, **some_error)
        assert excinfo.value.status == 415

    def test_error_code(self):
        def check_assertion(exc, *args):
            with pytest.raises(AssertionError):
                exc(*args)
        check_assertion(exceptions.PicovicoServerError, 400)
        check_assertion(exceptions.PicovicoServerError, 200)
        check_assertion(exceptions.PicovicoServerError, 300)
        check_assertion(exceptions.PicovicoRequestError, 300)
        check_assertion(exceptions.PicovicoRequestError, 200)
        check_assertion(exceptions.PicovicoRequestError, 500)
