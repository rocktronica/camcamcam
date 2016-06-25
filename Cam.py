import subprocess

def has_program(program):
    try:
        subprocess.check_call(['which', program])
    except subprocess.CalledProcessError:
        return False
    else:
        return True

class Cam():
    def take_picture(self, filename = None, warmup = 1.25, rotate = 0,
            height = None, width = None):
        filename = filename or '/tmp/camcamcam.jpg'

        if has_program('imagesnap'):
            command = ('imagesnap'
                + ((' -w ' + str(warmup)) if warmup > 0 else '')
                + ' ' + filename)
        elif has_program('raspistill'):
            command = ('raspistill'
                + ((' -t ' + str(warmup * 1000)) if warmup > 0 else '')
                + ' --output ' + filename
                + (' --rotation ' + str(rotate) if rotate > 0 else '')
                + (' --height ' + str(height) if height else '')
                + (' --width ' + str(width) if width else '')
            )

        subprocess.call(command, shell=True)

        return filename
