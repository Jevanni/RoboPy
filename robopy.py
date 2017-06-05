# Python programming gaming highly inspired by robocode game
# http://robocode.sourceforge.net

import os
import glob
import imp
import math

from collections import defaultdict
from threading import Thread

import pygame
from pygame.locals import *

from game_constants import *

class RobotPyException(Exception) :
    pass

class TankThread(Thread) :

    def __init__(self, tank_object) :
        Thread.__init__(self)
        self.tank = tank_object

    def run(self) :
        while True :
            self.tank.run()

class Game() :

    def __init__(self) :

        self.sprites_group = pygame.sprite.Group()

        self.init_field()
        self.init_tank()
        self.launch()

    @staticmethod
    def equal_positions_circle(height, width, offset, number) :
        # return the positions of n individuals using an hypothetic circle
        # of radius min(width, height) - offset
        # return also the angle for the individuals to look at the center

        radius = (min((width, height)) - offset - TANK_SIZE) / 2.
        center_position = cp = (width / 2., height / 2.)
        angle = (2 * math.pi) / number

        positions = [(cp[0] + radius * math.cos(angle * i),
        cp[1] + radius * math.sin(angle * i))
        for i in range(number)]

        angles = [math.degrees(math.pi - (angle * i + math.pi / 2))
        for i in range(number)]

        return positions, angles

    def init_field(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.screen.fill((255, 255, 255))

    def init_tank(self) :
        dname = os.path.dirname(os.path.realpath(__file__))
        fnames = os.path.join(dname, "robots", "*.py")
        fnames = [fname for fname in glob.glob(fnames) if os.path.basename(fname) != "template.py"]

        fnames = fnames * 2

        if len(fnames) < 2 :
            raise RobotPyException("More than one robot must be initialized to run the game")

        ip, angles = Game.equal_positions_circle(MAP_HEIGHT, MAP_WIDTH,
        POSITION_OFFSET, len(fnames))

        tanks = []
        for idx, fname in enumerate(fnames) :
            module = imp.load_source("robot_module_%i" %idx, fname)
            tanks.append(module.Robot(TANK_LIFE, angles[idx], ip[idx], TANK_SIZE,
            self.sprites_group))

        self.threads = [TankThread(tank) for tank in tanks]

    def split_sprites(self) :
        # return the current sprites in different distinct group
        # based on their kind
        # usefull for correct drawing

        self.sprites_groups = defaultdict(pygame.sprite.Group)
        for sprite in self.sprites_group :
            self.sprites_groups[sprite.kind].add(sprite)

    def draw_sprites(self) :
        sprites_order = ["radar", "base", "turret"]
        for kind in sprites_order :
            self.sprites_groups[kind].draw(self.screen)

    def launch(self) :
        clock = pygame.time.Clock()
        done = False

        self.split_sprites()

        while not done :

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            self.draw_sprites()
            pygame.display.flip()
            clock.tick(10)

game = Game()
pygame.quit()
