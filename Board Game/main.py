
import pygame as pg
import sys
from settings import *
from sprites import *
import random

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.player_turn = 0

        self.back_image = pg.Surface((TILESIZE, TILESIZE)) 
        self.back_image = pg.image.load(os.path.join(img_folder, "try.jpg")).convert_alpha()
        temp_scale1 = 8*TILESIZE/self.back_image.get_width()
        temp_scale2 = 7*TILESIZE/self.back_image.get_height()
        if temp_scale1 > temp_scale2:
            temp_scale = temp_scale1
        else:
            temp_scale = temp_scale2
        self.back_image = pg.transform.scale(self.back_image,(int(self.back_image.get_width()*temp_scale), int(self.back_image.get_height()*temp_scale)))
        self.back_image_rect = self.back_image.get_rect()
        self.back_image_rect.center = (8*TILESIZE, 5.5*TILESIZE) #self.screen.get_rect().center
        self.game_finished = 0

        

    def load_data(self):
        pass

    def new(self):
        '''
        # Fill background first surface
        self.background = pg.Surface((6*TILESIZE, 1*TILESIZE)).convert()
        self.background.fill((DARKGREEN))
        # Display some text for first surface
        font = pg.font.SysFont('None', 50)
        self.text = font.render("THE GOOD LIFE", 1, (10, 10, 10))
        self.textpos = self.text.get_rect()
        self.textpos.x = self.background.get_rect().x
        self.textpos.y = self.background.get_rect().y
        self.textpos.center = self.background.get_rect().center
        # Blit text to the surface
        self.background.blit(self.text, self.textpos)
        '''
        
        # initialize all variables and do all the setup for a  new game
        self.players = pg.sprite.LayeredUpdates()
        self.all_sprites = pg.sprite.Group()
        self.tiles = pg.sprite.LayeredUpdates()
       
        # We create the tiles on the board
        Tile(self, 12, 5) #0
        Donate(self, 12, 6) #1
        Interact1(self, 12, 7)
        Bank(self, 12, 8)
        Shop(self, 12, 9)
        Throw_Again(self, 11, 9) #5
        Save(self, 10, 9)
        Donate(self, 9, 9)
        Interact1(self, 8, 9)
        Bank(self, 7, 9)
        Shop(self, 6, 9) #10
        Throw_Again(self, 5, 9)
        Save(self, 4, 9)
        Shop(self, 3, 9)
        Donate(self, 3, 8)
        Interact1(self, 3, 7) #15
        Throw_Again(self, 3, 6)
        Bank(self, 3, 5)
        Save(self, 3, 4)
        Donate(self, 3, 3)
        Interact1(self, 3, 2) #20
        Shop(self, 3, 1)
        Throw_Again(self, 4, 1)
        Save(self, 5, 1)
        Interact1(self, 6, 1)
        Bank(self, 7, 1) #25
        Donate(self, 8, 1)
        Throw_Again(self, 9, 1)
        Interact1(self, 10, 1)
        Save(self, 11, 1)
        Shop(self, 12, 1) #30
        Bank(self, 12, 2)
        Interact1(self, 12, 3)
        Donate(self, 12, 4)

        #we create list of players
        self.player = []
        self.player.append(Player(self, 12, 5, 0))
        self.player.append(Player(self, 12, 5, 1))

        #initialize the dice
        self.dice = Dice(self, self.player, 6, 3)
        
        #set player turn false
        self.player_turn = 0
        
        #print(self.tiles.sprites())

        #we define the win text function
    def win_text(self):
        self.win_message = pg.Surface((12*TILESIZE, 3*TILESIZE)).convert()
        self.win_message.fill((DARKGREEN))
        font = pg.font.SysFont(None, 150)
        # Display some text with 2 posibilities
        if self.game_finished == 1:
            self.text = font.render("YOU WON!", 1, (10, 10, 10))
        elif  self.game_finished == 2:
            self.text = font.render("YOU LOST!", 1, (10, 10, 10))
        #blit text into surface
        textpos = self.text.get_rect() 
        textpos.center = self.win_message.get_rect().center
        self.win_message.blit(self.text, textpos)
        self.win_message_pos = self.win_message.get_rect()
        self.win_message_pos.center = self.screen.get_rect().center
        

            
    def run(self):
        # game loop
        # when we set self.playing = False --> the game ends
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.player[self.player_turn].donated >= 1000000 and self.player[self.player_turn].saved >= 0 and self.game_finished == 0:
                self.game_finished = self.player_turn + 1
                self.win_text()
            
            
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.player[self.player_turn].update()
        self.player[1-self.player_turn].update()
        self.all_sprites.update()


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, ( 0, y), (WIDTH, y))

    def draw(self):
        
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.back_image,self.back_image_rect)
        self.tiles.draw(self.screen)
        
        self.players.draw(self.screen)
        #self.screen.blit(self.background, (5*TILESIZE, 0*TILESIZE))
        self.load_show_status()
        self.screen.blit(self.player_data[0], (13.5*TILESIZE, 0*TILESIZE))
        self.screen.blit(self.player_data[1], (13.5*TILESIZE, 1.5*TILESIZE))
        self.screen.blit(self.player_data[2], (13.5*TILESIZE, 6.5*TILESIZE))
        self.show_tile_legend()
        if self.player[self.player_turn].show_options == 1:
            self.tiles.get_sprite(self.player[self.player_turn].tile_pos).show_options()
            mini_dice = self.dice.image
            mini_dice = pg.transform.scale(mini_dice,(2*TILESIZE, 2*TILESIZE))
            self.screen.blit(mini_dice, (7*TILESIZE, 6*TILESIZE))
        else:
            self.all_sprites.draw(self.screen)

        if self.game_finished > 0:
            self.screen.blit(self.win_message, self.win_message_pos)
        pg.display.flip()



    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_o:
                    self.player[0].donated = 1000000
                    self.player[0].saved = 0
                    #if game_finished is false --> you go to the player[player_turn] events
                if self.game_finished == 0:
                    if self.player[self.player_turn].show_options == 1:
                        self.tiles.get_sprite(self.player[self.player_turn].tile_pos).events(event)
                    else:
                        if event.key == pg.K_SPACE:
                            self.player[self.player_turn].move()
                

    def load_show_status(self):
        self.player_data = []
        self.player_data.append(pg.Surface((4*TILESIZE, 1*TILESIZE)).convert())
        if self.player_turn == 0:
            self.player_data[0].fill(LIGHTBLUE)
        else:
            self.player_data[0].fill(PINK)
        # Display some text --> players turn on the screen
        font = pg.font.Font(None, 40)
        self.text = font.render("Player %d" % (self.player_turn + 1), 1, (10, 10, 10))
        self.textpos = self.text.get_rect()
        self.textpos.center = self.player_data[0].get_rect().center
        self.player_data[0].blit(self.text, self.textpos)
        for index in range(1,3):
            self.player_data.append(pg.Surface((4*TILESIZE, 2.5*TILESIZE)).convert())
            if index == 1:
                self.player_data[index].fill((LIGHTBLUE))
            else:
                self.player_data[index].fill((PINK))
            
            # Display some text --> players amounts updates
            font = pg.font.Font(None, 40)
            self.text = font.render("Player %d:" % (index), 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.topleft = self.player_data[index].get_rect().topleft
            self.player_data[index].blit(self.text, self.textpos)
            
            font = pg.font.Font(None, 30)
            self.text = font.render("Wallet: %d" % self.player[index-1].wallet, 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.topleft = self.player_data[index].get_rect().topleft
            self.textpos.x += 30
            self.textpos.y += 30
            self.player_data[index].blit(self.text, self.textpos)

            font = pg.font.Font(None, 30)
            self.text = font.render("Invested: %d (%d%%)" % (self.player[index-1].invested,self.player[index-1].current_invested_percent*100), 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.topleft = self.player_data[index].get_rect().topleft
            self.textpos.x += 30
            self.textpos.y += 60
            self.player_data[index].blit(self.text, self.textpos)

            font = pg.font.Font(None, 30)
            self.text = font.render("Saved: %d (%d%%)" % (self.player[index-1].saved,self.player[index-1].current_saved_percent*100), 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.topleft = self.player_data[index].get_rect().topleft
            self.textpos.x += 30
            self.textpos.y += 90
            self.player_data[index].blit(self.text, self.textpos)
     
            font = pg.font.Font(None, 30)
            self.text = font.render("Donated: %d" % self.player[index-1].donated, 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.topleft = self.player_data[index].get_rect().topleft
            self.textpos.x += 30
            self.textpos.y += 120
            self.player_data[index].blit(self.text, self.textpos)
        
    def show_tile_legend(self):
        self.legend = []
        self.rect = []
        names = ['Bank','Donate','Spend','Save','Throw Again','Interact']
        colors = [GREEN,BLUE,RED,YELLOW,WHITE,PURPLE]
        for index in range(0,len(names)):
            self.legend.append(pg.Surface((2.5*TILESIZE, TILESIZE)))
            self.legend[index].fill(colors[index])
            self.rect.append(self.legend[index].get_rect())
            self.rect[index].x = (0) * TILESIZE
            self.rect[index].y = (index + 1) * TILESIZE

            font = pg.font.Font(None, 35)
            self.text = font.render(names[index], 1, (10, 10, 10))
            self.textpos = self.text.get_rect()
            self.textpos.center = self.legend[index].get_rect().center
            #self.textpos.x += 30
            #self.textpos.y += 60
            self.legend[index].blit(self.text, self.textpos)
            self.screen.blit(self.legend[index],(0,(index + 1) * TILESIZE))
        
    def show_status(self):
        pass
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
g.new()

g.run()
   
