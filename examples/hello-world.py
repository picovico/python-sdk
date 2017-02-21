from picovico import PicovicoAPI

# 1. Define the fundamentals
PICOVICO_DEVICE_ID = 'SOME-DEVICE-ID'
PICOVICO_APP_ID = 'YOUR-APPLICATION-ID'
PICOVICO_APP_SECRET = 'YOUR-APP-SECRET'

# 2. Initialize API
# - Provide the app_secret argument, or call api.authenticate() later
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, PICOVICO_APP_SECRET)
api.authenticate()

# component alias (optional)
pv_music = api.music_component
pv_style = api.style_component
pv_photo = api.photo_component
pv_video = api.video_component
pv_project = api.project

# 3. Begin a project. (Once a project is begun, it remains as active project)
pv_project.begin(name='Hello World') # Choose your project name.

# 4. Define the project
pv_project.set_style('vanilla') # Choose a style, Vanilla is always beautiful :)
pv_project.set_quality(720)
pv_project.add_text('Hello World', 'This is Picovico') # Title, Text or Subtitle
pv_project.add_photo_url('', 'thumb', 'caption') # Upload photo by URL, file or previous uploads
pv_project.add_music('NhLIi') # Clear Air, By Kevin MacLeod (You can use your music as well)
pv_project.add_credit('Music', 'Kevin MacLeod') # Give credit, wherever required
# 5. Save the project progress (Optional, you may directly jump to preview or render)
pv_project.save()

# 6. Preview if required (Optional, you may jump to render if you are sure)
pv_project.preview()

# 7. Send rendering request for the active project
pv_project.render()
