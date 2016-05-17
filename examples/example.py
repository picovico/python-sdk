from picovico import PicovicoAPI

#Create a config files to import settings

PICOVICO_DEVICE_ID = 'SOME-DEVICE-ID'
PICOVICO_APP_ID = 'YOUR-APPLICATION-ID'
PICOVICO_APP_SECRET = None
#'YOUR-APP-SECRET'

#initiate api
#provide the app_secret argument, or call api.authenticate() later
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, PICOVICO_APP_SECRET)

#to get picovico system components
free_styles = api.free_styles()
free_musics = api.free_musics()

# Authentication is done by either of the methods, .login() or .authenticate()
# USE ONLY ONE
# .login() to login with username and password
# .authenticate() to login with app_id and app_secret
api.authenticate('YOUR-APP-SECRET')
api.login('YOUR-USERNAME', 'YOUR-PASSWORD')

#Either login or authenticate is needed for actions described below:
pv_music = api.music_component
pv_style = api.style_component
pv_photo = api.photo_component
pv_video = api.video_component
pv_project = api.project_components


#View profile 
api.me()

#For video creation
pv_project.begin(name='OPTIONAL')
#if change of name required
pv_project.set_name('NEW_NAME')

pv_project.set_style('STYLE_NAME')
pv_project.set_quality(720)
pv_project.add_text('title', 'body')
pv_project.add_photo('id', 'caption')
pv_project.add_music('id')
pv_project.add_credit('somename', 'somevalue')
#for saving project video
pv_project.save()
#for rendering project video
pv_project.render()
#for preview of project
pv_project.preview()
#for project delete
pv_project.discard()

#for music and photo upload
pv_project.add_photo_file('full/file/path', 'caption')
pv_project.add_photo_url('url', 'thumb', 'caption')
pv_project.add_music_url('url', 'preview')
pv_project.add_music_file('full/file/path')



#All components are provided with some basic method
#In some cases the method may not be implemented
#Component methods
pv_photo.all()
pv_photo.one('SINGLE_PHOTO_ID')
pv_photo.upload_file('LOCAL_FILE_PATH')
pv_photo.upload_url('PHOTO_URL', 'PHOTO_THUMBNAIL_URL')
pv_photo.delete('SINGLE_PHOTO_ID')
