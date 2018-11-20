#!/usr/bin/env python2
# coding=utf-8

from hermes_python.hermes import Hermes
import Queue
import RPi.GPIO as GPIO
from PIL import Image
from Adafruit_Thermal import *
import os
import random
from snipshelpers.thread_handler import ThreadHandler
from snipshelpers.config_parser import SnipsConfigParser
import time

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

DIR = os.path.dirname(os.path.realpath(__file__)) + '/image/'

class Skill:

    def __init__(self):

        self.ledPin = 12
        self.printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
        list_dir = [d for d in os.listdir(DIR) if os.path.isdir(DIR+d)]
        self.dir = {}
        self.image = [i for i in os.listdir(DIR) if not i in list_dir]
        for l in list_dir :
            tmp = os.listdir(DIR + l)
            self.dir[l] = tmp
        print(self.image)
        print(self.dir)
    
def extract_image_name(intent_message):
    image = []
    if intent_message.slots.image is not None:
        for room in intent_message.slots.image:
            image.append(room.slot_value.value.value)
    return image

def callback(hermes, intent_message):
    print(intent_message.session_id)
    image = extract_image_name(intent_message)
    print(image)
    to_print = ""
    for tmp in image:
        for d in skill.dir:
                if tmp in d:
                    to_print = DIR + d + "/" + random.choice(skill.dir[tmp])
        for d in skill.image:
            if tmp in d:
                to_print = DIR + d

    if to_print == "":
        return
        for i in image:
            skill.printer.println("We do not have an image of " + i + " in this printer.")
    else:
        img = Image.open(to_print)
        new_width  = 384
        new_height = new_width * img.size[1] / img.size[0]
        print(new_width)
        print(new_height)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        skill.printer.printImage(img, True)
        time.sleep(0.2)
        skill.printer.setCodePage(Adafruit_Thermal.CODEPAGE_ISO_8859_1)
        skill.printer.println(u"Créez votre propre assistant\nvocal respectueux de la vie\nprivée".encode("latin-1"))
        skill.printer.println("https://makers.snips.ai")
        skill.printer.println("#MakeWithSnips")
        skill.printer.setCodePage(0)
    skill.printer.feed(3)
    print(image)

if __name__ == "__main__":
    skill = Skill()
    skill.printer.println("Ready!!")
    skill.printer.feed(3)
    
    with Hermes(MQTT_ADDR) as h: 
        h.skill = skill
        h.subscribe_intent("print", callback) \
         .loop_forever()
