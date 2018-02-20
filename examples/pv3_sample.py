from __future__ import print_function
import json

from picovico.exceptions import PicovicoError
from picovico import PicovicoAPI as PicovicoAPI

APP_ID = ''
APP_SECRET = ''
DEVICE_ID = ''

picovico = PicovicoAPI(APP_ID, app_secret=APP_SECRET, device_id=DEVICE_ID)
picovico.authenticate()
payload = {
    "style" : "vanilla_frameless",
    "quality" : 360,
    "name" : "Sample Video",
    "aspect_ratio" : "16:9",
    "assets" : [{
            "music" : {
                "id" : "aud_6j44J9zjbSQe54ZTTSqUj2"
            }
            ,
            "frames" : {
                pv.text_slide(title="You are", body="my love"),
                pv.text_slide(title="You are", body="CSS to my HTML"),
                pv.image_slide(image_url="https://images.unsplash.com/photo-1481326086332-e77dd61a4ea1"),
                pv.text_slide(title="You", body="make me complete")
            }
        }
    ]
}
try:
    res = pv.authenticated_api(method='post', url='me/videos', params=json.dumps(payload), headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
except PicovicoError as e:
    print(str(e))
else:
    print(res)

