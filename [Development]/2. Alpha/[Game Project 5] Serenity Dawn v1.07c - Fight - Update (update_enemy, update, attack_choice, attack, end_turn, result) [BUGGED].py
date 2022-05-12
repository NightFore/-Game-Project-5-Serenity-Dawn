import os
import pygame
import time
import pickle           # Load/Save Game
import random

import pygame_textinput
from Ressources         import *
from Balance            import *

pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Title
Project_Title = "Serenity Dawn"
pygame.display.set_caption(Project_Title)

# Screen Size
Screen_Size = display_width, display_height = 1280, 720
gameDisplay = pygame.display.set_mode((display_width, display_height))

class Tools():
    def __init__(self):
        self.event          = ""    # Button
        self.events         = ""    # Text
Tools = Tools()


class Combat():
    def __init__(self):
        # State
        self.Button_Action  = False
        self.Button_Turn    = False
        self.Button_Fight   = []
        self.End_Turn       = False
        
        self.Attack         = False
        self.Skill          = False
        
        self.Turn           = [False,False,False,False,False,False]
        self.Turn_Order     = 0
        
        self.Active_Time    = 0
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
Combat = Combat()


class GameState():
    def __init__(self):
        # Progress
        self.Zone   = 0
        self.Stage  = 0
GameState = GameState()


class Progress():
    def __init__(self):
        self.story = 0
        self.fight = 0
Progress = Progress()



# Miscellaneous
def file_len(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def load_file(path, image=False):
    """
    Load    : All texts/images in directory. The directory must only contain texts/images.
    Path    : The relative or absolute path to the directory to load texts/images from.
    Image   : Load and convert image in the direcoty path.
    Return  : List of files.
    """
    file = []
    for file_name in os.listdir(path):
        if image == False:
            file.append(path + os.sep + file_name)
        if image == True:
            file.append(pygame.image.load(path + os.sep + file_name).convert())
    return file

    
# Gallery Music
def Music_Play(Selection):
    pygame.mixer.music.load(Selection)
    pygame.mixer.music.play(-1)

# Text
def Text_Title_Screen():
    font = pygame.font.SysFont(None, 100)
    color = Color_Title_Screen
    return font, color

def Text_Button():
    font = pygame.font.SysFont(None, 40)
    color = Color_Blue
    return font, color

def Text_Interface():
    font = pygame.font.SysFont(None, 35)
    color = Color_Black
    return font, color


############################################################


class Setup():
    def __init__(self):
        # Background
        self.background = False

        # Music
        self.music = False

        # State
        self.button = False
        self.sprite = False
        self.fight  = False
        self.story  = False
        self.text   = False

        # Interface
        self.inventory  = False
        self.result     = False

        # State Update
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []

    def update_music(self, music):
        """
        Playing Music
        """
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    def update_init(self, background=False, music=False, button=False, sprite=False,  fight=False, text=False, story=False):
        """
        Background
        """
        self.background = background

        """
        Playing Music
        """
        self.music = music
        if self.music != False: 
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
        
        """
        Activate state functions
        """
        # State
        self.button = button
        self.sprite = sprite
        self.fight  = fight
        self.story  = story
        self.text   = text

        # Interface
        self.inventory  = False
        self.status     = None
        
        self.result     = False
        
        """
        Reset all lists when updating states
        """
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []

    def update(self):
        # Tools
        pygame.display.update()
        Tools.events = pygame.event.get()

        if self.background != False:
            gameDisplay.blit(self.background, (0,0))

        for event in Tools.events:
            Tools.event = event

        self.update_state()

    def update_state(self):
        if self.inventory == True:
            self.update_inventory()
        """
        Display interface menu
        """
        # Result
        if self.result == True:
            gameDisplay.blit(Interface_Result, (0, 0))
            
            for index in range(3):
                # Player
                if Fight.slot[index] == True:
                    gameDisplay.blit(Fight.character[index].Icon_Status, (300,70+150*index))

                if Fight.slot[3+index] == True:
                    gameDisplay.blit(Fight.character[3+index].Icon, (660, 115+95*index))
            
        


        """
        Display buttons from the list and check for mouse position.
        Call function action() if clicking on it
        """
        # Button
        if self.button == True:
            # Display Button
            for index in range(len(self.list_button)):
                self.list_button[index].update(index)
            for index in range(len(self.list_button_image)):
                self.list_button_image[index].update(index)

            # Check Mouse Position
            for event in Tools.events:
                for index in range(len(self.list_button)):
                    self.list_button[index].check(index)
                for index in range(len(self.list_button_image)):
                    self.list_button_image[index].check(index)

                

        """
        Display sprites from the list and check for mouse position.
        Call function action() if clicking on it.
        """
        # Sprite
        if self.sprite == True:
            # Display Sprite
            for index in range(len(self.list_sprite)):
                self.list_sprite[index].dt = clock.tick(FPS)
                self.all_sprites[index].update()
                self.all_sprites[index].draw(gameDisplay)

            # Check Mouse Position & Action
            for event in Tools.events:
                for index in range(len(self.list_sprite)):
                    if callable(self.list_sprite[index].action) == True:
                        self.list_sprite[index].button()

                    

        """
        Game_ui_Fight()         : Display background, list_text and list_button from 
        Fight_Action_Point()    : Generates action point for every character and allows them to take turn when reaching 100/100
        Turn_Phase()            : Check if the character taking an action is a player or enemy. If it is an enemy, it will automatically take an action
        Attack_Choice()         : Allows the player to select its target.
        """
        # Fight
        if self.fight == True:
            # Setup
            self.button = True
            self.text = True

            # Update
            Fight.update()



        """
        Display text from the list
        """
        # Text
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()


         
        """
        Display text being read from a file by the class StoryIG()
        Check for events and triggers to advance through the story
        """
        # Story
        if self.story == True:
            StoryIG.update()

            
    def inventory_init(self):
        if self.inventory == False:
            self.inventory = True
            self.sprite = False
            self.update_status(0)
            
            for index in range(3):
                if Fight.slot[index] == True:
                    Button(Fight.character[index].name, Text_Interface, 340, 180+150*index, 146, 38, 5, True, True, Color_Red, Color_Green, index, self.update_status)
                
        elif self.inventory == True:
            Menu_Zone()
            

    def update_inventory(self):
        gameDisplay.blit(Interface_Inventory, (0, 0))
        for index in range(3):
            if Fight.slot[index] == True:
                gameDisplay.blit(Fight.character[index].Icon_Status, (300,70+150*index))


    def update_status(self, status=None):
        if self.status!=status and status!=None:
            self.status = status
            self.list_text = []
            
            Text("Status",      540, 85, True, Text_Interface)
            Text("Equipment",   760, 85, True, Text_Interface)
            Text("Inventory",   960, 85, True, Text_Interface)
            
            Text(("Class : %s"      % Fight.character[status].Class),       450, 120, False, Text_Interface)
            Text(("Level : %i"      % Fight.character[status].level),       450, 150, False, Text_Interface)
            Text(("EXP : %i/100"    % Fight.character[status].Experience),  450, 180, False, Text_Interface)
            
            Text(("Health : %i"     % Fight.character[status].Maxhealth),   450, 220, False, Text_Interface)
            Text(("Strength : %i"   % Fight.character[status].Strength),    450, 250, False, Text_Interface)
            Text(("Magic : %i"      % Fight.character[status].Magic),       450, 280, False, Text_Interface)
            Text(("Speed : %i"      % Fight.character[status].speed),       450, 310, False, Text_Interface)
            Text(("Defense : %i"    % Fight.character[status].Defense),     450, 340, False, Text_Interface)
            Text(("Resistance : %i" % Fight.character[status].Resistance),  450, 370, False, Text_Interface)

############################################################ WIP
            Text(("Accuracy : %i"   % Fight.character[status].Resistance),  450, 410, False, Text_Interface)
            Text(("Evasion : %i"    % Fight.character[status].Resistance),  450, 440, False, Text_Interface)
            Text(("Critical : %i"   % Fight.character[status].Resistance),  450, 470, False, Text_Interface)
        
Setup = Setup()



class Text():
    def __init__(self, text, x, y, center, font):
        # Tools
        Setup.list_text.append(self)

        # Text
        self.text = text
        self.font = font
        self.font_type, self.color = self.font()

        # Position
        self.x = x
        self.y = y
        self.center = center

        # Surface
        self.textSurface = self.font_type.render(self.text, True, self.color)

        # Center Text
        if center == False:
            self.textRect = (self.x, self.y)
            
        if center == True:
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)
    
    # Display
    def display(self):
        gameDisplay.blit(self.textSurface, self.textRect)



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, center, path, dt, animation, action):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        # Tools
        Setup.list_sprite.append(self)
        Setup.all_sprites.append(pygame.sprite.Group(self))
        
        # Position
        self.x = x
        self.y = y
        self.center = center

        # Load Images
        self.path = path
        self.images = load_file(self.path, image=True)                                          # Load all images in the directory
        self.images_right = self.images                                                         # Normal image
        self.image_left = [pygame.transform.flip(image, True, False) for image in self.images]  # Flipping image.

        # Image
        self.index = 0                          # Current index
        self.image = self.images[self.index]    # Current image

        # Center Position
        if self.center == False:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.center == True:
            self.rect = self.image.get_rect(center=(self.x, self.y))

        # Update
        self.dt = dt
            #self.animation_time    = 0.1
        self.animation_time     = animation     # Time before sprite update
        self.current_time       = 0

            #self.animation_frames  = 6
        self.animation_frames   = animation     # Frame before sprite update
        self.current_frame      = 0

        # Action
        self.action = action
        
    def button(self):
        """
        Calls the function Selection when clicking oh the image
        """
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None:
                    self.action()

    def update_time_dependent(self):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        
        self.current_time += self.dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self):
        """
        This is the method that's being called when 'all_sprites.update(dt)' is called.
        """
        # Switch between the two update methods by commenting/uncommenting.
        # self.update_time_dependent()
        self.update_frame_dependent()



class Button():
    def __init__(self, text, font, x, y, w, h, b, border, center, active, inactive, selection, action=None):
        # Setup
        Setup.button = True
        
        # Tools
        Setup.list_button.append(self)

        # Text
        self.text = text
        self.font = font

        # Position
        self.x = x              # Position x
        self.y = y              # Position y
        self.w = w              # Width
        self.h = h              # Height
        self.b = b              # Border width
        self.border = border    # Border
        self.center = center    # Center

        # Color
        self.active     = active
        self.inactive   = inactive
        self.color      = inactive  # Color changes depending of the mouse position

        # Center button
        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)

        # Action
        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.color = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()
        else:
            self.color = self.inactive

    def update(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, self.rect, self.b)
        pygame.draw.rect(gameDisplay, self.color, self.rect)

        # Text
        font, color = self.font()
        textSurf = font.render(self.text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = self.x+self.w/2, self.y+self.h/2
        gameDisplay.blit(textSurf, textRect)



class Button_Image():
    def __init__(self, x, y, center, active, inactive, selection, action=None):
        # Tools
        Setup.list_button_image.append(self)

        # Position
        self.x = x              # Position x
        self.y = y              # Position y
        self.center = center    # Center

        # Image
        self.active     = active.convert()
        self.inactive   = inactive.convert()
        self.image      = inactive.convert()    # Image changes depending of the mouse position

        # Center Button
        if self.center == False:
            self.rect = self.active.get_rect(topleft=(x,y))

        if self.center == True:
            self.rect = self.active.get_rect(center=(x,y))

        # Action
        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.image = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()
        else:
            self.image = self.inactive

    def update(self, index):
        # Button
        gameDisplay.blit(self.image, self.rect)







class Fight():
    def __init__(self):
        # State
        self.training       = False
        self.turn           = None
        self.turn_phase     = None
        self.button         = False
        self.state_attack   = False
        
        # Character / Slot / Death Status
        self.character  = [[PlayerIG, IrisIG, GyreiIG], [None, None, None]]
        self.slot       = [[True, True, True],          [False, False, False]]
        self.death      = [[False, False, False],       [False, False, False]]

        # Information
        self.time = 0
        self.stage = 1

        # Interface Position
        self.character_x    = [[100, 250, 265], [1055, 905, 890]]
        self.character_y    = [[300, 175, 375], [300,  175, 375]]

        self.icon           = [10,  730]
        self.name           = [135, 855]
        self.health         = [305, 1025]
        self.action_text    = [475, 1195]
        self.action_bar     = [400, 1120]
        
        self.ui_image       = [570, 620, 670]
        self.ui_text        = [590, 640, 690]
        
        self.time_x         = 1205
        self.stage_x        = 75
        self.time_y         = 25
        self.stage_y        = 25

        
    def update(self):
        """
        Update : User Interface
            Setup           : Refresh information each loop
            User Interface  : Displays combat information (Time, Stage, Icon, Sprite, Name, Health, Action Point)
        """
        # Setup
        Setup.list_text = []

        # User Interface
        Text("Time: %s"  % self.time,   self.time_x,    self.time_y,    True, Text_Interface)
        Text("Stage: %s" % self.stage,  self.stage_x,   self.stage_y,   True, Text_Interface)

        for side in range(2):
            for index in range(3):
                if self.slot[side][index] == True:
                    character = self.character[side][index]

                    if self.death[side][index] == False:
                        gameDisplay.blit(character.Sprite, (self.character_x[side][index], self.character_y[side][index]))
                    gameDisplay.blit(character.Icon, (self.icon[side], self.ui_image[index]))

                    Text("%s"           % character.name,                           self.name[side],            self.ui_text[index],    True, Text_Interface)
                    Text("HP: %i/%i"    % (character.Health, character.Maxhealth),  self.health[side],          self.ui_text[index],    True, Text_Interface)
                    Text("AP: %i/100"   % character.Action_Point,                   self.action_text[side]+1,   self.ui_text[index]+1,  True, Text_Interface)
                    
                    pygame.draw.rect(gameDisplay, Color_Green, (self.action_bar[side]+1, self.ui_image[index]+1, 1.48 * character.Action_Point, 38))

                
        """
        Update : Action Point
            Generate action points until it reaches 100
            Give a turn to the character who reaches the threshold
            Resets the button list at the end of a turn
        """
        if self.turn == None:
            Setup.list_button = []
            for side in range(2):
                for index in range(3):
                    # Generating Action Point
                    if self.slot[side][index] == True and self.death[side][index] == False:
                        self.character[side][index].Action_Point += self.character[side][index].speed/10
                        
                        # Gain a Turn to the character
                        if self.character[side][index].Action_Point > 100:
                            self.character[side][index].Action_Point = 100
                            self.turn   = index
                            self.button = True


        """
        Update : Turn Phase
            Player Phase :
                Sprite_rect : Highlight the active character
                Button      : Displays available actions

            Enemy Phase :
                target          : Add to the list the index of the living characters
                random_target   : Randomly selects a character to attack
        """
        if self.turn != None:
            # Player Phase
            if self.turn < 3:
                sprite_rect = self.character[0][self.turn].Sprite.get_rect(topleft=(self.character_x[0][self.turn], self.character_y[0][self.turn]))
                pygame.draw.rect(gameDisplay, Color_Red, sprite_rect, 5)

                if self.button == True:
                    self.button = False
                    Button("Attack", Text_Button, 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, self.attack_choice)
                    Button("Skill",  Text_Button, 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)
                    Button("Guard",  Text_Button, 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)

            # Enemy Phase
            else:
                target = []
                for index in range(3):
                    if self.slot[0][index] == True:
                        target.append(index)
                random_target = random.choice(target)
                self.turn_phase = 1
                self.attack((random_target, 0))



    def update_enemy(self, enemy=[], random_enemy=False):
        """
        Story Enemy     :
            enemy : Enemies of the story read in a text file
        """
        if random_enemy == False:
            for index in range(len(enemy)):
                self.character[1][index] = enemy[index]
                self.slot[1][index]      = True
                self.death[1][index]     = False
                
        """
        Training Mode :
            enemy_count     : Random number of enemy
            avg_lvl         : Calculate average level of the player team
            enemy_random    : Random type of enemy
            enemy_name      : Name of the enemy
        """
        if random_enemy == True:
            enemy_count = random.randint(1, 3)
            
            avg_lvl = []
            for player in range(3):
                if self.slot[0][player] == True:
                    avg_lvl.append(self.character[0][player].level)
            avg_lvl = sum(avg_lvl)/len(avg_lvl)
            
            for index in range(enemy_count):
                enemy_random    = list_enemy[random.randint(0, len(list_enemy)-1)]
                enemy_name      = "Monster %s" % (index+1)

                self.character[1][index] = enemy_random(enemy_name, avg_lvl)
                self.slot[1][index]      = True
                self.death[1][index]     = False
                


    def attack_choice(self):
        """
        self.state_attack   : Attack Choice State (Prevent from clicking multiple times)
        self.slot/death     : Check Enemy Slot and Death State
        Button              : Draw a Selection Button surrounding each Enemy
        """
        if self.state_attack == False:
            self.turn_phase = 0
            self.state_attack = True
            for index in range(3):
                if self.slot[1][index] == True and self.death[1][index] == False:
                    sprite_rect = self.character[1][index].Sprite.get_rect(topleft=(self.character_x[1][index-3], self.character_y[1][index-3]))
                    Button(None, Text_Interface, sprite_rect[0]-10, sprite_rect[1]-10, sprite_rect[2]+20, sprite_rect[3]+20, 8, True, False, Color_Red, Color_Green, (index,1), self.attack)

    def attack(self, target):
        """
        Precision   : Value generated randomly corresponding to the hit & critical chance
            [Between 0 and 100]
            
        Accuracy    : Accuracy rate of the character to hit the target
            [2.5*Level + Speed^1.2/2 + 85]
            
        Evasion     : Subtract the accuracy of the character by the evasion rate of the target
            [2.5*Level + Speed/3]
            
        Critical    : Chance to make a critical hit that doubles the damage
            [35 - 25*(Health/Maxhealth)^(0.5 + 0.25*(P.Level-E.Level))]      35 - 25*(50/100)^0.5 = 20%
            
        Damage      : Damage value between 80% and 100% of the character strength
            (1) [Attack * (50 / (50 + Defense^1.25))]
            (2) [Attack * (10*Attack / (10*Attack + Defense^2*Attack/100))]
            (3) [10x^3 / (10x^2 + 100y^2)   (10*x**3) / (10*x**2 + 100*y**2)
            (4) [x^3 / (x^2 + 100y^2/x)
            (5) [x^3 / (x^2 + y^2 + y^3*100/(100+x^2))]
            (6) [x^3 / (x^2 + 1.5y^2 + y^3*100/(100+2x^2))]
        """
        print(target)
        side = target[1]
        target = target[0]
        
        attacker = self.character[self.turn_phase][self.turn]
        defender = self.character[side][target]
        precision   = random.randint(0, 100)
        accuracy    = 2.5*attacker.level + attacker.speed**1.2/2 + 85
        evasion     = 2.5*defender.level + defender.speed/3
        critical    = 35 - 25*(attacker.Health/attacker.Maxhealth)**(0.5 + 0.25*(attacker.level-defender.level))
        
        x = int(attacker.Strength)
        y = int(defender.Defense)
        attack      = x**3 / (x**2 + 2*y**2 + y**3*100/(100+1.5*x**2))
        damage      = random.randint(int(0.9*attack), int(1.1*attack))
        
        print("Attacker : %s" % attacker.name)
        print("Defender : %s" % defender.name)
        print("Precision = %i" % precision)
        print("Accuracy = %i" % accuracy)
        print("Evasion = %i" % evasion)
        print("Hit rate = %i" % (accuracy-evasion))
        print("Critical rate = %i" % critical)
        print("Damage = %i" % damage)
        print()

        print("Attack vs Defense = %i/%i" % (attacker.Strength, defender.Defense))
        print()
              
        # Success
        if (accuracy-evasion) >= precision:
            # Sound
            Random_SFX = random.randint(0, len(attacker.SFX_Attack)-1)
            pygame.mixer.Sound(attacker.SFX_Attack[Random_SFX]).play()
            
            # Normal Damage
            if critical < precision:
                defender.Health = int(defender.Health-damage)

            # Critical Damage
            else:
                defender.Health = int(defender.Health-damage*2)

            # Death
            if defender.Health < 0:
                defender.Health = 0
                defender.Action_Point = 0
                self.death[target] = True
                pygame.mixer.Sound(SFX_Battle_Defeated_battle02).play()

        # Miss
        else :
            pygame.mixer.Sound(SFX_Battle_Miss_battle14).play()

        self.end_turn()

    def end_turn(self):
        """
        Action Point    : Reset the Character Action Point to 0
        State_attack    : End Attack Choice State
        Turn            : Reset Turn to None
        Win             : Check for win condition
        """
        # Reset
        print(self.character[self.turn_phase][self.turn])
        print(self.character[self.turn_phase][self.turn].Action_Point)
        self.character[self.turn_phase][self.turn].Action_Point = 0
        self.state_attack = False
        self.turn = None

        # Win Condition
        Win = True
        for index in range(3):
            if self.slot[1][index] == True and self.death[1][index] == False:
                Win = False
                
        if Win == True:
            if self.training == False:
                Setup.update_init(story=True)
                StoryIG.next_file(story=True)
                Progress.fight += 1
                Progress.story += 1

            else:
                Setup.update_init(background=Interface_Fight, music=BGM_Victory_1)
                self.result()

        # Lose Condition
        Lose = True
        for index in range(3):
            if self.slot[0][index] == True and self.death[0][index] == False:
                Lose = False
                
        if Lose == True:
            Title_Screen()


    def result(self):
        if Setup.result == False:
            Setup.result    = True
            Setup.text      = True
            Setup.button    = True
                
            EXP  = 0
            Gold = 0
            for index in range(3):
                if self.slot[1][index] == True:
                    EXP  += self.character[1][index].EXP_Gain
                    Gold += self.character[1][index].Gold_Gain
            
            for index in range(3):
                # Player
                if self.slot[0][index] == True:
                    Text(self.character[0][index].name, 340, 180+150*index, True, Text_Interface)
                    Text(self.character[0][index].Class, 540, 90+150*index, True, Text_Interface)
                    Text("Level : %i" % self.character[0][index].level, 540, 135+150*index, True, Text_Interface)
                    Text("EXP : %i + %i" % (self.character[0][index].Experience, EXP), 540, 180+150*index, True, Text_Interface)

                # Enemy
                if self.slot[1][index] == True:
                    Text(self.character[1][index].name, 785, 135+95*index,  True, Text_Interface)
                    Text("Level : %i" % self.character[1][index].level, 785, 180+95*index,  True, Text_Interface)
                    
            Text("Stage : %s" % Fight.stage, 760, 430, True, Text_Interface)
            Text("Gold : %i + %i" % (PlayerIG.Gold, Gold), 760, 480, True, Text_Interface)
            Text("Result",      760, 85,  True, Text_Interface)
            Text("Inventory",   960, 85,  True, Text_Interface)
            Button("Next", Text_Button, 960, 455, 131, 86, 4, False, True, Color_Green, Color_Red, None, Menu_Zone)

            for index in range(3):
                if self.slot[0][index] == True:
                    self.character[0][index].Experience += EXP

                    while self.character[0][index].Experience >= 100:
                        self.character[0][index].update_level()
                        StoryIG.text_line[1][index] = self.character[index].name + " has Leveled Up!"
                    self.character[0][index].update_level()
            
            self.character[0][0].Gold += Gold
                
Fight = Fight()



class StoryIG():
    def __init__(self):
        # Text Input
        self.textinput  = pygame_textinput.TextInput()
        self.input_line = self.textinput.get_text()
        
        # State
        self.path           = ""                                            # Path of text files
        self.bootup         = ""                                            # Run self.update() once
        self.list_story     = load_file("Data\Story")                       # Load text files
        self.list_fight     = load_file("Data\Fight")                       # Load Enemy Informations
        self.file           = open(self.list_story[Progress.story], "r")    # Open the text file
        self.read_line      = ""                                            # Line of text read from the file
        self.state_read     = True                                          # Continue/Stop Reading
        self.state_input    = False                                         # Display input field

        # Position text
        self.x              = 5
        self.y              = 565
        self.character_x    = [100, 1180]
        self.character_y    = [535, 535]
        
        # Position input_box
        self.input_x        = 540
        self.input_y        = 340
        self.input_width    = 200
        self.input_height   = 40
        self.input_border   = 5
        
        # Display
        self.index          = [0,0]                         # Line index
        self.side           = ["[L]","[R]"]                 # Side of the text
        self.character      = ["",""]                       # Name of the speaking characters
        self.text_line      = [["","","","","","",""],      # Left side text
                               ["","","","","","",""]]      # Right side text

    def update_init(self):
        self.index          = [0,0]
        self.side           = ["[L]","[R]"]
        self.character      = ["",""]
        self.text_line      = [["","","","","","",""], ["","","","","","",""]]
        self.read_line      = ""
        self.state_read     = True
        self.state_input    = False
        self.file           = open(self.list_story[Progress.story], "r")
        

            
    def update(self):
        if self.textinput.update(Tools.events) or self.bootup!=self.file:
            """
            Bootup          : Start events once to load information like background, first line, etc...
            """
            if self.bootup != self.file:
                self.bootup = self.file

            
            """
            Input_Line      : Text entered by the keyboard
            Textinput       : Text Surface
            """
            # Input Text
            self.input_line = self.textinput.get_text()
            self.textinput  = pygame_textinput.TextInput()

            """
            State_Input     : Remove the Input Field
            State_Read      : Resume reading the Text File
            PlayerIG.name   : Name of the Player entered in the Input Field
            """
            # Player Name Input
            if self.state_input == True and self.input_line != "":
                self.next_file(story=True)
                self.bootup         = self.file
                self.state_input    = False
                self.state_read     = True
                PlayerIG.name       = self.input_line
                self.character[0]   = PlayerIG.name
                self.input_line     = ""

        
            """
            Read_Line       : Next Line in Text File
            Update_State    : Check for a change of State
            Clear_Text      : Clear Text if all lines are filled
            """
            # Read
            if self.state_read == True:
                self.read_line  = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))    # Text in File
                self.update_state()
                self.clear_text()
                
                for i in range(2):
                    if self.side[i] in self.read_line:
                        self.text_line[i][self.index[i]]                = self.read_line.replace(self.side[i], "")
                        self.text_line[i][self.index[i]+1]              = "(-> Press Enter)"
                        self.text_line[abs(i-1)][self.index[abs(i-1)]]  = ""
                        self.index[i] += 1
        self.update_display()


    def update_state(self):
        """
        Story Informations :
            Background  : Change the wallpaper by what is written in the text file
            Music       : Play the music written in the text file
            Sound       : Play the sound written in the text file
            Name        : Displays the name of the character in the corresponding side
            rstrip('\n'): Prevent reading bugs
        """
        if "(BACKGROUND)" in self.read_line:
            Setup.background = eval(self.read_line.replace("(BACKGROUND)", ""))
            self.read_line = self.file.readline().rstrip('\n')
            self.clear_text(left=True, right=True)
            self.character = ["",""]
            self.update_state()

        
        if "(MUSIC)" in self.read_line:
            Setup.update_music(eval(self.read_line.replace("(MUSIC)", "")))
            self.read_line = self.file.readline().rstrip('\n')
            self.clear_text(left=True, right=True)
            self.character = ["",""]
            self.update_state()

        
        if "(SOUND)" in self.read_line:
            eval(self.read_line.replace("(SOUND)", "")).play()
            self.read_line = self.file.readline().rstrip('\n')
            self.update_state()

    
        if "(NAME)" in self.read_line:
            for index in range(2):
                if self.side[index] in self.read_line:
                    self.character[index] = self.read_line.replace("(NAME)%s" % self.side[index], "").replace("%PlayerIG.name", ("%s" % PlayerIG.name))
            self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))
            self.update_state()


        """
        Story Events :
            Event   : Stop reading during an event
            Input   : Display an input field
            Next    : Open next text file
            Fight   : Start the fight with the enemies corresponding to the combat text file
            Result  : Shows victory screen
        """
        if "(INPUT)" in self.read_line:
            self.state_input    = True
            self.read_line      = self.read_line.rstrip('\n').replace("(INPUT)", "")
            self.input_line     = ""

        
        if "(EVENT)" in self.read_line:
            self.state_read = False
            self.read_line  = self.read_line.rstrip('\n').replace("(EVENT)", "")
            
        
        if "(NEXT)" in self.read_line:
            self.next_file(story=True)
            

        if "(FIGHT)" in self.read_line:
            # Informations : Load Background and Music
            self.next_file(fight=True)
            self.read_line = self.file.readline().rstrip('\n')
            self.update_state()

            enemy = []
            enemy_count = file_len(self.list_fight[Progress.fight])-3
            for index in range(enemy_count):
                enemy.append(eval(self.file.readline().rstrip('\n')))

            # User Interface
            Fight.update_enemy(enemy)
            Setup.update_init(Setup.background, Setup.music, fight=True)

        if "(RESULT)" in self.read_line:
            self.text_line[0][self.index[0]] = ""
            self.text_line[1][self.index[1]] = ""
            Fight.result()


    def update_display(self):
        """
        Background  : Cutscene's User Interface
        Text        : Character's Dialogue
        Input Box   : Display Input Field & Text Entered
        """
        # Background
        gameDisplay.blit(Interface_Cutscene, (0,0))

        # Input Box
        if self.state_input == True:
            pygame.draw.rect(gameDisplay, Color_Grey,   [self.input_x, self.input_y, self.input_width, self.input_height])
            pygame.draw.rect(gameDisplay, Color_Black,  [self.input_x, self.input_y, self.input_width, self.input_height], self.input_border)

            # Text Center
            rect    = self.textinput.get_surface()
            text_w  = rect.get_width()//2
            text_h  = rect.get_height()//2
            box_w   = self.input_x + self.input_width/2
            box_h   = self.input_y + self.input_height/2
            size    = (box_w-text_w, box_h-text_h)
            gameDisplay.blit(self.textinput.get_surface(), size)

        # Text
        for side in range(len(self.text_line)):
            self.load_text(self.character[side], self.character_x[side], self.character_y[side], True)
            for index in range(len(self.text_line[side])):
                self.load_text(self.text_line[side][index], self.x+720*side, self.y+20*index)
                

    def load_text(self, text, x, y, center=False):
        font     = pygame.font.SysFont(None, 35)
        textSurf = font.render(text, True, Color_Black)
        textRect = textSurf.get_rect(topleft=(x,y))
        
        if center == True:
            textRect = textSurf.get_rect(center=(x,y))

        gameDisplay.blit(textSurf, textRect)
    
    def clear_text(self, left=False, right=False):
        side = [left,right]
        for index in range(2):
            if side[index] == True or self.side[index] in self.read_line and self.index[index] == 6:
                self.text_line[index] = ["","","","","","",""]
                self.index[index] = 0

    def next_file(self, story=False, fight=False):
        self.file.close()

        if story == True:
            Progress.story += 1
            self.file = open(self.list_story[Progress.story], "r")
            
        elif fight == True:
            self.file = open(self.list_fight[Progress.fight], "r")
            self.clear_text(left=True, right=True)
                              
StoryIG = StoryIG()
    


##### ###### ##### #####



def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup.update_init(Background_Title_Screen_1, BGM_Title_Screen, text=True)
    
    # Button
    Button("Start",    Text_Button, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Main_Story)
    Button("Gallery",  Text_Button, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Main",     Text_Button, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Menu_Zone)

    # Text
    Text(Project_Title, display_width/2, display_height/4, True, Text_Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()


def Menu_Zone():
    # Setup
    Setup.update_init(Interface_Main_Menu, BGM_Menu_1, sprite=True, text=True)

    # Setup - Sprite
    AnimatedSprite(1230, 470, True, "Data\Sprite_Button\Sprite_Button_Fight",   clock.tick(FPS), 4, Main_Story)
    AnimatedSprite(615,  385, True, "Data\Sprite_Button\Sprite_Button_Traning", clock.tick(FPS), 4, Main_Training)

    # Setup - Button
    Button("Inventory", Text_Button, 120, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Setup.inventory_init)
    Button("Status",    Text_Button, 284, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Status)
    Button("Save",      Text_Button, 448, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Game_Save)
    Button("Music",     Text_Button, 1083, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Credits",   Text_Button, 1199, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, Credits)

    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Main_Story():
    # Setup
    Setup.update_init(story=True)
    StoryIG.update_init()
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()


def Main_Training():
    # Setup
    Setup.update_init(Interface_Fight, List_BGM[random.randint(8, 12)], fight=True)
    Fight.training = True

    # Enemy List
    Fight.update_enemy(random_enemy=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

    
def OST_Gallery():
    # Setup
    Setup.update_init(Background_Title_Screen_2, BGM_Title_Screen)

    # Music Buttons
    index = 0
    for row in range(round(0.5+len(List_BGM)/6)) :
        for col in range(6):
            if index < len(List_BGM):
                Button("Music %i" % (index+1), Text_Button, 60+200*col, 100+112*row, 160, 72, 12, True, False, Color_Green, Color_Red, List_BGM[index], Music_Play)
                index += 1

    # Exit Button
    Button_Image(1255, 25, True, Icon_Exit, Icon_Exit, None, Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Status():
    print("Status!")

def Game_Save():
    print("Game Saved!")

def Credits():
    print("Credits!")

Title_Screen()
