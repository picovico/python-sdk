from lib import config, constants 
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
headers = session
print(headers)
print("Authenticated")

acc = PicovicoAccount(headers)
r = acc.profile()
print(r)
print("Profile")

proj = PicovicoProject(headers)
print('project')
r = proj.begin("Some cool project")
print(r)
print("Video id")
print(r['id'])
video_id = r['id']
print("Begin project")

r = proj.set_style("vanilla")
print(r)
print("Style Added")

r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg', 'This is caption')
print(r)
print("Image added")

r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg')
print(r)
print("Another Image added")

r = proj.add_text("Aaeronn", "Bhatta")
print(r)
print("Text slide added")

r = proj.add_text("Vishnu", "Bhatta")
print(r)
print("Another Text slide added")

r = proj.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3")
print(r)
print("Music added")

r = proj.add_credits("Music", "Aaeronn")
print(r)
print("Credit Added")

r = proj.set_quality(constants.Q_360P)
print(r)
print("Quality set")


r = proj.create_video(video_id=video_id)
print(r)
print('Video Created')





