import flask
from subprocess import call

app = flask.Flask(
    __name__,
    static_folder='public',
)

from datetime import datetime
from time import time
def getPrettyTimeStamp():
    return datetime.fromtimestamp(time()).strftime('%Y%m%d_%H%M%S')

@app.route("/")
def hello():
    return "Hello World!"

def take_picture(filename, warmup = 1.25):
    call(
        'imagesnap'
        + ((' -w ' + str(warmup)) if warmup > 0 else '')
        + ' ' + filename
    , shell=True)

@app.route("/capture")
def cam():
    filename = 'public/capture/' + getPrettyTimeStamp() + '.jpg'
    take_picture(filename)
    return flask.send_file(filename, mimetype='image/jpg')

if __name__ == "__main__":
    app.run(debug=True)
