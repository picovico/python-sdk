from lib import config, constants 
from picovico import Picovico
from project import PicovicoProject
from lib.session import PicovicoSession

session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = session.authenticate()
auth_session = {'X-Access-Key': r['access_key'], 'X-Access-Token': r['access_token']}
print(r)

print("Authenticated")
r = session.profile(auth_session=auth_session)
print(r)

proj = PicovicoProject()
print('project')
r = proj.begin("Some cool project", auth_session=auth_session)
print(r)
print("Begin project")

r = proj.set_style("vanilla")
print(r)
print("Style Added")

r = proj.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted", auth_session=auth_session)
print(r)
print("Image uploaded")

r = proj.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted", auth_session=auth_session)
print(r)
print("Another Image uploaded")

r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', 'This is caption', auth_session=auth_session)
print(r)
print("Image added")

r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', auth_session=auth_session)
print(r)
print("Image added")

r = proj.add_text("Aaeronn", "Bhatta")
print(r)
print("Text slide added")

r = proj.add_text("Vishnu", "Bhatta")
print(r)
print("Another Text slide added")

r = proj.get_images(auth_session)
print(r)
print('Got photos')

r = proj.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted", auth_session=auth_session)
print(r)
print("Music uploaded")

r = proj.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", auth_session=auth_session)
print(r)
print("Music added")

# r = proj.add_credits("Music", "Aaeronn")
# print(r)
# print("Credit Added")

# r = proj.add_credits("Photo", "Hem")
# print(r)
# print("Another Credit Added")


r = proj.set_quality(constants.Q_360P)
print(r)
print("Quality set")

r = proj.create_video(auth_session=auth_session)
print(r)
print("Video Created")


