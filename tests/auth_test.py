import requests, unittest, json
from lib import config, urls
from lib.auth.session import PicovicoSession
from lib.exceptions import DataNotFound, PicovicoAPIResponseException
from ddt import ddt, data, unpack
from lib.api import PicovicoAPIRequest


@ddt
class PicovicoSessionTest(unittest.TestCase):

    @data(
            (config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET, False, False),
            ('277a723c32b3578a549e5aaaf8e79c7f7f3a64a91e12e1e219c6c50db4496a9300', 'e61b883b2a0109763cb0289f751df8289c6baa3fcab98bf2842f3345a70bc7b400', True, False),
            #('277a723c32b3578a549e5aaaf8e79c7f7f3a64a91e12e1e219c6c50db4496a9300', 'e61b883b2a0109763cb0289f751df8289c6baa3fcab98bf2842f3345a70bc7b400', False, True)
        )
    @unpack
    def test_authenticate(self, app_id, app_secret, expectedPicovicoAPIResponseException, expectedDataNotFound):
        '''
            Picovico Test: Authentication test for picovico
        '''
        self.session = PicovicoSession(app_id, app_secret)

        if expectedPicovicoAPIResponseException:
            self.assertRaises(PicovicoAPIResponseException, lambda: self.session.authenticate())
            return 

        # if expectedDataNotFound:
           
        #     # #self.assertRaises(PicovicoAPIResponseException, lambda: PicovicoAPIRequest.sdk_response())
        #     self.assertRaises(DataNotFound, lambda: self.session.authenticate())
        #     return 

        authenticate = self.session.authenticate()
        self.assertTrue(authenticate)

    def test_login(self):
        pass


if __name__ == '__main__':
    unittest.main()

