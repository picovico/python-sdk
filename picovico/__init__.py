from picovico.session import PicovicoSessionMixin
from picovico import urls as pv_urls
from picovico import baserequest as pv_request

class PicovicoAPI(PicovicoSessionMixin, pv_request.PicovicoRequest):
    def __init__(self, app_id, device_id=None, app_secret=None):
        super(PicovicoAPI, self).__init__(app_id, device_id=device_id, app_secret=app_secret)

    def authenticated_api(self, method='get', url=None, params=None, headers=None):
        self.request_args = self.get_request_args(method, req_data=params)
        auth_headers = self.auth_headers
        if headers is not None:
            if not auth_headers:
                auth_headers = headers
            else:
                auth_headers.update(headers)
        self.headers = auth_headers
        return self._respond(url)
        
    def anonymous_api(self, method='get', url=None, params=None, headers=None):
        self.request_args = self.get_request_args(method, req_data=params)
        self.header = headers
        return self._respond(url)
    
    def authenticate(self, app_secret=None):
        """ API authentication workflow.

        This is application secret based authentication.
        This also sets access headers and readies components.

        Args:
            app_secret(str): Application Secret provided by Picovico.
        """
        if app_secret is not None:
            self._set_app_secret(app_secret)
        assert self.app_secret, 'App secret provided by picovico is required'
        data={
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'device_id': self.device_id
        }
        self.headers = {'X-PV-Meta-App': self.app_id}
        response = self.post(path=pv_urls.PICOVICO_APP, post_data=data)
        self.set_access_tokens(access_key=response.get('access_key'),
                access_token=response.get('access_token'))


    def text_slide(self, title='', body=''):
        return {
            "name": 'text',
            "data": {
                "title": title,
                "text": body
            }
        }
    
    def image_slide(self, image_url, image_id, caption=''):
        d = {
            "name": 'image',
            "data": {
                "caption": caption
            }
        }
        if image_url and not image_id:
            d['url'] = image_url
        elif not image_url and image_id:
            d['id'] = image_id
        return d
