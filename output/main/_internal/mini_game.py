import sys

import pygame
import random as r

pygame.init()
width, height = 900, 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Кто читает тот умрет')
clock = pygame.time.Clock()

heat_sound = pygame.mixer.Sound('Resourses/sounds/inGame/snd_curtgunshot.ogg')
small_font = pygame.font.Font('Resourses/fonts/Minecraft Rus NEW.otf', 20)
big_font = pygame.font.Font('Resourses/fonts/Minecraft Rus NEW.otf', 40)

player = pygame.sprite.Group()
attack1 = pygame.sprite.Group()
crystals = pygame.sprite.Group()
ground = pygame.sprite.Group()
cave = pygame.sprite.Group()
hearts = pygame.sprite.Group()


class Ground(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/backgroundImage/ground.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -10, 450


class Cave(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/backgroundImage/cave.jpg')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/inGame/woman.png')
        self.image = pygame.transform.scale(self.image, (40, 120))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 450, 350
        self.hp = 3

    def update(self, move):
        if move == 'left':
            self.rect = self.rect.move(-4, 0)
        if move == 'right':
            self.rect = self.rect.move(4, 0)

    def heat(self):
        if pygame.sprite.spritecollideany(self, attack1):
            heat_sound.play()
            self.hp -= 1

        if pygame.sprite.spritecollideany(self, crystals):
            global count
            count += 1

        if pygame.sprite.spritecollideany(self, hearts):
            if self.hp < 3:
                self.hp += 1

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def set_x(self, move):
        self.rect.x = move

    def set_y(self, move):
        self.rect.y = move

    def get_hp(self):
        return self.hp


class Stone(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/inGame/stone.png')
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(0, 900)
        self.rect.y = 0
        self.ban = False

    def update(self):
        self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, player):
            self.ban = True

    def get_ban(self):
        return self.ban


class Crystal(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/inGame/diamond.png')
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(0, 900)
        self.rect.y = 0
        self.ban = False

    def update(self):
        self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, player):
            self.ban = True

    def get_ban(self):
        return self.ban


class Heart(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Resourses/images/inGame/hp.png')
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(0, 900)
        self.rect.y = 0
        self.ban = False

    def update(self):
        self.rect = self.rect.move(0, 3)
        if pygame.sprite.spritecollideany(self, player):
            self.ban = True

    def get_ban(self):
        return self.ban


count = 0
pike = pygame.USEREVENT
pygame.time.set_timer(pike, 500)
heart = Player(player)
Ground(ground)
Cave(cave)
music_cave = pygame.mixer.Sound('Resourses/sounds/backgroundSound/music_cave.mp3')


def mini_game():
    timer = 60
    tick = 0
    running = True
    pygame.mixer.init()

    music_cave.play(loops=-1)
    while running:
        screen.fill('black')
        cave.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pike:
                if tick % 2 == 0:
                    timer -= 1
                tick += 1
                rand = r.randint(1, 10)
                if rand in [9, 10]:
                    Crystal(crystals)
                elif rand == 1:
                    Heart(hearts)
                else:
                    Stone(attack1)

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and heart.rect.left > 0:
            player.update('left')
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and heart.rect.right < 900:
            player.update('right')

        for i in attack1:
            if i.get_ban():
                attack1.remove(i)
        for i in crystals:
            if i.get_ban():
                crystals.remove(i)
        for i in hearts:
            if i.get_ban():
                hearts.remove(i)

        if heart.get_hp() == 0:
            running = False
            pygame.quit()
            sys.exit()

        if timer == 0:
            return True

        attack1.draw(screen)
        attack1.update()
        crystals.draw(screen)
        crystals.update()
        hearts.draw(screen)
        hearts.update()

        ground.draw(screen)

        player.draw(screen)
        heart.heat()

        crystal_text = small_font.render(f'У вас {count} кристалл', True, 'white')
        hp_text = small_font.render(f'У вас {heart.get_hp()} HP', True, 'white')
        timer_text = big_font.render(f'{timer}', True, 'white')

        screen.blit(crystal_text, (50, 50))
        screen.blit(hp_text, (50, 100))
        screen.blit(timer_text, (300, 50))

        pygame.display.flip()
        clock.tick(60)
