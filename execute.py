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
r = proj.begin("My project")
print(r)
print("Video id")
print(r['id'])
video_id = r['id']
print("Begin project")

# r = proj.open(video_id=video_id)
# print(r)
# print('Video Opened')

r = proj.set_style("carol")
print(r)
print("Style Added")

r = proj.add_image('http://c.tadst.com/gfx/600x400/christmas.jpg?1', 'Ho Ho Ho Its christmas :)')
print(r)
print("Image added")

r = proj.add_text("Christmas", "A season of cold warm with happiness around ")
print(r)
print("Text slide added")

r = proj.add_text("...And", "Christmas is the season when you buy this year's gifts with next year's money..")
print(r)
print("Text slide added")


r = proj.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg')
print(r)
print("Another Image added")

r = proj.add_text("My Wish", "Dear Santa, what I want for Christmas is... your list with names of naughty girls.")
print(r)
print("Text slide added")

r = proj.add_text("...And", "a bar with my choice of wine.. HO HO..")
print(r)
print("Text slide added")

r = proj.add_image('http://snowvillageinn.com/wp-content/uploads/2015/10/christmas_decoration.jpg')
print(r)
print("Another Image added")

r = proj.add_image('http://oilersnation.com/uploads/Image/christmas2.jpg')
print(r)
print("Another Image added")

r = proj.add_text("Wish", "you all MERRY CHRISTMAS")
print(r)
print("Text slide added")

r = proj.add_music("https://s3-us-west-2.amazonaws.com/pv-audio-library/free-music/preview/Christmas/Kevin-MacLeod-Christmas-Rap.mp3")
print(r)
print("Music added")

r = proj.add_credits("Music", "Aaeronn")
print(r)
print("Credit Added")

r = proj.set_quality(constants.Q_360P)
print(r)
print("Quality set")

r = proj.preview_video(video_id=video_id)
print(r)
print("Previewed")

r = proj.create_video(video_id=video_id)
print(r)
print('Video Created')







