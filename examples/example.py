from picovico import PicovicoAPI

# Define the fundamentals
PICOVICO_DEVICE_ID = 'SOME-DEVICE-ID'
PICOVICO_APP_ID = 'YOUR-APPLICATION-ID'
PICOVICO_APP_SECRET = 'YOUR-APP-SECRET'

# Initialize API
"""
1. Optionally, authentication can be done later as well.
  api.authenticate('app-secret')
2. To authenticate with username / password instead
  api.login('username', 'password')
"""
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, PICOVICO_APP_SECRET)

# Picovico Components are referenced as api.some_component
pv_music = api.music_component
pv_style = api.style_component
pv_photo = api.photo_component
pv_video = api.video_component

# Project is a separate workflow to assist in video creation
"""
Refer to Hello World Example, for better understanding of the Project Workflow
- A project is begun, which remains as active project
- Define the project with slides / music / style etc
- Save / Preview the project
- Render / Discard to close the active project
"""
pv_project = api.project

# Check the available freebies
"""
- Picovico has a library of Free (Attribution required) Music Files
- Picovico has a set of fundamental styles, which are free for personal usage
"""
free_styles = api.free_styles()
free_musics = api.free_musics()

# View profile, Check your account balance, etc.
api.me()

# Upload Local File
pv_project.add_photo_file('full/file/path', 'caption')
pv_project.add_music_file('full/file/path')

# Use hosted image / music
pv_project.add_photo_url('url', 'thumb', 'caption')
pv_project.add_music_url('url', 'preview')

# Use Preview Uploads
pv_project.add_photo('id')
pv_project.add_music('id')

# Navigate Picovico Library, or your library with the available helper methods
"""
  - .all() - Fetch all items
  - .one('id') - Fetch one item
  - .delete('id') - Delete item (subject to ownership)
"""
pv_photo.all()
pv_photo.one('SINGLE_PHOTO_ID')
pv_photo.delete('SINGLE_PHOTO_ID')

# Other methods
pv_photo.upload_file('LOCAL_FILE_PATH')
pv_photo.upload_url('PHOTO_URL', 'PHOTO_THUMBNAIL_URL')

pv_music.upload_file('...')
pv_music.upload_url('...', '...')

# Please refer to the class reference, if you have any further confusions
# Please contact dev@picovico.com for queries