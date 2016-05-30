import argparse
import flask
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default='127.0.0.1')
parser.add_argument("--port", type=int, default=5000)
parser.add_argument("--debug", type=bool, default=False)
parser.add_argument("--save", type=bool, default=False)
arguments = parser.parse_args()

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

def take_picture(filename = None, warmup = 1.25):
    filename = filename or '/tmp/camcamcam.jpg'

    call(
        'imagesnap'
        + ((' -w ' + str(warmup)) if warmup > 0 else '')
        + ' ' + filename
    , shell=True)

    return filename

@app.route("/capture")
def cam():
    filename = None
    if arguments.save:
        filename = 'public/capture/' + getPrettyTimeStamp() + '.jpg'

    filename = take_picture(filename)
    return flask.send_file(filename, mimetype='image/jpg')

if __name__ == "__main__":
    app.run(host=arguments.host, port=arguments.port, debug=arguments.debug)
