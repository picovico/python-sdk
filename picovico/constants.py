from collections import namedtuple

SUPPORTED_IMAGE_FORMAT = ('PNG', 'JPEG')

_all_status =  ("initial", "processing", "published")
STATUS = namedtuple('Status', [st.upper() for st in _all_status])._make(_all_status)

_quality = {
    'PREVIEW': 144,
    'STANDARD': 360,
    'MEDIUM' : 480,
    'HIGH_DEF': 720
}
QUALITY = namedtuple('Quality',_quality.keys())(**_quality)

_asset = ('image', 'music', 'video', 'audio', 'text')
ASSETS = namedtuple('Asset', [a.upper() for a in _asset])._make(_asset)
