#!/usr/bin/python3

import pygame
import optparse
import os, sys
import config
import platform

parser = optparse.OptionParser(usage='python %prog -c True\nor:\npython %prog -c True', version="0.0.1",
                               prog=sys.argv[0])
parser.add_option('-c', '--cached-map', action="store_true", help="Loads the cached map file stored in map.cache",
                  dest="load_cached", default=False)
options, args = parser.parse_args()

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    config.GPIO_AVAILABLE = True
    print("GPIO AVAILABLE")
    
except Exception:
    _, err, _ = sys.exc_info()
    print("GPIO UNAVAILABLE (%s)" % err)
    config.GPIO_AVAILABLE = False

if config.GPIO_AVAILABLE:
    # Init framebuffer/touchscreen environment variables
    # os.environ['SDL_VIDEODRIVER'] = 'fbcon'
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"


    
    config.touchScale = 100
    config.invertPosition = True

from pypboy.core import Pypboy

if __name__ == "__main__":
    boy = Pypboy('Pip-Boy 3000', config.WIDTH, config.HEIGHT)
    print("RUN")
    boy.run()
