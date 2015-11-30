'''
    Url configuration for Picovico python-sdk
'''

#Config for Picovico endpoint api url
PICOVICO_API_ENDPOINT = "https://uapi-f1.picovico.com/v2.1/"

LOGIN = "login"
APP_AUTHENTICATE = "login/app"
BEGIN_PROJECT = "me/videos"
SINGLE_VIDEO = "me/videos/{}"
SAVE_VIDEO = "me/videos/{}"
PREVIEW_VIDEO = "me/videos/{}/preview"
CREATE_VIDEO = "me/videos/{}/render"
DUPLICATE_VIDEO = "me/videos/{}/duplicate"
GET_VIDEOS = "me/videos"
UPLOAD_MUSIC = "me/musics"
GET_MUSICS = "me/musics"
GET_LIBRARY_MUSICS = "musics"
DELETE_MUSIC = "me/musics/{}"
UPLOAD_PHOTO = "me/photos"
GET_STYLES = "me/styles"
GET_DRAFT = "me/draft"
GET_SINGLE_DRAFT = "me/draft/{}"
ME = "me"