import requests, sys
import unittest
import picovico
from lib import config

class PicovicoVideoTest(unittest.TestCase):

    def setUp(self):
        '''
            Picovico Test: Set up the app_id and app_secret and authenticate.
        '''
        self.app = picovico.Picovico(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
        authenticate = self.app.authenticate()
        self.assertTrue('access_key' and 'access_token' in authenticate.keys())

    # def test_begin(self):
    #   '''
    #       Picovico Test: Begin a project with 
    #   '''
    #   response = self.app.begin("My cool video")
    #   print(response)
    #   self.assertTrue('id' in response.keys())

    def test_video(self):
        begin = self.app.begin("My another cool video")
        self.assertTrue('id' in begin.keys())

        style = self.app.set_style('vanilla')
        self.assertTrue(style is True)

        for i in range(0,2):
            image = self.app.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
            self.assertTrue('id' in image.keys())

        for i in range(0,2):
            text = self.app.add_text("This is cool", "This is not cool")
            self.assertTrue(text is True)

        music = self.app.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3")
        self.assertTrue('id' in music.keys())

        credit = self.app.add_credits("Music", "Vishnu")
        self.assertTrue(credit is True)

        quality = self.app.set_quality(picovico.Picovico.Q_360P)
        self.assertTrue(quality is True)

        create = self.app.create()
        self.assertEqual(create['status'], 7101)



if __name__ == '__main__':
    unittest.main()