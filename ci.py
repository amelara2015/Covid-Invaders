#!/usr/bin/env python
# coding: utf-8

"""
#pip install time
про анимацию спрайтов
https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images

про pygame
https://is42-2018.susu.ru/blog/2019/04/29/pygame-shpargalka-dlya-ispolzovaniya/
"""
# In[1]:


import pygame as pg
import pygame.freetype
pg.freetype.init()

from random import randint
pg.init()
#pg.mixer.init()


# In[2]:



class Main():
    
    FPS = 60
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    FON_COLOR = (250, 250, 250)
    
    GAME_STATUS = "new_game" #can be "new_game", "game", "menu", "pause", "game_over", "settigs","quit"

    ACCELERATION_FACTOR = 1
    
    
    if __name__ == "__main__" :
        pg.freetype.init()
        
    #None if pg.font.get_init() else  pg.font.init() #раскоментил для отладки
    AmaticSC32 = pg.freetype.Font("Fonts/AmaticSC-Bold.ttf", 32)
    AmaticSC70 = pg.freetype.Font("Fonts/AmaticSC-Bold.ttf", 70)
    #pg.font.quit()
    
    
    
    def __init__(self):
        pass
    
    
    
    
    @staticmethod
    def get_event():
        sc = pg.display.set_mode((Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT)) 
        sc.fill(FON_COLOR)
        pg.time.Clock().tick(1)
        www = pg.event.get()
        print(www)
    

    
    
    @staticmethod
    def go():
        Main.GAME_STATUS = "menu"
        pg.display.set_caption("Covid Invaiders")
        sc = pg.display.set_mode((Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT))
        pg.mixer.init()
        while True: 
        
            #print(Main.GAME_STATUS)
            if Main.GAME_STATUS == "menu":
                Main._menu(sc)
            if Main.GAME_STATUS == "new_game":
                Main._new_game()


            if Main.GAME_STATUS == "game":
                Main._game(sc)

            if  Main.GAME_STATUS == "next_level":
                Main._next_level()
            
            if Main.GAME_STATUS == "game_over":
                Main._game_over(sc)
            
            if Main.GAME_STATUS == "quit":
                Main.ACCELERATION_FACTOR = 1
                pg.quit()
                return
    @staticmethod
    def _menu(main_surf):
        
        main_surf.fill(Main.FON_COLOR)

        Text.make_menu_text()
        Text.show(main_surf)

        pg.time.Clock().tick(Main.FPS)
        pg.display.update()            

        for event in pg.event.get():
            if Event_handler.quit(event):
                return
            #Event_handler.push_arrow(event, Main.ship1)
            Event_handler.enter(event)
            Event_handler.escape(event)
    
    @staticmethod
    def _new_game():
        Enemy.make_list()
        Enemy.set_swarm()
        Ship.SPRITES = pg.sprite.Group()
        Main.ship1 = Ship()
        Text.make_game_text()#создает поверхности с текстом
        #global ship1
        #global ship2
        #ship2 = Ship()
        Main.GAME_STATUS = "game"
        return

    @staticmethod
    def _game(main_surf):        
        while Main.GAME_STATUS == "game":
            main_surf.fill(Main.FON_COLOR)
            Enemy.move_swarm(main_surf)

            #rrecct = Enemy.SPRITES.sprites()[0].rect # хитбокс элемента из группы спрайтов 
            #pg.draw.rect(sc, (125, 125, 125), rrecct)

            Bullet.update(main_surf)
            Ship.update(main_surf)
            #Text.update()#обновляет поверхности с текстом
            Text.show(main_surf)#накладывает текстовую поверхность на главную поверхность

            pg.time.Clock().tick(Main.FPS*Main.ACCELERATION_FACTOR)
            pg.display.update()            
            #pg.display.flip()

            for event in pg.event.get():
                if Event_handler.quit(event):
                    return
                Event_handler.push_arrow(event, Main.ship1)
                Event_handler.shot(event, Main.ship1)
                if Event_handler.escape(event):
                    return
                
                """
                if event.type == BAH:
                    Main.FON_COLOR = (0,0,0)
                """        
    
    @staticmethod
    def _next_level():        
        Enemy.make_list()
        Enemy.set_swarm()
        #Text.make_game_text()#создает поверхности с текстом
        Main.GAME_STATUS = "game"
        Main.ACCELERATION_FACTOR = 1
        return

    
    @staticmethod
    def _game_over(main_surf):        
        
        menu_surfase = pg.Surface((Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT), pg.SRCALPHA)
        transparency = 150 #задаётся прозрачность меню
        menu_surfase.fill((Main.FON_COLOR + (transparency,))) 

        Text.make_game_over_text()
        Text.show(menu_surfase)

        main_surf.blit(menu_surfase, (0,0))
        
        #pg.time.delay(2000) # 1 second == 1000 milliseconds
        while True:
            pg.time.Clock().tick(Main.FPS*Main.ACCELERATION_FACTOR)
            pg.display.update()            
            #pg.display.flip()

            for event in pg.event.get():
                if Event_handler.quit(event):
                    return
                if Event_handler.any_key(event):
                    return
    
    @staticmethod #масштабирует поверхность
    def scale(img, scale):
        new_width = round(img.get_width() * scale)
        new_height = round(img.get_height() * scale)
        new_img = pg.transform.scale(img, (new_width, new_height))
        return new_img
    
    @staticmethod #отдаёт ректрикт, центрированный по координатам
    def get_center(surf, position, old_rect=None, to_center_x=True, to_center_y=True):
        if old_rect == None:
            old_rect = surf.get_rect()
            old_rect.x = position[0]
            old_rect.y = position[1]
        new_rect = surf.get_rect(center=position)
        new_rect.x = new_rect.x if to_center_x else old_rect.x
        new_rect.y = new_rect.y if to_center_y else old_rect.y
        return new_rect
    
    
    @staticmethod #ускоряет игру в зависимости от числа оставшихся врагов
    def get_acceleration_factor (count_of_living_enemies):
        max_enemy = 55
        max_value = 5
        curvature = 3
        acceleration_factor = (max_value-1)*((max_enemy - count_of_living_enemies) / max_enemy)**curvature+1
        return acceleration_factor    


# In[3]:


class Event_handler():
    def ___init__ ():
        pass
    
    @staticmethod
    def quit(event):
        if event.type == pg.QUIT:
            Main.ACCELERATION_FACTOR = 1
            pg.quit()
            Main.GAME_STATUS = "quit"
            return True
        return False
    
    @staticmethod
    def push_arrow(event, ship):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                ship.motion_vector = -1 #to left
            elif event.key == pg.K_RIGHT:
                ship.motion_vector = 1 #to right
                
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT,
                             pg.K_RIGHT]:
                ship.motion_vector = 0 #to stop
    
    @staticmethod            
    def shot(event, ship):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ship.shot()
                
    @staticmethod            
    def enter(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                Main.GAME_STATUS = "new_game"    
    
    @staticmethod            
    def any_key(event):
        if event.type == pg.KEYDOWN:
            if Main.GAME_STATUS == "game_over":
                Main.GAME_STATUS = "menu"
                return True   
        return False
    
    @staticmethod            
    def escape(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if Main.GAME_STATUS == "game":
                    Main.GAME_STATUS = "menu"
                    return True
                elif Main.GAME_STATUS == "menu":
                    Main.GAME_STATUS = "quit"
                    return True 
                elif Main.GAME_STATUS == "game_over":
                    Main.GAME_STATUS = "menu"
                    return True 
                
        return False  


# In[4]:


class Bullet(pg.sprite.Sprite):
    
    IMG_DICT = {"player1":'Sprites/bullets/player_bullet_blue.png',
                "gray1": 'Sprites/bullets/virus1_bullet_gray.png',}
    
    
    bullet_img = pg.image.load('Sprites/bullets/player_bullet_blue.png') 
    ENEMY_IMG = pg.image.load('Sprites/bullets/virus1_bullet_gray.png')
    
    SHIP_BULLET_VELOCITY = Main.SCREEN_HEIGHT // 55 #уменьшить число, чтобы повысить скорость
    ENEMY_BULLET_VELOCITY = Main.SCREEN_HEIGHT // 70
    
    SHIP_BULLET_SPRITES = pg.sprite.Group()
    ENEMY_BULLET_SPRITES = pg.sprite.Group()
    HIT_BOX = 0.8 # 1=спрайту, 0,5=половина спрайта
    
    def __init__(self, parent, x):
        pg.sprite.Sprite.__init__(self)
        
        self.parent = parent #определять класс чтобы узнать кто стреляет вирус или корабль
        self.parent_type = self.parent.__class__.__name__
        
        self.type_ = self.parent.get_type #нормальный путь. спрашивать тип стрелка напрямую. 
        self.image = Bullet._get_img(self.type_)
        
        if  self.parent_type == "Ship": #спрашивает у родителя какой его класс
            self.derection = -1    # -1=вверх = стреляет корабль по врагам, 1=вниз=враги по кораблю
            self.velocity = Bullet.SHIP_BULLET_VELOCITY
            
             #Bullet.bullet_img.convert_alpha()
            
            self.rect = self.image.get_rect(center=(x, self.parent.rect.top)) #пуля летит от верха, 
            self.add(Bullet.SHIP_BULLET_SPRITES)
        
        elif self.parent_type == "Enemy":
            self.derection = 1 
            self.velocity = Bullet.ENEMY_BULLET_VELOCITY
            #self.image = Bullet.ENEMY_IMG.convert_alpha()
            self.rect = self.image.get_rect(center=(x, self.parent.rect.y + self.parent.rect.width // 2 )) 
            self.add(Bullet.ENEMY_BULLET_SPRITES)
        
    
    
    @staticmethod
    def _get_img(type_):
        path = Enemy.IMG_BULLET_DICT.get(type_) or Ship.IMG_BULLET_DICT.get(type_) 
        bullet_img = pg.image.load(path).convert_alpha()
        return bullet_img
    
    @staticmethod
    def update (surfase):
        for bullet in (Bullet.SHIP_BULLET_SPRITES.sprites() + 
                       Bullet.ENEMY_BULLET_SPRITES.sprites()):
            bullet._move()
            bullet._check_collision()
        
        """
        for bullet in Bullet.SHIP_BULLET_SPRITES.sprites():
            bullet._move()
        for bullet in Bullet.ENEMY_BULLET_SPRITES.sprites():
            bullet._move()    
        """        
        Bullet.SHIP_BULLET_SPRITES.draw(surfase)
        Bullet.ENEMY_BULLET_SPRITES.draw(surfase)
            

        
        
    def _move(self):
        self.rect.y += self.velocity * self.derection
        if not 0 < self.rect.y < Main.SCREEN_HEIGHT :
            self.parent.set_ready_to_fire
            #print(self.parent.ready_to_fire)
            self.kill()
                
        
    def _check_collision(self):
        #коллизия пули с вирусом
        if self.parent_type == "Ship":
            collision_list = pg.sprite.spritecollide(self, Enemy.SPRITES, False,
                                                     collided = pg.sprite.collide_circle_ratio(Enemy.HIT_BOX)) 
            #возвращает список коллизий. 
            #collide_circle_ratio(0.5) уменьшает коллизию спрайта до круга, в 2 раза меньше исходного прямоугольникаквадрата 
            if collision_list:
                self.kill()
                self.parent.ready_to_fire = True
                self.parent.update_score(collision_list[0].enemy_type)
                collision_list[0].death()
        
        elif self.parent_type == "Enemy":
            #коллизия пули с пулей
            collision_list = pg.sprite.spritecollide(self, Bullet.SHIP_BULLET_SPRITES, False,
                                                    collided = pg.sprite.collide_circle_ratio(Bullet.HIT_BOX))
            if collision_list:
                self.parent.ready_to_fire = True
                self.kill()
                collision_list[0].parent.ready_to_fire = True
                collision_list[0].kill()
            
            #коллизия пули с бутылкой
            collision_list = pg.sprite.spritecollide(self, Ship.SPRITES, False,
                                                    collided = pg.sprite.collide_circle_ratio(Ship.HIT_BOX))
   
            if collision_list:
                self.kill()
                self.parent.ready_to_fire = True
                collision_list[0].death()
                #print(collision_list)
    """
    
    """


# In[5]:


class Ship(pg.sprite.Sprite):
    
    SHIP1_IMG = pg.image.load('Sprites/player1.png')#.convert_alpha()
    
    IMG_BULLET_DICT = {"player1":'Sprites/bullets/player_bullet_blue.png',}
    
    VELOCITY = Main.SCREEN_WIDTH // 200 #меньше значение - больше скорость
    
    SPRITES = pg.sprite.Group()
    HIT_BOX = 0.5
    NEW_GAME_LIVES = 3
    
    def __init__(self, type_ = "player1"):
        pg.sprite.Sprite.__init__(self)
        self.type_ = type_ # "player1" or "player2"
        self.image = Ship.SHIP1_IMG
        self.rect = self.image.get_rect(center=(Main.SCREEN_WIDTH // 2, Main.SCREEN_HEIGHT - 80))
        
        self.motion_vector = 0
        self.ready_to_fire = True
        self.score = 0
        self.lives = Ship.NEW_GAME_LIVES
        self.add(Ship.SPRITES)
        
    @staticmethod
    def update(surface):
        for ship in Ship.SPRITES:
            ship._move()
        Ship.SPRITES.draw(surface)
    
    
    @property
    def set_ready_to_fire(self):
        self.ready_to_fire = True

    
    @property
    def get_type(self):
        return self.type_
    
    def update_score(self, enemy_type):
        self.score += 50
        Text.update(Text.SHOW_DICT["SHIP1_SCORE"], "%06d" % self.score) #плохо, что тут конкретный корабль
        #Text.SHOW_DICT["SHIP1_SCORE"].text = str(self.score)  
    

    
    def _move(self):
        new_x = self.rect.x + Ship.VELOCITY * self.motion_vector
        if 0 < new_x < Main.SCREEN_WIDTH - self.rect[2]:
            self.rect.x = new_x
    
    def shot(self):
        if self.ready_to_fire:
            self.ready_to_fire = False
            self.bullet = Bullet(self, self.rect.center[0]) #говорит пуле, что её создал корабль
    
    def death(self):
        self.lives -= 1
        Text.update(Text.SHOW_DICT["LIVES1"], "%02d" % self.get_lives)
        if self.lives <= 0:
            Main.GAME_STATUS = "game_over" #Тест!
    
    @property
    def get_lives(self):
        return self.lives
    """        
    def draw(self, surfase):
        self._move()
        
        #if self.bullet != None:
        #    self.bullet.update(surfase)
        #pg.draw.rect(surfase, (125, 125, 125), self.rect)
        surfase.blit(self.image, self.rect)
    """    


# In[6]:


#Сделать, чтобы шрифты загружались в начале для каждого используемого размера в виде констант
class Text():
    
    text_surfase = pg.Surface((Main.SCREEN_WIDTH, Main.SCREEN_HEIGHT))
    text_surfase.fill(Main.FON_COLOR)   
    text_surfase.set_colorkey(Main.FON_COLOR) #делаю прозрачнуб поверхность под текст
   


    SHIP1_IMG = Main.scale(Ship.SHIP1_IMG , 0.50)
    
    TOP_LINE = 20
    BOTTOM_LINE = Main.SCREEN_HEIGHT - 25
    
    color_dict = {"red":(186, 76, 75), "blue":(107, 147, 127),"yellow":(195, 194, 125), "gray":(160, 220, 232),}
    
    SCORE1 = 0
    
    def __init__(self, key, text = "111", x=100, y=100, color="blue", font=Main.AmaticSC32, to_center_x=True, to_center_y=True,):
        self.text = str(text)
        #self.size = size
        self.font = font
        self.color = Text.color_dict[color]
        self.surf, tmp_rect = self.font.render(self.text, self.color)
        #центрирует поверхность
        self.rect = Main.get_center(self.surf, (x, y), to_center_x=to_center_x, to_center_y=to_center_y)   
        
        #self.rect.x = new_pos[0]
        #self.rect.y = new_pos[1]
        
        Text.SHOW_DICT[key] = self
        
        
        
    @staticmethod #кладет текстовую поверхность и инфокартинки на главную поверхность 
    def show(main_surfase):
        Text.text_surfase.fill(Main.FON_COLOR)
        if Main.GAME_STATUS == "game":
            main_surfase.blit(Text.SHIP1_IMG, 
                          Main.get_center(Text.SHIP1_IMG,(20,Text.BOTTOM_LINE-2))) #картинка корабля рядом с жизнями
        for text in Text.SHOW_DICT.values():
            Text.text_surfase.blit(text.surf,(text.rect.x, text.rect.y))
        main_surfase.blit(Text.text_surfase, (0,0))
    
    

        
    
    def update(self, text):
        self.text = str(text)
        self.surf, void = self.font.render(self.text, self.color)
        #Main.get_center(self.surf,(self.x, self.y), to_center_x=False)[2:4]
        self.surf
       

    

    @staticmethod
    def make_menu_text():
        Text.SHOW_DICT = {}
        NEW_GAME = Text("NEW_GAME", "NEW GAME"  , x=Main.SCREEN_WIDTH // 2 , y=Main.SCREEN_HEIGHT // 3, font=Main.AmaticSC70)
        QUIT = Text("QUIT", "QUIT"  , x=Main.SCREEN_WIDTH // 2 , y=Main.SCREEN_HEIGHT // 2, font=Main.AmaticSC70)

    
    @staticmethod
    def make_game_text():
        Text.SHOW_DICT = {}
        SCORE1 = Text("SCORE1", "SCORE <1> ", color="red", x=60 , y=Text.TOP_LINE)
        SHIP1_SCORE = Text("SHIP1_SCORE", "000000", color="red", x=SCORE1.rect.right, to_center_x=False, y=Text.TOP_LINE) 
        #чиcло очков прыгает при 8 и 9 в числе
        HI_SCORE = Text("HI_SCORE", "HI-SCORE ", x=Main.SCREEN_WIDTH // 2 - 40 , y=Text.TOP_LINE)
        HI_SCORE_SCORE = Text("HI_SCORE_SCORE", "000000", x=HI_SCORE.rect.right, to_center_x=False, y=Text.TOP_LINE) 
        SCORE2 = Text("SCORE2", "SCORE <2> ", color="yellow", x=Main.SCREEN_WIDTH - 120  , y=Text.TOP_LINE)
        SHIP2_SCORE = Text("SHIP2_SCORE", "000000", color="yellow", x=SCORE2.rect.right, to_center_x=False  , y=Text.TOP_LINE)
        #X1 = Text("X1", "x ", x=40, y=Text.BOTTOM_LINE)
        LIVES1 = Text("LIVES1", "%02d" % Ship.NEW_GAME_LIVES , x=45 , y=Text.BOTTOM_LINE)
        
    @staticmethod
    def make_game_over_text():
        Text.SHOW_DICT = {}
        
        GAME_OVER = Text("GAME_OVER", "GAME OVER"  , x=Main.SCREEN_WIDTH // 2 , y=Main.SCREEN_HEIGHT // 3, font=Main.AmaticSC70)
        YOU_SCORE = Text("YOU_SCORE", "YOU SCORE IS %d" % Main.ship1.score, x=Main.SCREEN_WIDTH // 2, y=GAME_OVER.rect.bottom + 50 )
    """     
        
      
    
        
    def _blit(self):
        Text.text_surfase.blit(self.surf, (self.rect.x, self.rect.y))
    
    def init_font():
        
        None if pg.font.get_init() else pg.font.init()
        AmaticSC32 = pg.font.Font("Fonts/AmaticSC-Bold.ttf", self.size)
    
    
    @staticmethod
    def make_menu():
        Text.MENU_DICT = {}   
        
        NEW_GAME = Text("NEW_GAME", "NEW GAME"  , x=Main.SCREEN_WIDTH // 2 , y=Main.SCREEN_HEIGHT // 3, font=Text.AmaticSC70)
        QUIT = Text("QUIT", "QUIT"  , x=Main.SCREEN_WIDTH // 2 , y=Main.SCREEN_HEIGHT // 2, font=Text.AmaticSC70)
        """


# In[7]:


class Enemy(pg.sprite.Sprite):
    """
    enemy_yellow_img = pg.image.load('Sprites/enemy_yellow.png')
    enemy_red_img = pg.image.load('Sprites/enemy_red.png')
    enemy_gray_img = pg.image.load('Sprites/enemy_gray.png')
    
   
    enemy_red_img = pg.transform.scale(enemy_red_img, (enemy_size, enemy_size))
    enemy_gray_img = pg.transform.scale(enemy_gray_img, (enemy_size, enemy_size))
    """
    pg.mixer.init()
    DEATH_SND = pg.mixer.Sound('Sound/death.wav')
    
    enemy_size = Main.SCREEN_WIDTH // 14  #масштабирование врагов. увеличить число для уменьшения размера
    
    #последняя цифра и расширенее файла указываются процедурно
    IMG_DICT = {"red": "Sprites/Enemy/virus2_red_",
                "gray":"Sprites/Enemy/virus1_gray_",
                "yellow":"Sprites/Enemy/virus2_yellow_",}
    
    IMG_BULLET_DICT = {"red":"Sprites/Bullets/virus2_bullet_red.png",
                       "gray":"Sprites/Bullets/virus1_bullet_gray.png",
                       "yellow":"Sprites/Bullets/virus2_bullet_yellow.png",}
    
    velocity =  Main.SCREEN_WIDTH // 400 #уменьшить значение, чтобы увеличить скорость
    ROWS = 5 #число строк
    COLUMNS = 11 #число столбцов
    
   
    x = 10 #начальные координаты роя
    y = 40
    fall_velocity = 10 

    HIT_BOX = 0.4 # уменьшает размер хитбокса и делает его круглым 
    dx = enemy_size * 0.9 #расстоянние между столбцами 
    dy = enemy_size * 0.7 
    
    TIME_TO_DEATH = 6
    
    
    derection = 1  #1 is rigth, -1 is left
    swarm_width = dx * COLUMNS
    swarm_heigth = dy * ROWS
    
    CHANSE_TO_FIRE = 2 # вероятность выстрела за тик (0=нет, 1000=100%)
    
    
    def __init__ (self, type_="gray"):
        pg.sprite.Sprite.__init__(self)
        self.enemy_type = type_ #gray, red, yellow
        
        self.image_sequence = Enemy._get_image_sequence(self.enemy_type) #секвенция с анимацией
        self.image_index = 0
        self.image = self.image_sequence[self.image_index]
              
        self.rect = self.image.get_rect(center=(0, 0))
        self.x = Enemy.velocity
        self.row = 0
        self.column = 0
        self.allow_to_fire = False
        self.ready_to_fire = True
        self.alive = True
        self.time_to_death = Enemy.TIME_TO_DEATH
        
        self.add(Enemy.SPRITES)
    
    
    
    
    def _make_rect(self):
        rect1 = self.image.get_rect(center=(0, 0)) #уменьшаем хитбокс center=(0, 0) get_size()
        rect2 = rect1.inflate(-25,-25)
        rect2.center = (100, 100)
        #rect = rect.move(-25,-25)
        return rect2
    
    @property
    def get_type(self):
        return self.enemy_type
    
    @property
    def set_ready_to_fire(self):
        self.ready_to_fire = True
    
    def _update_image(self):
        self.image_index += 1
        if self.image_index == len(self.image_sequence):
            self.image_index = 0

            
        self.image = self.image_sequence[self.image_index]
    
    
    
    
    
    @staticmethod
    def _get_image_sequence(enemy_type):
        image_sequence = []
        for frame_number in range(0,3):
            path = Enemy.IMG_DICT.get(enemy_type) + "%d.png" % frame_number
            enemy_img = pg.image.load(path).convert_alpha()
            enemy_img = pg.transform.scale(enemy_img, (Enemy.enemy_size, Enemy.enemy_size))
            image_sequence.append(enemy_img)
        
        path = "Sprites/Enemy/bah.png" #добавляет последний спрайт взрыва
        enemy_img = pg.image.load(path).convert_alpha()
        enemy_img = pg.transform.scale(enemy_img, (Enemy.enemy_size, Enemy.enemy_size))
        image_sequence.append(enemy_img)
        return image_sequence
    
    @staticmethod
    def set_swarm(): #устанавливает рой на начальные координаты
        Enemy.x = 0
        Enemy.y = Main.SCREEN_WIDTH // 26
        
    @staticmethod
    def move_swarm(surface):
        Enemy.x += Enemy.velocity * Enemy.derection
        #Enemy.y += Enemy.fall_velocity 
        if Enemy.SPRITES.sprites() == []: #если спрайты убиты, то некс левел
            Main.GAME_STATUS = "next_level" 
        for enemy in Enemy.SPRITES:
            Enemy._update(enemy)
        Enemy.SPRITES.draw(surface)
        
    def _update (self):
        #pg.time.set_timer(self._update_image(), 1000)
        self._death_timer() #анимация смерти
        self._fire() # стрельба
        self._move()
    
    def _death_timer (self):
        if self.alive == False: 
            self.time_to_death -= 1
            if self.time_to_death == 0:
                self.kill() #дохнет, если больше нет спрайтов  
            
                if self.allow_to_fire: #отдаем возможность стрелять тому, кто выше
                    for enemy in reversed(Enemy.SPRITES.sprites()):  
                        if enemy.column == self.column:
                            #print(enemy.allow_to_fire)
                            enemy.allow_to_fire = True
                            #print(enemy.allow_to_fire)
                            break
            
            if self.time_to_death % 2 == 0:
                self._update_image()
                
    
    

    def _move(self):
        # черные квадраты вместо аллов ту фаер
        #if self.allow_to_fire:
        #if self.ready_to_fire == False:
         #   self.image = pg.Surface((50,50))
        
        self.rect.x = Enemy.x + Enemy.dx * self.column #движение влево-вправо
        self.rect.y = Enemy.y + Enemy.dy * self.row
        previous_direction = Enemy.derection
        if self.rect.x < 0 :    # повороты от границ экрана
            Enemy.derection = 1
        elif self.rect.x + self.rect.width > Main.SCREEN_WIDTH:
            Enemy.derection = -1
        if  previous_direction != Enemy.derection:
            Enemy.y += Enemy.fall_velocity 
        #self._fire() # стрельба
    
    def _fire(self): 
        if (self.allow_to_fire * self.ready_to_fire): 
            if randint(0, 1000) < Enemy.CHANSE_TO_FIRE:
                self.ready_to_fire = False
                self.bullet = Bullet(self, self.rect.x + self.rect.width // 2)
                
  
    

    def death(self):
        count_of_enemies = len(Enemy.SPRITES) #ускоряем игру
        Main.ACCELERATION_FACTOR = Main.get_acceleration_factor(count_of_enemies)

        
        self.alive = False #запускаем анимацию смерти
        Enemy.DEATH_SND.play()

        
                
                    
        
    
    @staticmethod
    def make_list(): #делаем врагов процедурно. они попадают в список Enemy.SPRITES
        Enemy.SPRITES = pg.sprite.Group()
        name = "invaider"
        for r in range(Enemy.ROWS):
            for c in range(Enemy.COLUMNS):
                e = name + "_%s_%s" % (r, c)
                if r < 1:    # тип врагов в строке
                    type_ = "'gray'"
                elif 1 <= r < 3 :
                    type_ = "'red'"
                else:
                    type_ = "'yellow'"
                
                exec("%s = Enemy(%s)" % (e, type_))
                exec(("%s.row = " % e) + str(r))  # указываем каждому врагу его столбец и строку
                exec(("%s.column = " % e) + str(c))
                if r == (Enemy.ROWS - 1): #разрешает стрелять нижнему ряду
                    exec("%s.allow_to_fire = True" % e)


# In[8]:


Main.go()

"""
про эвенты:

https://www.rupython.com/pygame-42-37299.html
https://coderoad.ru/24475718/PyGame-%D0%9F%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%B5-%D0%A1%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B5
https://overcoder.net/q/3682782/%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-pygametimesettimer
https://www.pygame.org/docs/ref/event.html?
"""