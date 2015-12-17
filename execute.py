from lib import config
from picovico import Picovico

app = Picovico(config.PICOVICO_APP_ID, config.PICOVICO_APP_SECRET)
r = app.authenticate()
print(r)
print("Authenticated")
# r = app.profile()
# print(r)