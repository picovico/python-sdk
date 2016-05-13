from picovico import PicovicoAPI

#Create a config files to import settings

PICOVICO_DEVICE_ID = 'SOME-DEVICE-ID'
PICOVICO_APP_ID = 'YOUR-APPLICATION-ID'
PICOVICO_APP_SECRET = None
#'YOUR-APP-SECRET'

#initiate api
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, 'PICOVICO-APP-SECRET-[OPTIONAL]') # can call .authenticate method later

#to get picovico system components
free_styles = api.free_styles()
free_musics = api.free_musics()

#To authenticate with app_id and app_secret
api.authenticate('YOUR-APP-SECRET')
#if secret is initiated in api just call api.authenticate()

#To login with username and password
api.login('YOUR-USERNAME', 'YOUR-PASSWORD')

#Either login or authenticate is needed for actions described below:
pv_music = api.music_component
pv_style = api.style_component
pv_photo = api.photo_component
pv_video = api.video_component

#View profile 
api.me()

#All components are provided with some basic method
#In some cases the method may not be implemented
#Component methods
pv_photo.all()
pv_photo.one('SINGLE_PHOTO_ID')
pv_photo.upload_file('LOCAL_FILE_PATH')
pv_photo.upload_url('PHOTO_URL', 'PHOTO_THUMBNAIL_URL')
pv_photo.delete('SINGLE_PHOTO_ID')
