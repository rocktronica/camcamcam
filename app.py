import argparse
import flask

import Cam

parser = argparse.ArgumentParser(
    description='Web wrapper for FaceTime camera, mostly to make sure my cat is eating her food when I\'m away!',
    usage='python app.py [arguments]')

parser.add_argument("--host", type=str, default='127.0.0.1',
    help='Host, eg 127.0.0.1 (localhost)')
parser.add_argument("--port", type=int, default=8080,
    help='Port, eg 8080')
parser.add_argument("--rotate", type=int, default=0,
    help='Photo rotate, for pi')
parser.add_argument("--height", type=int, default=None,
    help='Photo height, for pi')
parser.add_argument("--width", type=int, default=None,
    help='Photo width, for pi')
parser.add_argument("--debug", action="store_true",
    help='Run Flask in debug mode')
parser.add_argument("--save", action="store_true",
    help='Save pictures to public folder instead of using /tmp')
parser.add_argument("--broadcast", action="store_true",
    help='Supplant host and port to 0.0.0.0 and 80, for externalizing machine')
arguments = parser.parse_args()

cam = Cam.Cam()

app = flask.Flask(
    __name__,
    static_folder='public',
    template_folder=''
)

from datetime import datetime
from time import time
def getPrettyTimeStamp():
    return datetime.fromtimestamp(time()).strftime('%Y%m%d_%H%M%S')

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/capture")
@app.route("/capture/<refresh>")
def capture(refresh=None):
    filename = None
    if arguments.save:
        filename = 'public/capture/' + getPrettyTimeStamp() + '.jpg'
    filename = cam.take_picture(
        filename,
        rotate = arguments.rotate,
        height = arguments.height,
        width = arguments.width
    )

    return (
        flask.send_file(filename, mimetype='image/jpg'),
        200,
        {'Refresh': refresh + ';url=/capture/' + refresh} if refresh else {}
    )

if __name__ == "__main__":
    broadcast = arguments.broadcast
    host = arguments.host if not broadcast else '0.0.0.0'
    port = arguments.port if not broadcast else 80

    app.run(host=host, port=port, debug=arguments.debug)
