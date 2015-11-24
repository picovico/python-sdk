from lib import config
from picovico import Picovico

app = Picovico(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = app.authenticate()
print(r)
r = app.profile()
print(r)
r = app.begin("Aaeronn")
print(r)
r = app.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted")
print(r)
r = app.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted")
print(r)
r = app.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
print(r)