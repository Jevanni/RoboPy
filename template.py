import os
import pygame

# http://xorobabel.blogspot.fr/2012/10/pythonpygame-2d-animation-jrpg-style.html

class SpriteProjectile(pygame.sprite.Sprite) :

    def __init__(self, launcher, starting_position, speed) :
        self.launcher = launcher
        self.position = starting_position
        self.speed = speed

    def move(self) :
        pass

    def hit_robot(self) :
        pass

class SpriteObject(pygame.sprite.Sprite) :

    def __init__(self, kind, parent, * args) :
        super(SpriteObject, self).__init__()

        self.image = self.get_image(* args)
        self.rect = self.image.get_rect()
        self.kind = kind
        self.parent = parent

    def set_position(self, x, y) :
        self.rect.center = (x, y)

    def get_position(self) :
        return self.rect.center

    def set_angle(self, radius) :
        self.image = pygame.transform.rotate(self.image, radius)
        self.make_rect_again()

    def make_rect_again(self) :
        x, y = self.get_position()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def get_image_size(self) :
        return (self.image.get_width(),
        self.image.get_height())

class SpriteImage(SpriteObject) :

    def get_image(self, basename) :
        dname = os.path.dirname(os.path.realpath(__file__))
        fname = os.path.join(dname, "img", basename)
        return pygame.image.load(fname)

    def resize(self, size) :
        width, height = self.get_image_size()
        max_size = max(width, height)
        prc = max_size / float(size)

        new_size = (int(width / prc), int(height / prc))
        self.image = pygame.transform.scale(self.image, new_size)

class SpriteRadar(SpriteObject) :

    def set_position(self, x, y) :
        pass

    def set_angle(self, radius) :
        pass

    def get_image(self, angle, range) :
        pass

class Robot(pygame.sprite.Sprite) :

    def __init__(self, life, radius, positions, size, sprites_group) :
        super(Robot, self).__init__()

        self.name = None
        self.author = None

        self.life = life
        self.base_radius = self.turret_radius = radius
        self.positions = positions
        self.sprites_group = sprites_group

        self.setup_sprites(size)

    def setup_sprites(self, size) :
        self.tank_base = SpriteImage("base", self, "Tank_Blue_NT.png")
        self.tank_base.resize(size)
        self.tank_base.set_position(* self.positions)
        self.tank_base.set_angle(self.base_radius)
        self.sprites_group.add(self.tank_base)

        self.tank_turret = SpriteImage("turret", self, "Tank_Turret_Green.png")
        self.tank_turret.resize(size)
        self.tank_turret.set_position(* self.positions)
        self.tank_turret.set_angle(self.turret_radius)
        self.sprites_group.add(self.tank_turret)



    # Action functions

    def turn_componments(self, radius, robot=True, turret=False, radar=False) :
        pass

    def move_forward(self, distance) :
        pass

    def move_backward(self, distance) :
        pass

    def shoot(self, power) :
        pass

    def distance_to_position(self, position) :
        pass

    def stop(self) :
        pass

    def is_colliding(self) :
        pass

    # TO OVERRIDE

    def ishit(self) :
        pass

    def detect_enemy(self, position) :
        pass

    def run(self) :
        pass

    def hit_robot(self) :
        pass

    def collide(self) :
        pass
