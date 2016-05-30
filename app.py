from flask import Flask
from subprocess import call

app = Flask(
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

@app.route("/cam")
def cam():
    filename = 'public/capture/' + getPrettyTimeStamp() + '.jpg'
    call('imagesnap ' + filename, shell=True)
    return '<a href=' + filename + '>' + filename + '</a>'



if __name__ == "__main__":
    app.run(debug=True)
