# Stuff
from random import random
from matplotlib import pyplot as plt
import scipy.signal as signal
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
import scipy, matplotlib
import wave, struct 
import pyaudio

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
        global screenWidth, screenHeight, pos
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

def GetAudioDevices():
        devices = []
        audioInterface = pyaudio.PyAudio()
        for i in range(audioInterface.get_device_count()):
                if("Lautsprecher" in audioInterface.get_device_info_by_index(i).get('name')):
                        devices.append(audioInterface.get_device_info_by_index(i))
        
         
def GetHeight(screenHeight):
        global rectHightArray
        #------------------------------------------------------------------------------------------------#
        height = 20 
        height = random() * screenHeight/4*3
        
        rectHightArray.append(height)

def DrawRects():
        global colors, screenHeight, rectHightArray
        widthRect = screenWidth/len(colors)
        rectHightArray = []
        
        for i in range(len(colors)):
                GetHeight(screenHeight)
                heightRect = rectHightArray[i]
                # Change Hex to RGB
                hex = str(colors[i]).lstrip('#')
                RGB = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
                # Draw Rect
                pygame.draw.rect(screen, RGB, pygame.Rect(widthRect * i, screenHeight-heightRect, widthRect, heightRect))
                

# def RecordAudio():


if __name__ =="__main__":
        colors = GetColors()

        GetMonitorMeasurements()
        GetAudioDevices()

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

        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True
                screen.fill(transperantColor)
                #--------------------------Work Space------------------------#
                
                DrawRects()

                #------------------------------------------------------------#
                pygame.display.update()