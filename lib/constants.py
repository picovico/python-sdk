'''
    Constants configuration for Picovico
'''

class PicovicoConstants(object):
    # Api version settings 
    API_VERSION = '2.1'
    VERSION = '2.0.13'
    API_SERVER = 'api.picovico.com'
    API_SCHEME = 'https'

    # Available Video rendering states
    VIDEO_INITIAL = "initial"
    VIDEO_PUBLISHED = "published"
    VIDEO_PROCESSING = "processing"

    # Rendering Quality Levels
    Q_360P = 360 # ld
    Q_480P = 480 # sd
    Q_720P = 720 # md
    Q_1080P = 1080 # hd

    STANDARD_SLIDE_DURATION = 5