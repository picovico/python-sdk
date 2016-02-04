from picovico import PicovicoAPI

#Create a config files to import settings

PICOVICO_DEVICE_ID = 'com.picovico.api.python-sdk'
PICOVICO_APP_ID = "some-app-id"
PICOVICO_APP_SECRET = "some-app-secret"

#initiate api
api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID, PICOVICO_APP_SECRET)
#api = PicovicoAPI(PICOVICO_APP_ID, PICOVICO_DEVICE_ID)

#to get picovico system components
styles = api.get_library_styles()
musics = api.get_library_musics()

#To authenticate with secret
api.authenticate()
#If secret is not provided in api initialization
#api.authenticate(PICOVICO_APP_SECRET)

#To login with username and password
api.login('YOUR_USERNAME', 'YOUR_PASSWORD')

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
my_photo_component.get_photos()
my_photo_component.get_photo('SINGLE_PHOTO_ID')
my_photo_component.upload_photo_file('LOCAL_FILE_PATH')
my_photo_component.upload_photo_url('PHOTO_URL', 'PHOTO_THUMBNAIL_URL')
my_photo_component.delete_photo('SINGLE_PHOTO_ID')
