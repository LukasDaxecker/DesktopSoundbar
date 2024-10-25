# Stuff
from random import random
import os
import time
import numpy as np
# Graphics
from screeninfo import get_monitors
import pygame
import win32api
import win32con
import win32gui
# Audio Input
import pyaudiodevice
from pyaudiodevice import default_playback
from pyaudiodevice.audio_common import AudioCommon

def GetColors():
        try:
                file = open("ColorRange.txt", "r")
                inputString = file.read()
                colors = inputString.split("\n")                                 
        except:
                print("File not Found")
        finally:
                del inputString                         
                file.close
                print("File opened and read")
                return colors
        
def GetMonitorMeasurements():
        try:
                for m in get_monitors():
                        if m.is_primary:
                                screenWidth = m.width
                                screenHeight = int(m.height/4)
                                pos = int(m.height/4*3)
        except:
                print("Cannot find Monitors")
        finally:
                print("Monitor Massurements have been taken")

        return screenWidth, screenHeight, pos

def GetAudioDevices():
        common = AudioCommon() 
        return common.get_default_device() # Defaults to headset
         
def GetHeight(screenHeight):
        #------------------------------------------------------------------------------------------------#
        height = 20 
        height = random() * screenHeight/4*3
        #------------------------------------------------------------------------------------------------#
        
        return height

def DrawRects(colors, screenHeight, screenWidth):
        widthRect = screenWidth/len(colors)
        
        for i in range(len(colors)):
                heightRect = GetHeight(screenHeight)
                # Change Hex to RGB
                hex = str(colors[i]).lstrip('#')
                RGB = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
                # Draw Rect
                pygame.draw.rect(screen, RGB, pygame.Rect(widthRect * i, screenHeight-heightRect, widthRect, heightRect))
                

# def RecordAudio():


if __name__ =="__main__":
        colors = GetColors()

        screenWidth, screenHeight, pos = GetMonitorMeasurements()
        audioDevice = GetAudioDevices()

        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,pos)
        pygame.init()
        screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)
        done = False
        transperantColor = (255, 0, 128)  # Transparency color

        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transperantColor), 0, win32con.LWA_COLORKEY)

        print(default_playback.DefaultPlayback.get_volume()) 
        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                screen.fill(transperantColor)
                #--------------------------Work Space------------------------#
                # DrawRects(colors, screenHeight, screenWidth)

                #------------------------------------------------------------#
                pygame.display.update()