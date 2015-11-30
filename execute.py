from lib import config, constants
from picovico import Picovico

app = Picovico(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = app.authenticate()
print(r)
r = app.profile()
print(r)

r = app.begin("Some cool project")
print(r)
print("Begin project")

r = app.set_style("vanilla")
print(r)
print("Style Added")

r = app.add_text("Aaeronn", "Bhatta")
print(r)
print("Text slide added")

r = app.add_image('http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png', "This is caption")
print(r)
print("Image Added")

r = app.add_image('http://s3.amazonaws.com/pvcdn2/video/8501d6865c2d484abb2e8a858cffca80/8501d6865c2d484abb2e8a858cffca80-360.jpg')
print(r)
print("Another image added")

r = app.add_text("Vishnu", "Raj")
print(r)
print("Another Text slide added")

# r = app.upload_image("http://s3-us-west-2.amazonaws.com/pv-styles/christmas/pv_christmas_winter_themes.png", "hosted")
# print(r)
# r = app.upload_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3", "hosted")
# print(r)

# r = app.get_musics()
# print(r)
# r = app.get_library_musics()
# #print(r)
# print("library music completed")

r = app.add_music("http://s3.amazonaws.com/picovico-1/assets/music/Latin/Latinish.mp3")
print(r)
print("Music added")
# r = app.delete_music("nMBt9")
# print(r)
# print("Music deleted")

# r = app.get_styles()
# print(r)
# print("Style added")
# r = app.remove_credits()
# print(r)
r = app.add_credits("Music", "Aaeronn")
print(r)
print("Credit Added")

r = app.add_credits("Photo", "Hem")
print(r)
print("Another Credit Added")


r = app.set_quality(Picovico.Q_360P)
print(r)
print("Quality set")

# r = app.remove_credits()
# print(r)
# print("Credit removed")

# r = app.get("nMB2k")
# print(r)
# print("Single video")

r = app.create()
print(r)
print("Video Created")

r = app.get_videos()
print(r)