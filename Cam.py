import subprocess

def has_program(program):
    try:
        subprocess.check_call(['which', program])
    except subprocess.CalledProcessError:
        return False
    else:
        return True

class Cam():
    def __init__(self, warmup = 1.25, rotate = 0, height=None, width=None):
        self.warmup = warmup
        self.rotate = rotate
        self.height = height
        self.width = width

    def take_picture(self, filename = None):
        filename = filename or '/tmp/camcamcam.jpg'

        if has_program('imagesnap'):
            command = ('imagesnap'
                + ((' -w ' + str(self.warmup)) if self.warmup > 0 else '')
                + ' ' + filename)
        elif has_program('raspistill'):
            command = ('raspistill'
                + ((' -t ' + str(self.warmup * 1000)) if self.warmup > 0 else '')
                + ' --output ' + filename
                + (' --rotation ' + str(self.rotate) if self.rotate > 0 else '')
                + (' --height ' + str(self.height) if self.height else '')
                + (' --width ' + str(self.width) if self.width else '')
            )

        subprocess.call(command, shell=True)

        return filename
