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

        # Progress
        Tools.Current_Progress  = 0
        Tools.Progress          = ["Prologue_1", "Prologue_2", "Prologue_3", "Prologue_4"]
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
        self.Turn_Phase     = ""
        self.Turn_Order     = 0
        
        self.Active_Time    = 0
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
Combat = Combat()


class GameState():
    def __init__(self):
        # Progress
        self.Zone   = 0
        self.Stage  = 0
        self.Story  = 0
GameState = GameState()


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

        if self.background != None:
            gameDisplay.blit(self.background, (0,0))

        for event in Tools.events:
            Tools.event = event

        self.update_state()

    def update_state(self):
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
        Display interface menu
        """
        # Interface
        if self.result == True:
            gameDisplay.blit(Interface_Result, (0, 0))
            gameDisplay.blit(Icon_Ellesia_Status, (300,70))
            gameDisplay.blit(Icon_Iris_Status,  (300,220))
            gameDisplay.blit(Icon_Gyrei_Status, (300,370))

            # Enemy Icon
            for index in range(len(Fight.character[3:])):
                gameDisplay.blit(Fight.character[3+index].Icon, (660, 115+95*index))
                


        
        if self.inventory == True:
            gameDisplay.blit(Interface_Inventory, (0, 0))
            gameDisplay.blit(Icon_Ellesia_Status, (300,70))
            gameDisplay.blit(Icon_Iris_Status,  (300,220))
            gameDisplay.blit(Icon_Gyrei_Status, (300,370))
            
        


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
        self.textRect = self.textSurface.get_rect()

        # Center Text
        if center == True:
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
        self.images = self.load_images(self.path)                                               # Load all images in the directory
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

    def load_images(self, path):
        """
        Loads all images in directory. The directory must only contain images.

        Args:
            path: The relative or absolute path to the directory to load images from.

        Returns:
            List of images.
        """
        images = []
        for file_name in os.listdir(path):
            image = pygame.image.load(path + os.sep + file_name).convert()
            images.append(image)
        return images
        
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
        # Character / Slot / Death Status
        self.character = [PlayerIG, IrisIG, GyreiIG, Wolf("Wolf 1"), Wolf("Wolf 2"), Wolf("Wolf 3")]
        self.slot   = [True, True, True, True, True, True]
        self.death  = [False, False, False, False, False, False]

        # State
        self.turn = None
        self.button = False
        self.state_attack = False

        # Interface Position
        self.status_bar_y = 2*[590,640,690]
        
        self.character_x = [100,250,265,1055,905,890]
        self.character_y = [300,175,375,300,175,375]
        
        self.icon_x = 3*[10] + 3*[730]
        self.icon_y = 2*[570,620,670]
        
        self.name_x = 3*[135] + 3*[855]
        self.name_y = self.status_bar_y
        
        self.health_x = 3*[305] + 3*[1025]
        self.health_y = self.status_bar_y
        
        self.action_text_x = 3*[475] + 3*[1195]
        self.action_text_y = self.status_bar_y
        
        self.action_bar_x = 3*[401] + 3*[1121]
        self.action_bar_y = 2*[571,621,671]
        
        # Information
        self.time = 0
        self.time_x, self.time_y = 75, 25

        self.stage = 1
        self.stage_x, self.stage_y = 1205, 25

    def update_enemy(self, enemy=[], random_enemy=False):
        # Random Enemy
        if random_enemy == True:
            enemy = []
            for index in range(3-len(enemy)):
                random_enemy = random.randint(0, len(list_enemy)-1)
                enemy.append(list_enemy[random_enemy])

        # Add Enemies to the Character List
        for index in range(len(enemy)):
            self.character[index+3] = enemy[index]("Monster %s" % (index+1))
            self.slot[index+3] = True
            self.death[index+3] = False

    def attack_choice(self):
        if self.state_attack == False:
            self.state_attack = True        # Prevent bugs from multiple button clicks
            for index in range(3, 6):
                if self.slot[index] == True and self.death[index] == False:
                    sprite_rect = self.character[index].Sprite.get_rect(topleft=(self.character_x[index], self.character_y[index]))
                    Button(None, Text_Interface, sprite_rect[0]-10, sprite_rect[1]-10, sprite_rect[2]+20, sprite_rect[3]+20, 8, True, False, Color_Red, Color_Green, index, self.attack)

    def attack(self, target):
        hit = random.randint(0, 100)
        accuracy = (50+0.5*self.character[self.turn].Level) * (self.character[self.turn].Speed**2 / self.character[target].Speed**2)
        critical = (10+0.5*self.character[self.turn].Level) * self.character[self.turn].Speed * self.character[self.turn].Strength / (self.character[target].Defense * self.character[self.turn].Defense*5)

        if accuracy >= hit:
            if critical <= hit:
                self.character[target].Health -= self.character[self.turn].Strength
            else:
                self.character[target].Health -= self.character[self.turn].Strength*2       # Critical Damage

            if self.character[target].Health < 0:
                self.character[target].Health = 0

        self.end_turn()

    def end_turn(self):
        """
        Reset Character Action_Point, List_Button, Turn to None
        Check the dead characters
        Check win Condition
        """
        # Reset Character's Action Point & States
        self.character[self.turn].Action_Point = 0
        self.state_attack = False
        self.turn = None

        # Death Check
        for index in range(6):
            if self.slot[index] == True and self.character[index].Health <= 0:
                self.death[index] = True
                self.character[index].Action_Point = 0

        # Win Condition
        if all(self.slot[3:] and self.death[3:]):               ####################### WIP
            Tools.Current_Progress += 1
            eval(Tools.Progress[Tools.Current_Progress])()

    def update(self):
        """
        Update : User Interface
            Setup   : Refresh information each loop
            Text    : Information, Name, Health & Action_Point
            Image   : Character's Sprite & Icon
            Button  : Appears when it is the turn of a character
        """
        # Setup
        Setup.list_text = []
        
        # Information
        Text("Time: %s"  % self.time, self.time_x, self.time_y, True, Text_Interface)
        Text("Stage: %s" % self.stage, self.stage_x, self.stage_y, True, Text_Interface)

        # Characters Status
        for index in range(6):
            if self.slot[index] == True:
                # Characters - Image
                if self.death[index] == False:
                    gameDisplay.blit(self.character[index].Sprite, (self.character_x[index], self.character_y[index]))  # Sprite
                gameDisplay.blit(self.character[index].Icon, (self.icon_x[index], self.icon_y[index]))                  # Icon

                # Character - Information
                Text("%s" % self.character[index].name, self.name_x[index], self.name_y[index], True, Text_Interface)
                Text("HP: %i/%i" % (self.character[index].Health, self.character[index].Maxhealth), self.health_x[index], self.health_y[index], True, Text_Interface)

                # Character - Action Point
                Text("AP: %i/100" % self.character[index].Action_Point, self.action_text_x[index], self.action_text_y[index], True,Text_Interface)
                pygame.draw.rect(gameDisplay, Color_Green, (self.action_bar_x[index], self.action_bar_y[index], 1.48 * self.character[index].Action_Point, 38))
        """
        Update : Action Point
            Generate Action_Point up to 100
            When 100 is reached, give a turn to the character
            Reset List_Button after a Turn Reset
        """
        if self.turn == None:
            Setup.list_button = []
            
            for index in range(6):
                # Generating Action Point
                if self.slot[index] == True and self.death[index] == False:
                    self.character[index].Action_Point += self.character[index].Speed/10
                    
                # Gain a Turn to the character
                if self.character[index].Action_Point > 100:
                    self.character[index].Action_Point = 100
                    self.turn = index
                    self.button = True

        """
        Update : Turn Phase
            Player Phase    : Displays the player's actions
            Enemy Phase     : Randomly attacks a player
        """
        if self.turn != None:
            # Player Phase
            if self.turn < 3:
                # Highlight the Character's Turn
                sprite_rect = self.character[self.turn].Sprite.get_rect(topleft=(self.character_x[self.turn], self.character_y[self.turn]))
                pygame.draw.rect(gameDisplay, Color_Red, sprite_rect, 5)

                # Player Action Buttons
                if self.button == True:
                    self.button = False
                    Button("Attack", Text_Button, 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, self.attack_choice)
                    Button("Skill",  Text_Button, 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)
                    Button("Potion", Text_Button, 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)

            # Enemy Phase
            else:
                target = 0          # WIP target = random.randint(0, 2)
                self.attack(target)
            ############################################################
Fight = Fight()



class StoryIG():
    def __init__(self, read=True, input_box=False):
        # Text Input
        self.textinput  = pygame_textinput.TextInput()
        self.input_line = self.textinput.get_text()

        # State
        self.file       = open(List_Story[GameState.Story], "r")    # Read File
        self.read       = read                                      # Continue/Stop Reading
        self.input_box  = input_box                                 # Writing
        self.read_line  = ""                                        # Text File

        # Position text
        self.x          = 5
        self.y          = 565
        self.character_x = [100, 1180]
        self.character_y = [535, 535]
        
        # Position input_box
        self.input_x        = 540
        self.input_y        = 340
        self.input_width    = 200
        self.input_height   = 40
        self.input_border   = 5
        
        # Display
        self.index      = [0,0]
        self.character  = ["",""]
        self.text_line  = [["","","","","","",""],["","","","","","",""]]

    def update(self):
        if self.textinput.update(Tools.events):
            # Text
            self.input_line = self.textinput.get_text()
            self.textinput  = pygame_textinput.TextInput()

            # Input
            if self.input_box == True and self.input_line != "":
                self.input_box = False
                self.read = True

                # Player name
                PlayerIG.name = self.input_line
                self.character[0] = PlayerIG.name
                self.input_line = ""
                self.next_file(next_line=False)
                
            # Read
            if self.read == True:
                self.read_line  = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))    # Text in File

                # Next File
                if "(NEXT)" in self.read_line:
                    self.next_file()

                if "(SOUND)" in self.read_line:
                    self.play_sound(self.read_line.replace("(SOUND)", ""))
                    self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))

                if "(CUTSCENE END)" in self.read_line:
                    self.cutscene_end()

                # Event State
                if "(EVENT)" in self.read_line:
                    self.read = False

                # Input State
                if "(INPUT)" in self.read_line:
                    self.input_box  = True
                    self.input_line = ""
                    self.read_line  = self.read_line.replace("(INPUT)", "")

                # Result Screen
                if "(RESULT)" in self.read_line:
                    Result()

                # Left Side
                if "[L]" in self.read_line:
                    # Left Clear
                    if self.index[0] == 6:
                        self.clear_text("Left")
                        
                    # Left Character
                    if "(NAME)" in self.read_line:
                        self.character[0] = self.read_line.replace("(NAME)[L]", "")
                        self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))

                    # Left Text
                    self.text_line[0][self.index[0]]    = self.read_line.replace("[L]", "")
                    self.text_line[0][self.index[0]+1]  = "(-> Press Enter)"
                    self.text_line[1][self.index[1]]    = ""
                    self.index[0] += 1

                # Right Side
                if "[R]" in self.read_line:
                    # Right Clear
                    if self.index[1] == 6:
                        self.clear_text("Right")
                        
                    # Right Character
                    if "(NAME)" in self.read_line:
                        self.character[1] = self.read_line.replace("(NAME)[R]", "")
                        self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))

                    # Right Text
                    self.text_line[1][self.index[1]]    = self.read_line.replace("[R]", "")
                    self.text_line[1][self.index[1]+1]  = "(-> Press Enter)"
                    self.text_line[0][self.index[0]]    = ""
                    self.index[1] += 1
        self.display()

    def clear_text(self, side):
        if side == "Left":
            self.text_line[0] = ["","","","","","",""]
            self.index[0] = 0
            
        if side == "Right":
            self.text_line[1] = ["","","","","","",""]
            self.index[1] = 0

    def play_sound(self, sound):
        eval(sound).play()
            
    def cutscene_end(self):
        self.next_file(next_line=False)
        self.clear_text("Left")
        self.clear_text("Right")
        Tools.Current_Progress += 1
        eval(Tools.Progress[Tools.Current_Progress])()

    def next_file(self, next_line=True):
        self.file.close()
        GameState.Story += 1
        self.file = open(List_Story[GameState.Story], "r")

        if next_line == True:
            self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))    # Text in File

    def display(self):
        # Background
        gameDisplay.blit(Interface_Cutscene, (0,0))

        # Text
        for side in range(len(self.text_line)):
            self.load_text(self.character[side], self.character_x[side], self.character_y[side], True)
            
            for index in range(len(self.text_line[side])):
                self.load_text(self.text_line[side][index], self.x+720*side, self.y+20*index, False)

        # Input Box
        if self.input_box == True:
            pygame.draw.rect(gameDisplay, Color_Grey,   [self.input_x, self.input_y, self.input_width, self.input_height])
            pygame.draw.rect(gameDisplay, Color_Black,  [self.input_x, self.input_y, self.input_width, self.input_height], self.input_border)

            # Text Center
            rect    = self.textinput.get_surface()
            text_w  = rect.get_width()//2
            text_h  = rect.get_height()//2
            box_w   = self.input_x + self.input_width/2
            box_h   = self.input_y + self.input_height/2
            size = (box_w-text_w, box_h-text_h)
            gameDisplay.blit(self.textinput.get_surface(), size)

    def load_text(self, text, x, y, center):
        font = pygame.font.SysFont(None, 35)
        textSurf = font.render(text, True, Color_Black)

        if center == False:
            textRect = textSurf.get_rect(topleft=(x,y))
            
        if center == True:
            textRect = textSurf.get_rect(center=(x,y))

        gameDisplay.blit(textSurf, textRect)
StoryIG = StoryIG()



##### ###### ##### #####



def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup.update_init(Background_Title_Screen_1, OST_Title_Screen, text=True)
    
    # Button
    Button("Start",    Text_Button, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, eval(Tools.Progress[0]))
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
    Setup.update_init(Interface_Main_Menu, OST_Menu_Main_1_1, sprite=True, text=True)

    # Setup - Sprite
    AnimatedSprite(615,  385, True, "Data\Sprite_Button\Sprite_Button_Traning", clock.tick(FPS), 4, Debug_Fight)
    AnimatedSprite(1230, 470, True, "Data\Sprite_Button\Sprite_Button_Fight",   clock.tick(FPS), 4, None)

    # Setup - Button
    Button("Inventory", Text_Button, 120, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Inventory)
    Button("Status",    Text_Button, 284, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Status)
    Button("Save",      Text_Button, 448, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Game_Save)

    # Setup - Button
    Button("Music",     Text_Button, 1083, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Credits",   Text_Button, 1199, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, Credits)


    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()
    

def Result():
    if Setup.result == False:
        Setup.result    = True
        Setup.text      = True
        Setup.button    = True

        # Name
        Text(PlayerIG.name, 340, 180, True, Text_Interface)
        Text(IrisIG.name,   340, 330, True, Text_Interface)
        Text(GyreiIG.name,  340, 480, True, Text_Interface)

        # Class
        Text(PlayerIG.Class, 540, 90,  True, Text_Interface)
        Text(IrisIG.Class,   540, 240, True, Text_Interface)
        Text(GyreiIG.Class,  540, 390, True, Text_Interface)

        # Level
        Text("Level : %i" % PlayerIG.Level, 540, 135, True, Text_Interface)
        Text("Level : %i" % IrisIG.Level,   540, 285, True, Text_Interface)
        Text("Level : %i" % GyreiIG.Level,  540, 435, True, Text_Interface)

        # Results :
        Experience, Gold = 0, 0
        for index in range(len(Fight.character[3:])):
            Experience += Fight.character[3+index].EXP_Gain
            Gold += Fight.character[3+index].Gold_Gain
        Text("EXP : %i + %i" % (PlayerIG.Experience, Experience), 540, 180,  True, Text_Interface)
        Text("EXP : %i + %i" % (IrisIG.Experience, Experience),   540, 330, True, Text_Interface)
        Text("EXP : %i + %i" % (GyreiIG.Experience, Experience),  540, 480, True, Text_Interface)
        Text("Stage : %s" % Fight.stage, 760, 430, True, Text_Interface)
        Text("Gold : %i + %i" % (PlayerIG.Gold, Gold), 760, 480, True, Text_Interface)
        
        # Interface
        Text("Result",      760, 85,  True, Text_Interface)
        Text("Inventory",   960, 85,  True, Text_Interface)
        Button("Next", Text_Button, 960, 455, 135, 90, 4, False, True, Color_Green, Color_Red, None, Menu_Zone)

        # Enemy        
        for index in range(len(Fight.character[3:])):
            Text(Fight.character[3+index].name, 785, 135+95*index,  True, Text_Interface)
            Text("Level : %i" % Fight.character[3+index].Level, 785, 180+95*index,  True, Text_Interface)
            
def Inventory():
    if Setup.inventory == False:
        Setup.sprite = False
        Setup.inventory = True
        Text(PlayerIG.name, 340, 180, True, Text_Interface)
        Text(IrisIG.name,   340, 330, True, Text_Interface)
        Text(GyreiIG.name,  340, 480, True, Text_Interface)
        Text("Status",      540, 85, True, Text_Interface)
        Text("Equipment",   760, 85, True, Text_Interface)
        Text("Inventory",   950, 85, True, Text_Interface)
    
    else:
        Setup.sprite = True
        Setup.inventory = False
        Setup.list_text = []

def Status():
    print("Status!")

def Game_Save():
    print("Game Saved!")

def Credits():
    print("Credits!")



    
def Debug_Fight():
    # Setup
    Setup.update_init(Interface_Fight, List_OST[random.randint(7, 16)], fight=True)

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
    Setup.update_init(Background_Title_Screen_2, OST_Title_Screen)

    # Music Buttons
    Music_Selection = 0
    for row in range(round(len(List_OST)/6)) :
        for col in range(6):
            if Music_Selection < len(List_OST):
                Button("Music %i" % (Music_Selection+1), Text_Button, 60+(40+display_width/8)*col, 100+(40+display_height/10)*row, display_width/8, display_height/10, 12, True, False, Color_Green, Color_Red, Music_Selection, Music_Play)
                Music_Selection += 1

    # Exit Button
    Button_Image(1255, 25, True, Icon_Exit, Icon_Exit, None, Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()



def Prologue_1():
    # Setup
    Setup.update_init(Background_Prologue, OST_Cutscene_1_1, text=True, story=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()
                
def Prologue_2():
    # Setup
    Setup.update_init(Background_Cutscene_1, OST_Cutscene_1_2, text=True, story=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Prologue_3():
    # Setup
    Setup.update_init(Interface_Fight, OST_Fight_1_1, fight=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Prologue_4():
    # Setup
    Setup.update_init(Interface_Fight, OST_Menu_Victory_1, story=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

        

# Gallery Music
def Music_Play(Selection):
    pygame.mixer.music.load(List_OST[Selection])
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

Title_Screen()
