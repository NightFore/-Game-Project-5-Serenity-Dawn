import os
import pygame
import time
import pickle           # Load/Save Game
import random
import re               # re.split()

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
        self.Turn_Count     = 1
        
        self.Active_Time    = 0
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
Combat = Combat()


class GameState():
    def __init__(self):
        # Progress
        self.Zone   = 0
        self.Stage  = 0
        self.Story  = 0
        
        # Interface Fight
        self.Character          = [PlayerIG]
        self.Character_Slot     = []
        self.Character_Death    = []
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
        Activate state sunctions
        """
        self.button = button
        self.sprite = sprite
        self.fight  = fight
        self.story  = story
        self.text   = text
        
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
        if self.fight == True:
            self.button = True
            self.text   = True
            # Reset Text
            self.list_text = []
            
            # Interface
            Game_ui_Fight()

            # State - Action Point
            Fight_Action_Point()

            # State - Turn Phase
            if Combat.Turn_Phase != "":
                Turn_Phase()
                
            # State - Attack Selection
            if Combat.Attack == True:
                Attack_Choice()

            if Combat.End_Turn == True:
                self.list_button = []
                Combat.Button_Action = False
                Combat.Button_Turn = False
                Combat.End_Turn = False

        """
        Display text from the list
        """
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()
        """
        Display text being read from a file by the class StoryIG()
        Check for events and triggers to advance through the story
        """
        if self.story == True:
            StoryIG.update()
Setup = Setup()



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
                self.read_line  = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))    # Text in File

                # Next File
                if "(NEXT)" in self.read_line:
                    self.next_file()

                if "(SOUND)" in self.read_line:
                    self.play_sound(self.read_line.replace("(SOUND)", ""))
                    self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

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

                # Left Side
                if "[L]" in self.read_line:
                    # Left Clear
                    if self.index[0] == 6:
                        self.clear_text("Left")
                        
                    # Left Character
                    if "(NAME)" in self.read_line:
                        self.character[0] = self.read_line.replace("(NAME)[L]", "")
                        self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

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
                        self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

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



class Text():
    def __init__(self, text, font, x, y, center):
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







def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup.update_init(Background_Title_Screen_1, OST_Title_Screen, button=True, text=True)
    
    # Button
    Button("Start",    Text_Button, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, eval(Tools.Progress[0]))
    Button("Gallery",  Text_Button, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Main",     Text_Button, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Menu_Zone_1)

    # Text
    Text(Project_Title, Text_Title_Screen, display_width/2, display_height/4, True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Menu_Zone_1():
    # Setup
    Setup.update_init(Background_Main_1, OST_Menu_Main_1_1, sprite=True, text=True)

    # Sprite Setup
    AnimatedSprite(615,  435, True, "Data\Sprite_Button\Sprite_Button_Traning", clock.tick(FPS), 4, Training)
    AnimatedSprite(1230, 520, True, "Data\Sprite_Button\Sprite_Button_Fight",   clock.tick(FPS), 4, Prologue_3)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def OST_Gallery():
    # Setup
    Setup.update_init(Background_Title_Screen_2, OST_Title_Screen, button=True)

    # Button Setup
        # Music
    Music_Selection = 0
    for row in range(round(len(List_OST)/6)) :
        for col in range(6):
            if Music_Selection < len(List_OST):
                Button("Music %i" % (Music_Selection+1), Text_Button, 60+(40+display_width/8)*col, 100+(40+display_height/10)*row, display_width/8, display_height/10, 12, True, False, Color_Green, Color_Red, Music_Selection, Music_Play)
                Music_Selection += 1

        # Exit
    Button_Image(1255, 25, True, Icon_Exit, Icon_Exit, None, Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Training():
    # Setup
    Setup.update_init(Interface_Fight, List_OST[random.randint(7, 16)], text=True, button=True, fight=True)

    # Player / Enemy
    GameState.Character         = [PlayerIG, IrisIG, GyreiIG]
    GameState.Character_Slot    = [True,     True,   True,      True,   True,       True]
    GameState.Character_Death   = [False,    False,  False,     False,  False,      False]

    # Random Enemy
    for i in range(3):
        Enemy = List_Enemy[random.randint(0, len(List_Enemy)-1)]
        GameState.Character.append(Enemy("Monster %i" % (i+1)))
    
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
    Setup.update_init(Interface_Fight, OST_Fight_1_1, text=True, button=True, fight=True)

    # Player / Enemy
    GameState.Character         = [PlayerIG, "",    "",     WolfIG, "",     ""]
    GameState.Character_Slot    = [True,     False, False,  True,   False,  False]
    GameState.Character_Death   = [False,    True,  True,   False,  True,   True]
    
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



def Game_ui_Fight():
    # Information
    Text("Turn: %s"  % Combat.Turn_Count, Text_Interface, Turn_Count_X, Turn_Count_Y, True)
    Text("Stage: %s" % GameState.Stage,   Text_Interface, Stage_X,      Stage_Y,      True)
    
    # Commands
    if Combat.Turn_Phase != "" and Combat.Turn_Phase <= 2:
        if Combat.Button_Action == False:
            Combat.Button_Action = True
            Button("Attack", Text_Button, 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, Attack_Choice)
            Button("Skill",  Text_Button, 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)
            Button("Potion", Text_Button, 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)

    # Player / Enemy
    for i in range(6):
        if GameState.Character_Slot[i] == True:
            # Sprite
            if GameState.Character_Death[i] == False:
                gameDisplay.blit(GameState.Character[i].Sprite, (Sprite_Character_X[i], Sprite_Character_Y[i]))

            # Icon
            gameDisplay.blit(GameState.Character[i].Icon, (Status_Icon_X[i], Status_Bar_Image_Y[i]))

            # Text
            Text("%s"        % GameState.Character[i].name,                                       Text_Interface, Status_Name_X[i],   Status_Bar_Text_Y[i], True)
            Text("HP: %i/%i" % (GameState.Character[i].Health, GameState.Character[i].Maxhealth), Text_Interface, Status_Health_X[i], Status_Bar_Text_Y[i], True)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[i], Status_Action_Bar_Y[i], 1.48 * GameState.Character[i].Action_Point, 38))
            Text("AP: %i/100"   % GameState.Character[i].Action_Point, Text_Interface, Status_Action_X[i], Status_Bar_Text_Y[i], True)

def Fight_Action_Point():
    if all(i < 100 for i in Combat.Action_Point):    
        for i in range(6):
            if GameState.Character_Slot[i] == True and GameState.Character_Death[i] == False :
                GameState.Character[i].Action_Point += GameState.Character[i].Speed/10
                Combat.Action_Point[i]   = GameState.Character[i].Action_Point

                # Max Action Point = 100
                if GameState.Character[i].Action_Point > 100:
                    GameState.Character[i].Action_Point = 100

    else:
        for i in range(6):
            if Combat.Action_Point[i] >= 100 and Combat.Turn_Phase == "":
                Combat.Turn_Phase = i



def Turn_Phase():
    # Player Phase
    if Combat.Turn_Phase <= 2:
        # Active Turn Phase
        Sprite_Rect = GameState.Character[Combat.Turn_Phase].Sprite.get_rect(topleft=(Sprite_Character_X[Combat.Turn_Phase], Sprite_Character_Y[Combat.Turn_Phase]))
        pygame.draw.rect(gameDisplay, Color_Red, Sprite_Rect, 5)

    # Enemy Phase
    else:
        # Random Target Player
        Target_Player = random.randint(0,2)

        # Attack
        Attack(Target_Player)



def Attack_Choice():
    # State - Attack Selection
    Combat.Attack = True
    
    # Checking for Enemies
    if Combat.Button_Turn == False:
        Combat.Button_Turn = True
        for i in range(3,6):
            if GameState.Character_Slot[i] == True and GameState.Character_Death[i] == False:
                # Getting Sprite_Rect
                Sprite_Rect = GameState.Character[i].Sprite.get_rect(topleft=(Sprite_Character_X[i], Sprite_Character_Y[i]))

                # Selection Buttons
                Button(None, Text_Interface, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, 8, True, False, Color_Red, Color_Green, i, Attack)


                
def Attack(Selection):
    Combat.Attack = False
    # Turn Phase Character
    Character = GameState.Character[Combat.Turn_Phase]
        
    # RNG
    Hit = random.randint(0, 100)

    # Hit Chance (50+0.5*Level) * (Player.Speed^2/Enemy.Speed^2)
    Accuracy = (50 + (0.5*Character.Level)) * (Character.Speed**2 / GameState.Character[Selection].Speed**2)

    # Critical Chance (10+0.5*Level) * (Speed*Strength) / (5*Enemy.Defense*Player.Defense)
    Crit = (10 + (0.5*Character.Level)) * (Character.Speed*Character.Strength) / (GameState.Character[Selection].Defense*Character.Defense*5)

    if Accuracy >= Hit:
        # Damage
        if Crit<=Hit:
            GameState.Character[Selection].Health -= Character.Strength

        # Crit Damage
        else:
            GameState.Character[Selection].Health -= Character.Strength*2

        # HP Loss Cap
        if GameState.Character[Selection].Health < 0:
            GameState.Character[Selection].Health = 0
    End_Turn()

def End_Turn():
    # Turn Phase Character
    GameState.Character[Combat.Turn_Phase].Action_Point = 0

    Combat.Action_Point[Combat.Turn_Phase] = 0
    Combat.Turn_Phase = ""

    # Death Check
    for i in range(6):
        if GameState.Character_Slot[i] == True and GameState.Character[i].Health <= 0:
            GameState.Character_Death[i] = True
            GameState.Character[i].Action_Point = 0

    Combat.End_Turn = True

    Win()

def Win():
    if all(GameState.Character_Slot[4:6] and GameState.Character_Death[4:6]):
        Tools.Current_Progress += 1
        eval(Tools.Progress[Tools.Current_Progress])()
        

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
