import os
import sys

import pygame
import pygame_gui
import win32con
import win32api
import win32gui

pygame.init()
vertical_borders_1 = pygame.sprite.Group()
vertical_borders_2 = pygame.sprite.Group()
horizontal_borders_1 = pygame.sprite.Group()
horizontal_borders_2 = pygame.sprite.Group()
surface_for_person = pygame.sprite.Group()
evil = pygame.sprite.Group()
hero = pygame.sprite.Group()


class Download:
    def __init__(self, width, height, font, text_download):
        self.main_text = None
        self.font = font
        self.height = height
        self.width = width
        self.text_d = text_download
        self.run = True
        self.count = 0
        self.time = 1
        self.text_pr = ""
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.one = (1, 2, 3)
        self.info_win = pygame.display.get_wm_info()["window"]
        self.start_time = pygame.time.get_ticks()
        Download.process(self)
    def process(self):
        win32gui.SetWindowLong(self.info_win, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(self.info_win, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.info_win, win32api.RGB(*self.one), 0, win32con.LWA_COLORKEY)
        Download.text(self)
    def text(self):
        self.main_text = self.font.render("COLLOSYM", False, (249, 166, 2))
        self.main_text_coord = self.main_text.get_rect()
        self.main_text_coord.x = self.width // 3 + 70
        self.main_text_coord.y = self.height // 3
        Download.start_process(self)
    def start_process(self):
        while self.run:
            self.screen.fill(self.one)
            seconds = pygame.time.get_ticks() / 1000
            if self.count <= 4:
                if seconds > self.time:
                    self.text_pr = pygame.font.Font("data/Font_start_process.ttf", 15).render(self.text_d[self.count],
                                                                                              False,
                                                                                              (128, 128, 128))
                    self.text_coord = self.text_pr.get_rect()
                    self.text_coord.x = self.width // 3 + 180
                    self.text_coord.y = self.height // 3 + 60
                    self.count += 1
                    self.time += 1
                    self.screen.blit(self.text_pr, self.text_coord)
            if self.count >= 4 and seconds > self.time:
                self.run = False
                Start(self.width, self.height, 60)
                self.screen.fill(self.one)
                sys.exit()
            if self.text_pr != "":
                self.screen.blit(self.text_pr, self.text_coord)
            self.screen.blit(self.main_text, self.main_text_coord)
            pygame.display.flip()
class Return_Menu():
    def __init__(self, width, height):
        df = Start(width, height, 60)
        df.stack()
        df.window()
class Confirmation_Of_Exiting_The_Game():
    def __init__(self, width, height, manager):
        self.confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((width // 3 - 50, height // 3 - 100), (width // 3 + 120, height // 3 + 100)),
            manager=manager, window_title="Подтверждение",
            action_short_name="OK",
            blocking=True,
            action_long_desc="Вы уверены что хотите выйти?")
class Expert_Image():
    def __init__(self, name_image, colorkey=None):
        self.colorkey = colorkey
        self.file = "data"
        self.name_image = name_image
    def load_image(self):
        sss = os.path.join(self.file, self.name_image)
        if not os.path.isfile(sss):
            print(f'файл {sss} не найден')
            sys.exit()
        image = pygame.image.load(sss)
        if self.colorkey is not None:
            image = image.convert()
            if self.colorkey == -1:
                self.colorkey = image.get_at((0, 0))
            image.set_colorkey(self.colorkey)
        else:
            image = image.convert_alpha()
        return image
class Start:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.label = ["C", "O", "L", "L", "O", "S", "Y", "M"]
        self.font = pygame.font.Font("data/press-start-k.ttf", 30)
        Start.stack(self)
    def stack(self):
        self.time = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menu = True
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.button_play = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 3, self.height // 3 + 200), (500, 50)),
            text="PLAY",
            manager=self.manager)
        self.button_exit_menu = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 3, self.height // 3 + 250), (500, 50)),
            text="EXIT", manager=self.manager)
        pygame.mixer.init()
        pygame.mixer.music.load("data/05eeddac8c4a1ef.wav")
        pygame.mixer.music.play(-1)
        Start.window(self)
    def kill_button_menu(self):
        self.button_exit_menu.kill()
        self.button_play.kill()
    def img(self):
        self.image = Expert_Image('background_evil.gif').load_image()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
    def window(self):
        while self.menu:
            Start.img(self)
            self.screen.blit(self.image, self.rect)
            x = 580
            y = 350
            for label in self.label:
                label_text = self.font.render(label, 1, (249, 166, 2))
                coord_label_text = label_text.get_rect()
                coord_label_text.y = y
                coord_label_text.x = x
                x += 50
                self.screen.blit(label_text, coord_label_text)
            self.time_delta = self.time.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.button_play:
                            Start.kill_button_menu(self)
                            self.menu = False
                            Rules(self.width, self.height, self.time_delta)
                        if event.ui_element == self.button_exit_menu:
                            self.menu = False
                self.manager.process_events(event)
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            self.time.tick(60)
            pygame.display.flip()
class Rules:
    def __init__(self, width, height, time_delta):
        self.time_delta = time_delta
        self.width = width
        self.time = pygame.time.Clock()
        self.height = height
        self.fps = 60
        self.rules = True
        self.font = pygame.font.Font("data/F77 Minecraft.ttf", 30)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.zaderzhka = 0
        Rules.display(self)
    def text_display(self):
        text_rules_hero_1 = ["W - взлёт персонажа",
                             "A - движение направо",
                             "D - движение налево",
                             "F - атака героя"
                             ]
        text_rules_hero_2 = [
            "стрелка вверх - взлёт персонажа",
            "правая стрелка - движение направо",
            "левая стрелка - движение налево",
            "L - атака героя"
        ]
        x = 50
        y = 200
        main_text = self.font.render("ПРAВИЛА ИГРЫ", 1, pygame.Color("white"))
        self.screen.blit(main_text, main_text.get_rect(center=(self.width // 2, 50)))
        rules_hero_1 = self.font.render("ДВИЖЕНИЕ 1 ИГРОКА", 1, pygame.Color("white"))
        self.screen.blit(rules_hero_1, rules_hero_1.get_rect(center=(300, 150)))
        rules_hero_2 = self.font.render("ДВИЖЕНИЕ 2 ИГРОКА", 1, pygame.Color("white"))
        self.screen.blit(rules_hero_2, rules_hero_2.get_rect(center=(1100, 150)))
        main_text = self.font.render("ДЛЯ ВЫХОДА ИЗ ИГРЫ НАЖМИТЕ Esc", 1, pygame.Color("white"))
        self.screen.blit(main_text, main_text.get_rect(center=(self.width // 2, 650)))
        for text in text_rules_hero_1:
            print_text = self.font.render(text, 1, pygame.Color("white"))
            coord_rect_text = print_text.get_rect()
            coord_rect_text.x = x
            coord_rect_text.y = y
            y += 100
            self.screen.blit(print_text, coord_rect_text)
        x = 800
        y = 200
        for text in text_rules_hero_2:
            print_text = self.font.render(text, 1, pygame.Color("white"))
            coord_rect_text = print_text.get_rect()
            coord_rect_text.x = x
            coord_rect_text.y = y
            y += 100
            self.screen.blit(print_text, coord_rect_text)
    def display(self):
        while self.rules:
            self.zaderzhka += 1
            self.screen.fill((0, 0, 0))
            Rules.text_display(self)
            self.time.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Confirmation_Of_Exiting_The_Game(self.width, self.height, self.manager)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        self.rules = False
                self.manager.process_events(event)
            self.manager.update(self.time_delta)
            self.manager.draw_ui(self.screen)
            if self.zaderzhka == 300:
                self.rules = False
                Play_Game(self.width, self.height, self.time_delta)
            pygame.display.flip()
class SurfaceForPerson(pygame.sprite.Sprite):
    def __init__(self, center_width, center_height):
        pygame.sprite.Sprite.__init__(self)
        self.add(surface_for_person)
        self.image = pygame.Surface((990, 1))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(center=(center_width, center_height))
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        if y1 == 90:
            self.add(vertical_borders_1)
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == -90:
            self.add(vertical_borders_2)
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y2 == 0:
            self.add(horizontal_borders_2)
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else:
            self.add(horizontal_borders_1)
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
class Evil(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(evil)
        self.atacks = False
        self.image = image
        self.frames = []
        self.flip = 1
        self.rect = self.image.get_rect(center=(x, y))
        self.gif = 0
        self.scht = 0
        self.width = width
        self.height = height
        self.gravity = True
        self.atacks = False
        self.trigger = False
        self.hp_hero_2 = 100
        self.daent = False
        self.death = False
    def checked_left_and_right(self, key_down, character):
        if self.gravity:
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1) or pygame.sprite.spritecollideany(self,
                                                                                                        surface_for_person):
            self.gravity = False
        else:
            self.gravity = True
        if (self.gif >= 7 and key_down[pygame.K_LEFT]) or (self.gif >= 7 and key_down[pygame.K_RIGHT]):
            self.gif = 0
            Evil.update(self, key_down, self.flip, character)
        elif key_down[pygame.K_LEFT] and self.gif < 7:
            self.flip = 2
            Evil.update(self, key_down, self.flip, character)
            self.gif += 1
        elif key_down[pygame.K_RIGHT] and self.gif < 7:
            self.flip = 1
            Evil.update(self, key_down, self.flip, character)
            self.gif += 1
    def atack(self):
        Evil.animation(self, 8, 1, f"Attack_evil_hero_{self.flip}", self.flip)
        self.gif += 1
        if pygame.sprite.spritecollideany(self, hero):
            self.trigger = True
            self.daent = True
        else:
            self.trigger = False
    def idle(self, character):
        if self.gravity:
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1) or pygame.sprite.spritecollideany(self,
                                                                                                        surface_for_person):
            self.gravity = False
        else:
            self.gravity = True
        if self.gif >= 7:
            self.gif = 0
            Evil.animation(self, 8, 1, f"{character}{self.flip}", self.flip)
        else:
            Evil.animation(self, 8, 1, f"{character}{self.flip}", self.flip)
            self.gif += 1
    def hit(self):
        Evil.animation(self, 4, 1, f"Take Hit_2_{self.flip}", self.flip)
        self.gif += 1
        if self.daent == False:
            self.hp_hero_2 -= 1
            self.daent = True
    def update(self, *args):
        if self.gravity:
            self.rect = self.rect.move(0, 15)
            if pygame.sprite.spritecollideany(self, horizontal_borders_1):
                self.gravity = False
            else:
                self.gravity = True
        if args[0][pygame.K_RIGHT] and pygame.sprite.spritecollideany(self, vertical_borders_1):
            self.rect.x -= 5
            Evil.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_LEFT] and pygame.sprite.spritecollideany(self, vertical_borders_2):
            self.rect.x += 5
            Evil.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_RIGHT]:
            self.rect = self.rect.move(10, 0)
            Evil.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_LEFT]:
            self.rect = self.rect.move(-10, 0)
            Evil.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
    def jump(self, *args):
        if self.gif >= 7:
            self.gif = 0
            Hero.animation(self, 8, 1, f"{args[2]}{args[1]}", self.flip)
        elif args[0][pygame.K_UP] and pygame.sprite.spritecollideany(self, horizontal_borders_2):
            self.rect.y += 5
            Hero.animation(self, 8, 1, f"{args[2]}{args[1]}", self.flip)
            self.gif += 1
        elif args[0][pygame.K_UP]:
            self.rect = self.rect.move(0, -15)
            Hero.animation(self, 8, 1, f"{args[2]}{args[1]}", self.flip)
            self.gif += 1
    def animation(self, count_column, count_row, name, flip):
        self.frames = []
        self.image = Expert_Image(f"{name}.png").load_image()
        width, height = self.image.get_size()
        w, h = width / count_column, height / count_row
        row = 0
        if flip == 1:
            for j in range(int(height / h)):
                for i in range(int(width / w)):
                    self.frames.append(self.image.subsurface(pygame.Rect(i * w, row, w, h)))
                row += int(h)
        if flip == 2:
            for j in range(int(height / h)):
                for i in range(int(width / w) - 1, -1, -1):
                    self.frames.append(self.image.subsurface(pygame.Rect(w * i, row, w, h)))
                row += int(h)
class Hero(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(hero)
        self.atacks = False
        self.image = image
        self.frames = []
        self.flip = 1
        self.rect = self.image.get_rect(center=(x, y))
        self.gif = 0
        self.scht = 0
        self.width = width
        self.height = height
        self.gravity = True
        self.trigger = False
        self.hp_hero_1 = 100
        self.daent = False
        self.death = False
    def checked_pressed_a_and_d(self, key_down, character):
        if self.gravity:
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1) or pygame.sprite.spritecollideany(self,
                                                                                                        surface_for_person):
            self.gravity = False
        else:
            self.gravity = True
        if (self.gif >= 7 and key_down[pygame.K_a]) or (self.gif >= 7 and key_down[pygame.K_d]):
            self.gif = 0
            Hero.update(self, key_down, self.flip, character)
        elif key_down[pygame.K_a] and self.gif < 7:
            self.flip = 2
            Hero.update(self, key_down, self.flip, character)
            self.gif += 1
        elif key_down[pygame.K_d] and self.gif < 7:
            self.flip = 1
            Hero.update(self, key_down, self.flip, character)
            self.gif += 1
    def hit(self):
        Hero.animation(self, 3, 1, f"Take hit_hero_{self.flip}", self.flip)
        self.gif += 1
        if self.daent == False:
            self.hp_hero_1 -= 1
            self.daent = True
    def atack(self):
        Hero.animation(self, 8, 2, f"Attack{self.flip}", self.flip)
        self.gif += 1
        if pygame.sprite.spritecollideany(self, evil):
            self.trigger = True
            self.daent = True
        else:
            self.trigger = False
    def idle(self, character):
        if self.gravity:
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1) or pygame.sprite.spritecollideany(self,
                                                                                                        surface_for_person):
            self.gravity = False
        else:
            self.gravity = True
        if self.gif >= 7:
            self.gif = 0
            Hero.animation(self, 8, 1, f"{character}{self.flip}", self.flip)
        else:
            Hero.animation(self, 8, 1, f"{character}{self.flip}", self.flip)
            self.gif += 1
    def update(self, *args):
        if self.gravity:
            self.rect = self.rect.move(0, 10)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1) or pygame.sprite.spritecollideany(self,
                                                                                                        surface_for_person):
            self.gravity = False
        else:
            self.gravity = True
        if args[0][pygame.K_d] and pygame.sprite.spritecollideany(self, vertical_borders_1):
            self.rect.x -= 1
            Hero.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_a] and pygame.sprite.spritecollideany(self, vertical_borders_2):
            self.rect.x += 1
            Hero.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_d]:
            self.rect = self.rect.move(10, 0)
            Hero.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
        elif args[0][pygame.K_a]:
            self.rect = self.rect.move(-10, 0)
            Hero.animation(self, 8, 1, f"{args[2]}_{args[1]}", args[1])
    def jump(self, *args):
        if self.gif >= 2:
            self.gif = 0
            Hero.animation(self, 2, 1, f'Jump_hero_1_{args[1]}', args[1])
        elif args[0][pygame.K_w] and pygame.sprite.spritecollideany(self, horizontal_borders_2):
            self.rect.y += 1
            Hero.animation(self, 2, 1, f'Jump_hero_1_{args[1]}', args[1])
        elif args[0][pygame.K_w]:
            self.rect = self.rect.move(0, -10)
            Hero.animation(self, 2, 1, f'Jump_hero_1_{args[1]}', args[1])
    def animation(self, count_column, count_row, name, flip):
        self.frames = []
        self.image = Expert_Image(f"{name}.png").load_image()
        width, height = self.image.get_size()
        w, h = width / count_column, height / count_row
        row = 0
        if flip == 1:
            for j in range(int(height / h)):
                for i in range(int(width / w)):
                    self.frames.append(self.image.subsurface(pygame.Rect(i * w, row, w, h)))
                row += int(h)
        if flip == 2:
            for j in range(int(height / h)):
                for i in range(int(width / w) - 1, -1, -1):
                    self.frames.append(self.image.subsurface(pygame.Rect(w * i, row, w, h)))
                row += int(h)
class Background:
    def __init__(self, x, y):
        self.background = Expert_Image("Background_0.png").load_image()
        self.background = pygame.transform.scale(self.background, (x, y))
        self.rect = self.background.get_rect(center=(x // 2, y // 2))
class Play_Game:
    def __init__(self, width, height, time_delta):
        self.scht_hero_1 = 0
        self.scht_hero_2 = 0
        self.font = pygame.font.Font("data/press-start-k.ttf", 30)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.time_delta = time_delta
        self.fps = pygame.time.Clock()
        self.atack = False
        self.jump = False
        self.hp_pers = 10
        self.hp_pers_2 = 10
        self.pers = Hero(Expert_Image("ussaly_hero_1.png").load_image(), 0,
                         self.height - 300, self.width, self.height)
        self.pers_2 = Evil(Expert_Image("ussaly_hero_2.png").load_image(), self.width - 200, self.height - 300,
                           self.width,
                           self.height)
        Border(0, -80, self.width - 5, 0)
        Border(-100, self.height - 250, self.width - 5, self.height - 250)
        Border(-90, -90, -90, self.height + 90)
        Border(self.width - 90, 90, self.width - 90, self.height - 90)
        SurfaceForPerson(self.width // 2 - 100, self.height // 2 - 200)
        Play_Game.start_game(self)
    def draw_elements(self):
        surface_for_person.draw(self.screen)
        horizontal_borders_1.draw(self.screen)
        horizontal_borders_2.draw(self.screen)
        vertical_borders_1.draw(self.screen)
        vertical_borders_2.draw(self.screen)
    def hp_draw(self):
        x_hero_1 = 100
        x2_hero_1 = self.pers.hp_hero_1 * 3
        x_hero_2 = 1100
        x2_hero_2 = self.pers_2.hp_hero_2 * 3
        y1 = 50
        y2 = 50
        pygame.draw.rect(self.screen, (pygame.Color("red")), (x_hero_1, y1, x2_hero_1, y2))
        pygame.draw.rect(self.screen, (pygame.Color("red")), (x_hero_2, y1, x2_hero_2, y2))
    def score(self):
        score_text_hero_1 = self.font.render(str(self.scht_hero_1), True, pygame.Color("white"))
        score_text_hero_2 = self.font.render(str(self.scht_hero_2), True, pygame.Color("white"))
        score_text_hero_1_rect = score_text_hero_1.get_rect(center=(200, 200))
        score_text_hero_2_rect = score_text_hero_2.get_rect(center=(1200, 200))
        return score_text_hero_1, score_text_hero_2, score_text_hero_1_rect, score_text_hero_2_rect
    def start_game(self):
        while self.run:
            self.screen.blit(Background(self.width, self.height).background,
                             Background(self.width, self.height).rect)
            self.key_down = pygame.key.get_pressed()
            self.time = pygame.time.get_ticks() / 1000
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Confirmation_Of_Exiting_The_Game(self.width, self.height, self.manager)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.pers.atacks = True
                        self.pers.gif = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        self.pers_2.atacks = True
                        self.pers_2.gif = 0
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        self.run = False
                self.manager.process_events(event)
            if self.pers_2.trigger == False:
                if self.pers.atacks:
                    if self.pers.gif > 13:
                        self.pers.gif = 0
                        self.pers.atacks = False
                        self.pers.trigger = False
                    else:
                        self.pers.atack()
                        self.screen.blit(self.pers.frames[self.pers.gif], self.pers.rect)
                        if self.pers.trigger:
                            if self.pers_2.gif > 2:
                                self.pers_2.gif = 0
                                self.pers.trigger = False
                                self.pers_2.daent = False
                            else:
                                self.pers_2.hit()
                                self.screen.blit(self.pers_2.frames[self.pers_2.gif], self.pers_2.rect)
                elif self.pers.hp_hero_1 <= 0:
                    self.pers = Hero(Expert_Image("ussaly_hero_1.png").load_image(), 0,
                                     self.height - 300, self.width, self.height)
                    hero = pygame.sprite.Group()
                    self.pers.hp_hero_1 = 100
                    self.scht_hero_2 += 1
                elif (self.key_down[pygame.K_d]) or (self.key_down[pygame.K_a]):
                    self.pers.checked_pressed_a_and_d(self.key_down, 1)
                    self.screen.blit(self.pers.frames[self.pers.gif], self.pers.rect)
                elif self.key_down[pygame.K_w]:
                    self.pers.jump(self.key_down, self.pers.flip, 1)
                    self.screen.blit(self.pers.frames[self.pers.gif], self.pers.rect)
                else:
                    self.pers.idle("Idle_1pers")
                    self.screen.blit(self.pers.frames[self.pers.gif], self.pers.rect)
            if self.pers.trigger == False:
                if self.pers_2.atacks:
                    if self.pers_2.gif > 6:
                        self.pers_2.gif = 0
                        self.pers_2.atacks = False
                        self.pers_2.trigger = False
                    else:
                        self.pers_2.atack()
                        self.screen.blit(self.pers_2.frames[self.pers_2.gif], self.pers_2.rect)
                        if self.pers_2.trigger:
                            if self.pers.gif > 1:
                                self.pers.gif = 0
                                self.pers_2.trigger = False
                                self.pers.daent = False
                            else:
                                self.pers.hit()
                                self.screen.blit(self.pers.frames[self.pers.gif], self.pers.rect)
                elif self.pers_2.hp_hero_2 <= 0:
                    self.pers_2 = Evil(Expert_Image("ussaly_hero_2.png").load_image(), self.width - 200,
                                       self.height - 300,
                                       self.width,
                                       self.height)
                    self.pers_2.hp_hero_2 = 100
                    self.scht_hero_1 += 1
                    evil = pygame.sprite.Group()
                elif (self.key_down[pygame.K_LEFT]) or (self.key_down[pygame.K_RIGHT]):
                    self.pers_2.checked_left_and_right(self.key_down, 2)
                    self.screen.blit(self.pers_2.frames[self.pers_2.gif], self.pers_2.rect)
                elif self.key_down[pygame.K_UP]:
                    self.pers_2.jump(self.key_down, self.pers_2.flip, "Idle_2pers")
                    self.screen.blit(self.pers_2.frames[self.pers_2.gif], self.pers_2.rect)
                else:
                    self.pers_2.idle("Idle_2pers")
                    self.screen.blit(self.pers_2.frames[self.pers_2.gif], self.pers_2.rect)
            self.screen.blit(Play_Game.score(self)[0], Play_Game.score(self)[2])
            self.screen.blit(Play_Game.score(self)[1], Play_Game.score(self)[3])
            Play_Game.draw_elements(self)
            Play_Game.hp_draw(self)
            self.manager.draw_ui(self.screen)
            self.manager.update(self.time_delta)
            self.fps.tick(20)
            pygame.display.flip()
pygame.quit()
