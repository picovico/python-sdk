""" .. :mod: urls
            :synopsis: URL paths and endpoints.

All the api related endpoints and host.
"""

#: Base URL
PICOVICO_BASE = "https://uapi-f1.picovico.com/v2.1/"

PICOVICO_APP = "login/app"
PICOVICO_LOGIN = "login"
PICOVICO_MUSICS = "musics"
PICOVICO_STYLES = "styles"
ME = "me"
MY_DRAFT = "{}/draft".format(ME)
MY_PHOTOS = "{}/photos".format(ME)
MY_MUSICS = "{}/{}".format(ME, PICOVICO_MUSICS)
MY_VIDEOS = "{}/videos".format(ME)
MY_STYLES = "{}/{}".format(ME, PICOVICO_STYLES)
MY_SINGLE_PHOTO = MY_PHOTOS+"/{photo_id}"
MY_SINGLE_MUSIC = MY_MUSICS+"/{music_id}"
MY_SINGLE_DRAFT = MY_DRAFT+"/{draft_id}"
MY_SINGLE_VIDEO = MY_VIDEOS+"/{video_id}"
MY_SINGLE_VIDEO_CREATE = "{}/render".format(MY_SINGLE_VIDEO)
MY_SINGLE_VIDEO_PREVIEW = "{}/preview".format(MY_SINGLE_VIDEO)
MY_SINGLE_VIDEO_DUPLICATE = "{}/duplicate".format(MY_SINGLE_VIDEO)
