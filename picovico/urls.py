""" .. :mod: urls
            :synopsis: URL paths and endpoints.

All the api related endpoints and host.
"""

#: Base URL
PICOVICO_BASE = "https://uapi-f1.picovico.com/v2.1/"

#: Picovico APP login URL path.
PICOVICO_APP = "login/app"
#: Picovico login URL path.
PICOVICO_LOGIN = "login"
#: Picovico System music path.
PICOVICO_MUSICS = "musics"
#: Picovico System style path.
PICOVICO_STYLES = "styles"
#: Picovico User profile path for logged in user.
ME = "me"
#: Picovico user video project draft path.
MY_DRAFT = "{}/draft".format(ME)
#: Picovico user uploaded photos path.
MY_PHOTOS = "{}/photos".format(ME)
#: Picovico user uploaded musics path.
MY_MUSICS = "{}/{}".format(ME, PICOVICO_MUSICS)
#: Picovico user videos path.
MY_VIDEOS = "{}/videos".format(ME)
#: Picovico user specific styles path.
MY_STYLES = "{}/{}".format(ME, PICOVICO_STYLES)
#: Picovico user photo path with specific **id**.
MY_SINGLE_PHOTO = MY_PHOTOS+"/{photo_id}"
MY_SINGLE_MUSIC = MY_MUSICS+"/{music_id}"
MY_SINGLE_DRAFT = MY_DRAFT+"/{draft_id}"
MY_SINGLE_VIDEO = MY_VIDEOS+"/{video_id}"
MY_SINGLE_VIDEO_CREATE = "{}/render".format(MY_SINGLE_VIDEO)
MY_SINGLE_VIDEO_PREVIEW = "{}/preview".format(MY_SINGLE_VIDEO)
MY_SINGLE_VIDEO_DUPLICATE = "{}/duplicate".format(MY_SINGLE_VIDEO)
