from lib import config
from picovico import Picovico
from project import PicovicoProject
from lib.session import PicovicoSession

session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = session.authenticate()
auth_session = {'X-Access-Key': r['access_key'], 'X-Access-Token': r['access_token']}
print(auth_session)
print(r)

print("Authenticated")
print(auth_session)
r = session.profile(auth_session=auth_session)
print(r)

proj = PicovicoProject()
print('project')
print(auth_session)
r = proj.begin("Some cool project", auth_session=auth_session)
print(r)
print("Begin project")

# r = proj.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted", auth_session=auth_session)
# print(r)
# print("Image uploaded")

# r = proj.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted", auth_session=auth_session)
# print(r)
# print("Music uploaded")

r = proj.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", auth_session=auth_session)
print(r)
print("Music added")

r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', auth_session=auth_session)
print(r)
print("Image added")

r = proj.add_text("Aaeronn", "Bhatta")
print(r)
print("Text slide added")