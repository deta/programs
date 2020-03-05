import random
from deta.lib import app
from deta.lib.responses import Response
import svgs
from colors import colors


@app.http("/")
def avatar(event):
    i = event.params.get("i", "")
    c = event.params.get("c", colors[random.randint(0,920)])
    cc = event.params.get("cc")
    if cc:
       return Response(svgs.gradient.format(c, cc, i), content_type="image/svg+xml")
    return Response(svgs.onecolor.format(c, i), content_type="image/svg+xml")
