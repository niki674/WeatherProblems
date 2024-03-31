import random

import pygame as pg


class WaterBall(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/water.png")
        self.image = pg.transform.rotate(self.image, 270)
        size = random.randint(70, 150)

        self.image = pg.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.topleft = (800, random.randint(0, 600 - size))

        self.speedx = random.randint(1, 3)
        self.speedy = random.randint(-1, 1)

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy


class WaterBallHorizontal(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/water.png")
        size = random.randint(70, 150)

        self.image = pg.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.randint(0, 600 - size), 0)

        self.speedx = random.randint(-1, +1)
        self.speedy = random.randint(1, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Fireball(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/ball.png")

        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect(midbottom=pos)

        self.speed = 2

    def update(self):
        self.rect.y -= self.speed


class Starship(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/cosmolet.png")
        self.image = pg.transform.rotate(self.image, 270)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.image = pg.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.rect.midleft = (0, 300)

        self.mode = "vertical"

    def update(self):
        keys = pg.key.get_pressed()
        if self.mode == "horizontal":
            if (keys[pg.K_a] or keys[pg.K_LEFT]) and self.rect.left > 0:
                self.rect.x -= 5
            if (keys[pg.K_d] or keys[pg.K_RIGHT]) and self.rect.right < 900:
                self.rect.x += 5

        if self.mode == "vertical":
            if (keys[pg.K_w] or keys[pg.K_UP]) and self.rect.top > 0:
                self.rect.y -= 5
            if (keys[pg.K_s] or keys[pg.K_DOWN]) and self.rect.bottom < 550:
                self.rect.y += 5

    def switch_mode(self):
        self.image = pg.image.load("Resourses/images/inGame/cosmolet.png")
        self.image = pg.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (400, 580)

        self.mode = "horizontal"


class Captain(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/captain.png")
        self.image = pg.transform.scale(self.image, (400, 400))

        self.rect = self.image.get_rect()
        self.rect.topleft = (-30, 600)

        self.mode = "up"

    def update(self):
        if self.mode == "up":
            self.rect.y -= 3
            if self.rect.y <= 300:
                self.mode = "stay"


class Human(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/human.png")
        self.image = pg.transform.scale(self.image, (400, 400))

        self.rect = self.image.get_rect()
        self.rect.topleft = (-30, 600)

        self.mode = "up"

    def update(self):
        if self.mode == "up":
            self.rect.y -= 3
            if self.rect.y <= 300:
                self.mode = "stay"


class Zoi(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("Resourses/images/inGame/woman.png")
        self.image = pg.transform.scale(self.image, (100, 400))

        self.rect = self.image.get_rect()
        self.rect.topleft = (150, 600)

        self.mode = "up"

    def update(self):
        if self.mode == "up":
            self.rect.y -= 3
            if self.rect.y <= 300:
                self.mode = "stay"
