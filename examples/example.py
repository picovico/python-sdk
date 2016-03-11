from picovico import PicovicoAPI

#Create a config files to import settings

PICOVICO_DEVICE_ID = 'SOME-DEVICE-ID'
PICOVICO_APP_ID = 'YOUR-APPLICATION-ID'
PICOVICO_APP_SECRET = None
#'YOUR-APP-SECRET'

#initiate api
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, PICOVICO_APP_SECRET)
#api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID)

#to get picovico system components
free_styles = api.free_styles()
free_musics = api.free_musics()

#To authenticate
api.authenticate('YOUR-APP-SECRET')
#if secret is initiated in api just call api.authenticate()

#To login with username and password
api.login('YOUR-USERNAME', 'YOUR-PASSWORD')

#Either login or authenticate is needed for actions described below:
my_music_component = api.music_component
my_style_component = api.style_component
my_photo_component = api.photo_component
my_video_component = api.video_component

#View profile 
api.me()

#All components are provided with some basic method
#In some cases the method may not be implemented
#Component methods
my_photo_component.all()
my_photo_component.one('SINGLE_PHOTO_ID')
my_photo_component.upload_file('LOCAL_FILE_PATH')
my_photo_component.upload_url('PHOTO_URL', 'PHOTO_THUMBNAIL_URL')
my_photo_component.delete('SINGLE_PHOTO_ID')
