from lib import config, constants 
#from picovico import Picovico
from project import PicovicoProject
from lib.auth.session import PicovicoSession
from lib.auth.account import PicovicoAccount
from lib.components.video import PicovicoVideo
from lib.components.photo import PicovicoPhoto
from lib.components.music import PicovicoMusic
from lib.components.style import PicovicoStyle

session = PicovicoSession(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = session.authenticate()
print(r)
headers = session._get_auth_headers()
print(headers)

acc = PicovicoAccount()
r = acc.profile()
print(r)
print("Profile")

# proj = PicovicoProject()
# print('project')
# r = proj.begin("Some cool project", auth_session=auth_session)
# print(r)
# video_id = r['id']
# video_data = r
# print("Begin project")

# r = proj.set_style("vanilla")
# print(r)
# print("Style Added")

# r = proj.draft(auth_session=auth_session)
# print(r)
# print("Drafts")

# style = PicovicoStyle()
# r = style.get_styles(auth_session=auth_session)
# print(r)
# print("got style")

# r = style.set_style('vanilla', video_data=video_data)
# print(r)
# print("style set")


# photo = PicovicoPhoto()

# # r = proj.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted", auth_session=auth_session)
# # print(r)
# # print("Image uploaded")

# # r = proj.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted", auth_session=auth_session)
# # print(r)
# # print("Another Image uploaded")

# r = photo.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', 'This is caption', video_data=video_data, auth_session=auth_session)
# print(r)
# print("Image added")

# r = photo.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', video_data=video_data, auth_session=auth_session)
# print(r)
# print("Image added")

# # r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', 'This is caption', auth_session=auth_session)
# # print(r)
# # print("Image added")

# # r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', auth_session=auth_session)
# # print(r)
# # print("Image added")

# r = photo.add_text("Aaeronn", "Bhatta", video_data=video_data)
# print(r)
# print("Text slide added")

# r = photo.add_text("Vishnu", "Bhatta", video_data=video_data)
# print(r)
# print("Another Text slide added")

# # r = proj.add_text("Aaeronn", "Bhatta")
# # print(r)
# # print("Text slide added")

# # r = proj.add_text("Vishnu", "Bhatta")
# # print(r)
# # print("Another Text slide added")

# # r = proj.get_images(auth_session)
# # print(r)
# # print('Got photos')

# music = PicovicoMusic()

# # r = proj.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted", auth_session=auth_session)
# # print(r)
# # print("Music uploaded")

# # r = proj.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", auth_session=auth_session)
# # print(r)
# # print("Music added")

# r = music.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted", auth_session=auth_session)
# print(r)
# print("Music uploaded")

# r = music.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", video_data=video_data, auth_session=auth_session)
# print(r)
# print("Music added")

# r = proj.add_credits("Music", "Aaeronn")
# print(r)
# print("Credit Added")

# r = proj.add_credits("Photo", "Hem")
# print(r)
# print("Another Credit Added")


# r = proj.set_quality(constants.Q_360P)
# print(r)
# print("Quality set")

# #vid = PicovicoVideo()

# r = proj.create_video(video_id, auth_session=auth_session)
# print(r)
# print("Video Created")


