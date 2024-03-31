import time

import mini_game
from sprite import *


def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(bg, (0, 0))
    screen.blit(sprite.image, sprite.rect)

    text1 = font.render(text[text_number], True, pg.Color(255, 255, 255))
    screen.blit(text1, (280, 450))

    if text_number < len(text) - 1:
        text2 = font.render(text[text_number + 1], True, pg.Color(255, 255, 255))
        screen.blit(text2, (280, 470))


pg.init()
pg.mixer.init()

size = (900, 550)
screen = pg.display.set_mode(size)
pg.display.set_caption("Спасение города")

FPS = 120
clock = pg.time.Clock()

is_running = True
mode = "start_scene"

water_balls = pg.sprite.Group()
water_balls_horizontal = pg.sprite.Group()
fireballs = pg.sprite.Group()

start_text = ["Мы засекли сигнал с города Smart City.",
              "",
              "Наши друзья, дружелюбные хакатоновцы",
              "нуждаются в помощи.",
              "Природные катаклизмы хотят уничтожить",
              "наш прекрасный город,",
              "Как долго наш народ страдал от них, ",
              "теперь и смартситяне в беде...",
              "Мы должны помочь им.",
              "Выходим прямо сейчас.",
              "Спасибо, что починила машину, Зоя.",
              "Но тебе нужно сходить за ней на парковку.",
              "И зарядить её кристаллами. Вперёд!"]

human_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Вода уже начала топить город...",
              "Скоро вода дойдёт до сервера",
              "Спасите смартситян!", ]

middle_text = ["Девачки, я полетела!"
               ]

final_text = ["Огромное тебе спасибо,",
              "дорогая, Зоя!",
              "Как тебя отблагодарить?",
              "В любом случае, ",
              "теперь наш город спасен!",
              "Мы хотим отблагодарить тебя.",
              "Изобретатель Зоя получает",
              "орден SECON.",
              "А также ящик наших",
              "лучших запчастей",
              "",
              ""]

fi_final_text = ["Рада стараться",
                 "Нужна будет помощь, вы знаете кого звать",
                 "Вы знаете кого звать",
                 ""
                 ]

text_number = 0

bg = pg.image.load('Resourses/images/backgroundImage/фон.png').convert()
bg = pg.transform.scale(bg, size)

game_over_bg = pg.image.load('Resourses/images/backgroundImage/game_over.jpg').convert()
game_over_bg = pg.transform.scale(game_over_bg, size)

heart = pg.image.load('Resourses/images/inGame/heart.png').convert_alpha()
heart = pg.transform.scale(heart, (30, 30))
heart_count = 5

burn = pg.mixer.Sound('Resourses/sounds/inGame/burn.wav')
burn.set_volume(0.4)
laser_sound = pg.mixer.Sound('Resourses/sounds/inGame/звук лазера.wav')
win_sound = pg.mixer.Sound('Resourses/sounds/inGame/звук победы.wav')
pg.mixer.music.load('Resourses/sounds/backgroundSound/музыка.wav')
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play()

font = pg.font.Font('Resourses/fonts/Merriweather-Black.ttf', 20)

captain = Captain()
human = Human()
zoi = Zoi()
starship = Starship()

game_over = False

while is_running:
    if game_over == True:
        screen.blit(game_over_bg, (0, 0))
        game_over_text = mini_game.big_font.render('GAME OVER', True, "red")
        screen.blit(game_over_text, (350, 220))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False

        pg.display.flip()
        clock.tick(FPS)
    else:
        # СОБЫТИЯ
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if mode == 'start_scene':
                    text_number += 2
                    if text_number > len(start_text) - 1:
                        text_number = 0
                        mini_game_bool = mini_game.mini_game()
                        if not mini_game_bool:
                            game_over = True
                        else:
                            mode = 'middle_scene'
                        start_time = time.time()

                elif mode == 'middle_scene':
                    text_number += 2
                    if text_number > len(middle_text) - 1:
                        text_number = 0
                        mode = "water_1"

                elif mode == 'human_scene':
                    text_number += 2
                    if text_number > len(human_text) - 1:
                        text_number = 0
                        starship.switch_mode()
                        mode = 'water_2'

                if mode == 'water_2':
                    if event.key == pg.K_SPACE:
                        fireballs.add(Fireball(starship.rect.midtop))
                        laser_sound.play()

                if mode == 'final_scene':
                    text_number += 2
                    if text_number > len(final_text) - 2:
                        text_number = 0
                        mode = 'fi_final_scene'

                if mode == 'fi_final_scene':
                    text_number += 2
                    if text_number > len(fi_final_text) - 2:
                        text_number = 0
                        mode = 'end'

        # ОБНОВЛЕНИЯ
        if mode == "start_scene":
            dialogue_mode(captain, start_text)

        if mode == "water_1":
            if time.time() - start_time >= 15.0:
                mode = 'human_scene'

            if random.randint(1, 60) == 1:
                water_balls.add(WaterBall())

            starship.update()
            water_balls.update()

            hits = pg.sprite.spritecollide(starship, water_balls, True)
            for hit in hits:
                heart_count -= 1
                burn.play()
                if heart_count <= 0:
                    game_over = True

            screen.blit(bg, (0, 0))
            screen.blit(starship.image, starship.rect)
            water_balls.draw(screen)

            for i in range(heart_count):
                screen.blit(heart, (i * 30, 0))

        if mode == "human_scene":
            dialogue_mode(human, human_text)

        if mode == "middle_scene":
            text_number = 0
            dialogue_mode(zoi, middle_text)

        if mode == "water_2":
            if time.time() - start_time >= 30.0:
                mode = 'final_scene'
                pg.mixer.music.fadeout(3)
                win_sound.play()

            if random.randint(1, 40) == 1:
                water_balls_horizontal.add(WaterBallHorizontal())

            starship.update()
            water_balls_horizontal.update()
            fireballs.update()

            hits = pg.sprite.spritecollide(starship, water_balls_horizontal, True)
            for hit in hits:
                heart_count -= 1
                burn.play()
                if heart_count <= 0:
                    game_over = True

            hits = pg.sprite.groupcollide(fireballs, water_balls_horizontal, True, True)

            screen.blit(bg, (0, 0))
            screen.blit(starship.image, starship.rect)
            water_balls_horizontal.draw(screen)
            fireballs.draw(screen)

            for i in range(heart_count):
                screen.blit(heart, (i * 30, 0))

        if mode == "final_scene":
            dialogue_mode(human, final_text)

        if mode == "fi_final_scene":
            text_number = 0
            human.kill()
            dialogue_mode(zoi, fi_final_text)

        pg.display.flip()
        clock.tick(FPS)
