#!/usr/bin/python3
#
# .../pypboy/game/core.py
#

import pygame
import time

from pygame import KEYDOWN, QUIT

import config
from pypboy.boot.cmdlinebootup import CmdLineClass


class Engine(object):

    EVENTS_UPDATE = pygame.USEREVENT + 1
    EVENTS_RENDER = pygame.USEREVENT + 2

    def __init__(self, title, width, height, *args, **kwargs):
        pygame.init()
        pygame.display.init()
        super(Engine, self).__init__(*args, **kwargs)


        self.rootParent = self

        # --- Screen and Canvas Setup ---
        self.native_size = (config.WIDTH, config.HEIGHT)
        display_info = pygame.display.Info()
        self.screen_size = (display_info.current_w, display_info.current_h)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        self.canvas = pygame.Surface(self.native_size)

        pygame.display.set_caption(title)
        pygame.mouse.set_visible(False)

        self.groups = []
        self.root_children = Group() # <-- MODIFICATION: Use the corrected Group class name
        self.background = pygame.surface.Surface(self.native_size).convert_alpha()
        backAdd = 30
        self.background.fill((backAdd, backAdd, backAdd), None, pygame.BLEND_RGB_ADD)

        self.rescale = False
        self.last_render_time = 0

        # Scanlines:
        self.lineCount = 80
        self.lineHeight = config.HEIGHT // self.lineCount
        scanline = pygame.transform.smoothscale(pygame.image.load('images/pipboyscanlines.png').convert_alpha(), (config.WIDTH, self.lineHeight))

        self.scanLines = pygame.Surface(self.native_size)
        self.scanLines.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)
        yPos = 0
        while yPos < config.HEIGHT:
            self.scanLines.blit(scanline, (0, yPos))
            yPos += self.lineHeight

        self.scanLines.blit(self.scanLines, (0, 0), None, pygame.BLEND_RGB_MULT)
        self.scanLines = self.scanLines.convert_alpha()
        self.scanLines.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)

        # Start humming sound:
        if config.SOUND_ENABLED:
            self.humSound = pygame.mixer.Sound('sounds/pipboy_hum.wav')
            self.humSound.play(loops=-1)
            self.humVolume = self.humSound.get_volume()

            self.distortLineHeight = (config.HEIGHT // 4)
            self.distortLine = pygame.transform.smoothscale(pygame.image.load('images/pipboydistorteffectmap.png'), (config.WIDTH, self.distortLineHeight))
            self.distortLine = self.distortLine.convert()
            self.distortY = -self.distortLineHeight
            self.distortSpeed = (config.HEIGHT / 40)
            self.overlayFrames = []

            print("START")

            cmdLine = CmdLineClass(self)

            bootPrintQueue = [
                "WELCOME TO ROBCO INDUSTRIES (TM) TERMLINK",
                ">SET TERMINAL/INQUIRE",
                "", "RIT-V300", "",
                ">SET FILE/PROTECTION=OWNER:RWED ACCOUNTS.F",
                ">SET HALT RESTART/MAINT",
                "",
                "Initializing Robco Industries(TM) MF Boot Agent v2.3.0",
                "RETROS BIOS",
                "RBIOS-4.02.08.00 52EE5.E7.E8",
                "Copyright 2201-2203 Robco Ind.",
                "Uppermem: 64 KB",
                "Root (5A8)",
                "Maintenance Mode",
                "",
                ">RUN DEBUG/ACCOUNTS.F",
                "**cls",
                "ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM",
                "COPYRIGHT 2075-2077 ROBCO INDUSTRIES",
                "",
            ]

            lineNum = 0
            canPrint = True
            genOverlays = True
            while (canPrint or genOverlays):
                if canPrint:
                    thisLine = bootPrintQueue[lineNum]
                    cmdLine.printText(thisLine)
                    lineNum += 1
                    canPrint = (lineNum < len(bootPrintQueue))
                if genOverlays:
                    if (self.distortY < config.HEIGHT):
                        thisFrame = self.scanLines.convert()
                        thisFrame.blit(self.distortLine, (0, self.distortY), None, pygame.BLEND_RGB_ADD)
                        thisFrame.fill(config.TINTCOLOUR, None, pygame.BLEND_RGB_MULT)
                        thisFrame = thisFrame.convert()
                        self.overlayFrames.append(thisFrame)
                        self.distortY += self.distortSpeed
                    else:
                        genOverlays = False

            self.animDelayFrames = len(self.overlayFrames)
            self.overlayFramesCount = (2 * self.animDelayFrames)
            self.frameNum = 0
            print("END GENERATE")

            cmdLine.printText(">MAPS.DOWNLOAD INIT")
            cmdLine.printText("\tDownloading Local map...")
            cmdLine.printText("\tDownloading World map...")
            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/start.wav').play()
            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/stop.wav').play()

            cmdLine.printText(">PIP-BOY.INIT")

            if not config.QUICKLOAD:
                self.showBootLogo()

            if config.SOUND_ENABLED:
                pygame.mixer.Sound('sounds/start.wav').play()
            print("END INIT PROCESS")

    def showBootLogo(self):
        bootLogo = pygame.image.load('images/bootupLogo.png')
        self.focusInDraw(bootLogo)

        if config.SOUND_ENABLED:
            bootSound = pygame.mixer.Sound('sounds/falloutBootup.wav')
            bootSound.play()

        pygame.display.update()
        pygame.time.wait(4200)

    def focusInDraw(self, canvas):
        self.frameNum = 0
        def divRange(val):
            while val >= 1:
                yield val
                val //= 2

        maxDiv = 2
        hicolCanvas = canvas.convert(24)
        for resDiv in divRange(maxDiv):
            blurImage = pygame.transform.smoothscale(hicolCanvas,
                (self.native_size[0] // resDiv, self.native_size[1] // resDiv))
            blurImage = pygame.transform.smoothscale(blurImage,
                (self.native_size[0] // resDiv, self.native_size[1] // resDiv))
            multVal = (255 // (1 * maxDiv))
            drawImage = canvas.convert()
            drawImage.fill((multVal, multVal, multVal), None, pygame.BLEND_RGB_MULT)
            drawImage.blit(blurImage, (multVal, multVal), None, pygame.BLEND_RGB_ADD)

            if (self.background != None):
                drawImage.blit(self.background, (0, 0), None, pygame.BLEND_RGB_ADD)
                self.background = pygame.transform.smoothscale(self.background, self.native_size)
                self.background = self.background.convert_alpha()
                self.background.fill((config.TINTCOLOUR), None, pygame.BLEND_RGB_MULT)

            drawImage.blit(self.overlayFrames[0], (0, 0), None, pygame.BLEND_RGB_MULT)
            scaled_image = pygame.transform.scale(drawImage, self.screen_size)
            self.screen.blit(scaled_image, (0, 0))
            pygame.display.update()

    def render(self):
        if self.last_render_time == 0:
            self.last_render_time = time.time()
            return 0
        else:
            interval = time.time() - self.last_render_time
            self.last_render_time = time.time()
        
        self.root_children.clear(self.canvas, self.background)
        self.root_children.render(interval)
        self.root_children.draw(self.canvas)
        for group in self.groups:
            group.render(interval)
            group.draw(self.canvas)
            
        scaled_canvas = pygame.transform.scale(self.canvas, self.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))
        
        pygame.display.flip()
        return interval

    def update(self):
        self.root_children.update()
        for group in self.groups:
            group.update()

    def add(self, group):
        if group not in self.groups:
            self.groups.append(group)

    def remove(self, group):
        if group in self.groups:
            self.groups.remove(group)


# --- MODIFICATION START ---
# The class was named EntityGroup, but the project expects it to be 'Group'.
# Renaming it here to match.
class Group(pygame.sprite.LayeredDirty):
# --- MODIFICATION END ---
    def render(self, interval):
        for entity in self:
            entity.render(interval)

    def move(self, x, y):
        for child in self:
            child.rect.move(x, y)


class Entity(pygame.sprite.DirtySprite):
    def __init__(self, dimensions=(0, 0), layer=0, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.image = pygame.surface.Surface(dimensions)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.child_groups = Group() # <-- MODIFICATION: Use the corrected Group class name
        self.layer = layer
        self.dirty = 2
        self.blendmode = pygame.BLEND_RGBA_ADD

    def render(self, interval=0, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def __le__(self, other):
        if type(self) == type(other):
            return self.label <= other.label
        else:
            return 0

    def __str__(self):
        return "Entity"