import pygame as pg
from settings import *
import os
import random
#import math

#set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.groups = game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        if num == 0:
            self.image = pg.image.load(os.path.join(img_folder, "splash-page-suuper.png")).convert_alpha()
        else:
            self.image = pg.image.load(os.path.join(img_folder, "splash-page-suuper2.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.center = self.game.tiles.get_sprite(0).rect.center
        self.rect.center = self.center # OR self.rect.center = (x*TILESIZE,y*TILESIZE) #* TILESIZE 
        self.tile_pos = 0
        self.dice_val = 1
        self.player_thrown = 0
        self.move_player = 0
        self.player_num = num
        #self.change_player = 0
        self.show_options = 0
        self.invested = 0
        self.donated = 0
        self.saved = 0
        self.invested_positive_rate = 0.02
        self.invested_negative_rate = 0
        self.saved_positive_rate = 0
        self.saved_negative_rate = -0.01
        self.selected = 0
        self.wallet = 100000

    
        
    def move(self):
        if self.player_thrown == 0 and self.move_player == 0:
            self.dice_val = random.randint(1,6)
            self.move_player = 0
            self.player_thrown = 1
            #self.change_player = 1
            self.game.dice.anim_flip = 0
            self.next_pos = (self.tile_pos + 1) % len(self.game.tiles.sprites())
            #if previous_pos > self.tile_pos:
                #self.wallet += 100000
            self.vx = (self.game.tiles.get_sprite(self.next_pos).rect.centerx - self.game.tiles.get_sprite(self.tile_pos).rect.centerx)/32
            self.vy = (self.game.tiles.get_sprite(self.next_pos).rect.centery - self.game.tiles.get_sprite(self.tile_pos).rect.centery)/32       
  

    def update(self):
        if self.invested_negative_rate == 0:
            self.current_invested_percent = self.invested_positive_rate
        else:
            self.current_invested_percent = self.invested_negative_rate
        if self.saved >= 0:
            self.current_saved_percent = self.saved_positive_rate
        else:
            self.current_saved_percent = self.saved_negative_rate
        
        if self.move_player == 1:# & self.change_player == 1:
            if self.dice_val > 0:
                if (self.game.tiles.get_sprite(self.next_pos).rect.centerx - self.rect.centerx != 0) or (self.game.tiles.get_sprite(self.next_pos).rect.centery - self.rect.centery != 0):
                    self.rect.centerx += self.vx
                    self.rect.centery += self.vy
                else:
                    self.tile_pos = (self.tile_pos + 1) % len(self.game.tiles.sprites())
                    self.next_pos = (self.tile_pos + 1) % len(self.game.tiles.sprites())
                    if self.tile_pos == 0:
                        self.wallet += 100000
                        self.invested_negative_rate = 0
                    self.vx = (self.game.tiles.get_sprite(self.next_pos).rect.centerx - self.game.tiles.get_sprite(self.tile_pos).rect.centerx)/32
                    self.vy = (self.game.tiles.get_sprite(self.next_pos).rect.centery - self.game.tiles.get_sprite(self.tile_pos).rect.centery)/32
                    #we used as a control variable...
                    #each time we move a tile accordinly to the dice val... we desc the dice_val 
                    self.dice_val -= 1
                    self.invested = self.invested*(1+self.current_invested_percent)
                    if self.saved < 0:
                        self.saved = self.saved*(1-self.saved_negative_rate)
                        
            else:
                self.move_player = 0
                self.show_options = 1
                self.selected = 0
            
        
class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
        self.finish = pg.Surface((4*TILESIZE, 1*TILESIZE)).convert()
        self.finish.fill((255, 255, 255))
        

        font = pg.font.Font(None, 30)
        self.finish_text1 = font.render("Press [Q] to end your turn", 1, (10, 10, 10))
        self.finish_textpos1 = self.finish_text1.get_rect()
        self.finish_textpos1.centery = self.finish.get_rect().centery
        self.finish.blit(self.finish_text1, self.finish_textpos1)
        
    def show_options(self):
        self.game.screen.blit(self.finish, (0*TILESIZE, 0*TILESIZE))

    def events(self, event):
        if event.key == pg.K_q:
            # ORDER IS IMPORTANT HERE!!
            self.game.player[self.game.player_turn].show_options = 0
            self.game.player_turn = 1-self.game.player_turn 

       # if event.key == pg.K_a:
           # self.game.player[self.game.player_turn].show_options = 1
            


            
class Bank(Tile):
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(GREEN)
        self.invest_x = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.invest_x.fill((GREEN))
        self.invest_y = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.invest_y.fill((GREEN))

        font = pg.font.Font(None, 50)
        self.invest_x_text1 = font.render("Invest: ", 1, (10, 10, 10))
        self.invest_x_textpos1 = self.invest_x_text1.get_rect()
        self.invest_x_textpos1.centerx = self.invest_x.get_rect().centerx
        self.invest_x.blit(self.invest_x_text1, self.invest_x_textpos1)

        font = pg.font.Font(None, 30)
        self.invest_x_text2 = font.render("Press [a] for 10k", 1, (10, 10, 10))
        self.invest_x_textpos2 = self.invest_x_text2.get_rect()
        self.invest_x_textpos2.center = self.invest_x.get_rect().center
        self.invest_x.blit(self.invest_x_text2, self.invest_x_textpos2)

        font = pg.font.Font(None, 50)
        self.invest_y_text1 = font.render("Withdraw: ", 1, (10, 10, 10))
        self.invest_y_textpos1 = self.invest_y_text1.get_rect()
        self.invest_y_textpos1.centerx = self.invest_y.get_rect().centerx
        self.invest_y.blit(self.invest_y_text1, self.invest_y_textpos1)

        font = pg.font.Font(None, 30)
        self.invest_y_text2 = font.render("Press [s] for 10k", 1, (10, 10, 10))
        self.invest_y_textpos2 = self.invest_y_text2.get_rect()
        self.invest_y_textpos2.center = self.invest_y.get_rect().center
        self.invest_y.blit(self.invest_y_text2, self.invest_y_textpos2)

    def show_options(self):
        super().show_options()
        self.game.screen.blit(self.invest_x, (4.5*TILESIZE, 3*TILESIZE))
        self.game.screen.blit(self.invest_y, (8.5*TILESIZE, 3*TILESIZE))
  
    def events(self, event):
        super().events(event)
        if event.key == pg.K_a:
            if self.game.player[self.game.player_turn].wallet >= 10000:
                self.game.player[self.game.player_turn].wallet -= 10000
                self.game.player[self.game.player_turn].invested += 10000
            
        
        if event.key == pg.K_s:
            if self.game.player[self.game.player_turn].invested >= 10000:
                self.game.player[self.game.player_turn].invested -= 10000
                self.game.player[self.game.player_turn].wallet += 10000
       
       
class Interact1(Tile):
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(PURPLE)
        self.interact_x = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.interact_x.fill((PURPLE))
        
       

        font = pg.font.Font(None, 50)
        self.interact_x_text1 = font.render("Get money: ", 1, (10, 10, 10))
        self.interact_x_textpos1 = self.interact_x_text1.get_rect()
        self.interact_x_textpos1.centerx = self.interact_x.get_rect().centerx
        self.interact_x.blit(self.interact_x_text1, self.interact_x_textpos1)

        font = pg.font.Font(None, 30)
        self.interact_x_text2 = font.render("Press [a] for 10k", 1, (10, 10, 10))
        self.interact_x_textpos2 = self.interact_x_text2.get_rect()
        self.interact_x_textpos2.center = self.interact_x.get_rect().center
        self.interact_x.blit(self.interact_x_text2, self.interact_x_textpos2)

        self.selected = 0
       


    def show_options(self):
        # super().show_options()
        self.game.screen.blit(self.interact_x, (4.5*TILESIZE, 3*TILESIZE))

        self.interact_y = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.interact_y.fill((PURPLE))
        font = pg.font.Font(None, 50)
        self.interact_y_text1 = font.render("Get money: ", 1, (10, 10, 10))
        self.interact_y_textpos1 = self.interact_y_text1.get_rect()
        self.interact_y_textpos1.centerx = self.interact_y.get_rect().centerx
        self.interact_y.blit(self.interact_y_text1, self.interact_y_textpos1)

        font = pg.font.Font(None, 30)
        self.interact_y_text2 = font.render("Press [s] for 10%", 1, (10, 10, 10))
        self.interact_y_textpos2 = self.interact_y_text2.get_rect()
        self.interact_y_textpos2.center = self.interact_y.get_rect().center
        self.interact_y.blit(self.interact_y_text2, self.interact_y_textpos2)
        font = pg.font.Font(None, 30)
        temp_val = self.game.player[1 - self.game.player_turn].wallet * 0.1
        self.interact_y_text2 = font.render("%(number)d" % {"number": temp_val}, 1, (10, 10, 10))
        self.interact_y_textpos2 = self.interact_y_text2.get_rect()
        self.interact_y_textpos2.midbottom = self.interact_y.get_rect().midbottom
        self.interact_y.blit(self.interact_y_text2, self.interact_y_textpos2)
        self.game.screen.blit(self.interact_y, (8.5*TILESIZE, 3*TILESIZE))

        if self.game.player[self.game.player_turn].selected == 1:
            super().show_options()
        

    def events(self, event):
        if self.game.player[self.game.player_turn].selected == 0:
            if event.key == pg.K_a:
                self.game.player[self.game.player_turn].wallet += 10000
                self.game.player[1 - self.game.player_turn].saved -= 10000
                self.game.player[self.game.player_turn].selected = 1
                
            if event.key == pg.K_s:
                temp_val = self.game.player[1 - self.game.player_turn].wallet * 0.1            
                self.game.player[self.game.player_turn].wallet += temp_val
                self.game.player[1 - self.game.player_turn].saved -= temp_val
                self.game.player[self.game.player_turn].selected = 1
            
        else:
            super().events(event)
        
       

class Shop(Tile):
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(RED)
        self.buy_x = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.buy_x.fill((RED))
        self.buy_y = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.buy_y.fill((RED))

        font = pg.font.Font(None, 30)
        self.buy_x_text1 = font.render("Increase rate: ", 1, (10, 10, 10))
        self.buy_x_textpos1 = self.buy_x_text1.get_rect()
        self.buy_x_textpos1.centerx = self.buy_x.get_rect().centerx
        self.buy_x.blit(self.buy_x_text1, self.buy_x_textpos1)

        font = pg.font.Font(None, 30)
        self.buy_x_text2 = font.render("Press [a] for 200k", 1, (10, 10, 10))
        self.buy_x_textpos2 = self.buy_x_text2.get_rect()
        self.buy_x_textpos2.center = self.buy_x.get_rect().center
        self.buy_x.blit(self.buy_x_text2, self.buy_x_textpos2)

        font = pg.font.Font(None, 30)
        self.buy_y_text1 = font.render("Decrease rate: ", 1, (10, 10, 10))
        self.buy_y_textpos1 = self.buy_y_text1.get_rect()
        self.buy_y_textpos1.centerx = self.buy_y.get_rect().centerx
        self.buy_y.blit(self.buy_y_text1, self.buy_y_textpos1)

        font = pg.font.Font(None, 30)
        self.buy_y_text2 = font.render("Press [s] for 250k", 1, (10, 10, 10))
        self.buy_y_textpos2 = self.buy_y_text2.get_rect()
        self.buy_y_textpos2.center = self.buy_y.get_rect().center
        self.buy_y.blit(self.buy_y_text2, self.buy_y_textpos2)

    def show_options(self):
        super().show_options()
        self.game.screen.blit(self.buy_x, (4.5*TILESIZE, 3*TILESIZE))
        self.game.screen.blit(self.buy_y, (8.5*TILESIZE, 3*TILESIZE))

    def events(self, event):
        super().events(event)
        if event.key == pg.K_a: # Increase your bank interest x2
            if self.game.player[self.game.player_turn].wallet >= 200000:
                self.game.player[self.game.player_turn].wallet -= 200000
                self.game.player[self.game.player_turn].invested_positive_rate *= 2
                self.game.player[self.game.player_turn].selected = 1
            else:
                pass # NOT ENOUGH MONEY IN WALLET! (sprite)
        if event.key == pg.K_s: # Make your opponents bank interest be -5% until passing the start again
            if self.game.player[self.game.player_turn].wallet >= 250000:
                self.game.player[self.game.player_turn].wallet -= 250000
                self.game.player[1-self.game.player_turn].invested_negative_rate = -0.05
                self.game.player[self.game.player_turn].selected = 1
            else:
                pass # NOT ENOUGH MONEY IN WALLET! (sprite)
            
        

 
class Donate(Tile):
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(BLUE)
        self.option1 = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.option1.fill((BLUE))

        font = pg.font.Font(None, 50)
        self.option1_text1 = font.render("Donate: ", 1, (10, 10, 10))
        self.option1_textpos1 = self.option1_text1.get_rect()
        self.option1_textpos1.centerx = self.option1.get_rect().centerx
        self.option1.blit(self.option1_text1, self.option1_textpos1)

        font = pg.font.Font(None, 30)
        self.option1_text2 = font.render("Press [a] to donate", 1, (10, 10, 10))
        self.option1_textpos2 = self.option1_text2.get_rect()
        self.option1_textpos2.center = self.option1.get_rect().center
        self.option1.blit(self.option1_text2, self.option1_textpos2)

    def show_options(self):
        super().show_options()
        self.game.screen.blit(self.option1, (4.5*TILESIZE, 3*TILESIZE))

    def events(self, event):
        super().events(event)
        if event.key == pg.K_a:
            if self.game.player[self.game.player_turn].wallet >= 10000:
                self.game.player[self.game.player_turn].wallet -= 10000
                self.game.player[self.game.player_turn].donated += 10000
        


class Throw_Again(Tile):
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(WHITE)
        self.repeat = pg.Surface((6*TILESIZE, 2*TILESIZE)).convert()
        self.repeat.fill((150, 150, 150))
        

        font = pg.font.Font(None, 50)
        self.repeat_text1 = font.render("Congrats! Throw again!", 1, (10, 10, 10))
        self.repeat_textpos1 = self.repeat_text1.get_rect()
        self.repeat_textpos1.centerx = self.repeat.get_rect().centerx
        self.repeat.blit(self.repeat_text1, self.repeat_textpos1)
      
    def show_options(self):
        # super().show_options()
        self.game.screen.blit(self.repeat, (5*TILESIZE, 3*TILESIZE))

    def events(self, event):
        # super().events(event)
        if event.key == pg.K_SPACE:
            self.game.player[self.game.player_turn].show_options = 0
            self.game.player[self.game.player_turn].move()
            #throw one more time

        
class Save(Tile):
    # using bank template
    def __init__(self,game,x,y):
        super().__init__(game,x,y)
        self.image.fill(YELLOW)
        self.invest_x = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.invest_x.fill((YELLOW))
        self.invest_y = pg.Surface((3*TILESIZE, 2*TILESIZE)).convert()
        self.invest_y.fill((YELLOW))

        font = pg.font.Font(None, 50)
        self.invest_x_text1 = font.render("Save: ", 1, (10, 10, 10))
        self.invest_x_textpos1 = self.invest_x_text1.get_rect()
        self.invest_x_textpos1.centerx = self.invest_x.get_rect().centerx
        self.invest_x.blit(self.invest_x_text1, self.invest_x_textpos1)

        font = pg.font.Font(None, 30)
        self.invest_x_text2 = font.render("Press [a] for 10k", 1, (10, 10, 10))
        self.invest_x_textpos2 = self.invest_x_text2.get_rect()
        self.invest_x_textpos2.center = self.invest_x.get_rect().center
        self.invest_x.blit(self.invest_x_text2, self.invest_x_textpos2)

        font = pg.font.Font(None, 50)
        self.invest_y_text1 = font.render("Withdraw: ", 1, (10, 10, 10))
        self.invest_y_textpos1 = self.invest_y_text1.get_rect()
        self.invest_y_textpos1.centerx = self.invest_y.get_rect().centerx
        self.invest_y.blit(self.invest_y_text1, self.invest_y_textpos1)

        font = pg.font.Font(None, 30)
        self.invest_y_text2 = font.render("Press [s] for 10k", 1, (10, 10, 10))
        self.invest_y_textpos2 = self.invest_y_text2.get_rect()
        self.invest_y_textpos2.center = self.invest_y.get_rect().center
        self.invest_y.blit(self.invest_y_text2, self.invest_y_textpos2)

    def show_options(self):
        super().show_options()
        self.game.screen.blit(self.invest_x, (4.5*TILESIZE, 3*TILESIZE))
        self.game.screen.blit(self.invest_y, (8.5*TILESIZE, 3*TILESIZE))
  
    def events(self, event):
        super().events(event)
        if event.key == pg.K_a:
            if self.game.player[self.game.player_turn].wallet >= 10000:
                self.game.player[self.game.player_turn].wallet -= 10000
                self.game.player[self.game.player_turn].saved += 10000
            
        if event.key == pg.K_s:
            if self.game.player[self.game.player_turn].saved >= 10000:
                self.game.player[self.game.player_turn].saved -= 10000
                self.game.player[self.game.player_turn].wallet += 10000





        
class Dice(pg.sprite.Sprite):
    def __init__(self, game, player, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.groups = game.all_sprites
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load(os.path.join(img_folder, "31.png")).convert_alpha()
       
        
        self.anim_list1 = pg.image.load(os.path.join(img_folder, "01.png")).convert_alpha()
        self.anim_list2 = pg.image.load(os.path.join(img_folder, "02.png")).convert_alpha()
        self.anim_list3 = pg.image.load(os.path.join(img_folder, "03.png")).convert_alpha()
        self.anim_list4 = pg.image.load(os.path.join(img_folder, "04.png")).convert_alpha()
        self.anim_list5 = pg.image.load(os.path.join(img_folder, "05.png")).convert_alpha()
        self.anim_list6 = pg.image.load(os.path.join(img_folder, "06.png")).convert_alpha()
        self.anim_list7 = pg.image.load(os.path.join(img_folder, "07.png")).convert_alpha()
        self.anim_list8 = pg.image.load(os.path.join(img_folder, "08.png")).convert_alpha()
        self.anim_list9 = pg.image.load(os.path.join(img_folder, "09.png")).convert_alpha()
        self.anim_list10 = pg.image.load(os.path.join(img_folder, "10.png")).convert_alpha()
        self.anim_list11 = pg.image.load(os.path.join(img_folder, "11.png")).convert_alpha()
        self.anim_list12 = pg.image.load(os.path.join(img_folder, "12.png")).convert_alpha()
        self.anim_list13 = pg.image.load(os.path.join(img_folder, "13.png")).convert_alpha()
        self.anim_list14 = pg.image.load(os.path.join(img_folder, "14.png")).convert_alpha()
        self.anim_list15 = pg.image.load(os.path.join(img_folder, "15.png")).convert_alpha()
        self.anim_list16 = pg.image.load(os.path.join(img_folder, "16.png")).convert_alpha()
        self.anim_list17 = pg.image.load(os.path.join(img_folder, "17.png")).convert_alpha()
        self.anim_list18 = pg.image.load(os.path.join(img_folder, "18.png")).convert_alpha()
        self.anim_list19 = pg.image.load(os.path.join(img_folder, "19.png")).convert_alpha()
        self.anim_list20 = pg.image.load(os.path.join(img_folder, "20.png")).convert_alpha()
        self.anim_list21 = pg.image.load(os.path.join(img_folder, "21.png")).convert_alpha()
        self.anim_list22 = pg.image.load(os.path.join(img_folder, "22.png")).convert_alpha()
        self.anim_list23 = pg.image.load(os.path.join(img_folder, "23.png")).convert_alpha()
        self.anim_list24 = pg.image.load(os.path.join(img_folder, "24.png")).convert_alpha()
        self.anim_list25 = pg.image.load(os.path.join(img_folder, "25.png")).convert_alpha()
        self.anim_list26 = pg.image.load(os.path.join(img_folder, "26.png")).convert_alpha()
        self.anim_list27 = pg.image.load(os.path.join(img_folder, "27.png")).convert_alpha()
        self.anim_list28 = pg.image.load(os.path.join(img_folder, "28.png")).convert_alpha()
        self.anim_list29 = pg.image.load(os.path.join(img_folder, "29.png")).convert_alpha()
        self.anim_list30 = pg.image.load(os.path.join(img_folder, "30.png")).convert_alpha()
        self.anim_list31 = pg.image.load(os.path.join(img_folder, "31.png")).convert_alpha()
        self.anim_list32 = pg.image.load(os.path.join(img_folder, "32.png")).convert_alpha()
        self.animation = [self.anim_list1,self.anim_list2,self.anim_list3,self.anim_list4,self.anim_list5,self.anim_list6,self.anim_list7,self.anim_list8,
                          self.anim_list9,self.anim_list10,self.anim_list11,self.anim_list12,self.anim_list13,self.anim_list14,self.anim_list15,self.anim_list16,
                          self.anim_list17,self.anim_list18,self.anim_list19,self.anim_list20,self.anim_list21,self.anim_list22,self.anim_list23,self.anim_list24,
                          self.anim_list25,self.anim_list26,self.anim_list27,self.anim_list28,self.anim_list29,self.anim_list30,self.anim_list31,self.anim_list32]
        
        #self.value = 1
        self.anim_flip = len(self.animation) + 1
        
        self.dice1= pg.image.load(os.path.join(img_folder,'diceOne.png')).convert_alpha()
        self.dice2= pg.image.load(os.path.join(img_folder,'diceTwo.png')).convert_alpha()
        self.dice3= pg.image.load(os.path.join(img_folder,'diceThree.png')).convert_alpha()
        self.dice4= pg.image.load(os.path.join(img_folder,'diceFour.png')).convert_alpha()
        self.dice5= pg.image.load(os.path.join(img_folder,'diceFive.png')).convert_alpha()
        self.dice6= pg.image.load(os.path.join(img_folder,'diceSix.png')).convert_alpha()
        self.dice7= pg.image.load(os.path.join(img_folder,'07.png')).convert_alpha()
        self.dice_list = [self.dice1,self.dice2,self.dice3,self.dice4,self.dice5,self.dice6,self.dice7]
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
    def update(self):
        if self.player[self.game.player_turn].player_thrown == 1:
            if self.anim_flip < len(self.animation):
                self.image = self.animation[self.anim_flip]
                self.image = pg.transform.scale(self.image,(4*TILESIZE, 4*TILESIZE))
                self.anim_flip += 1
            else:
                self.image = self.dice_list[self.player[self.game.player_turn].dice_val-1]
                self.image = pg.transform.scale(self.image,(4*TILESIZE, 4*TILESIZE))
                self.player[self.game.player_turn].move_player = 1
                self.player[self.game.player_turn].player_thrown = 0
                

    
'''
STUFF TO DO:

- Computer [player]


'''












        
