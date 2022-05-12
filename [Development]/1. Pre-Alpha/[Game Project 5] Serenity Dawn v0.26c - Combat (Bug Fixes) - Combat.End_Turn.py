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
        self.event          = ""        # Button
        self.events         = ""        # Text
        
        self.Background     = None
        self.Button         = []
        self.Button_Image   = []
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
        self.Zone           = 0
        self.Stage          = 0
        self.Story          = 0
        
        # Interface Fight
        self.Character      = [PlayerIG]
        self.Character_Slot     = []
        self.Character_Death    = []
GameState = GameState()



class Text():
    def __init__(self):
        self.textinput          = pygame_textinput.TextInput()

        # File
        self.File               = open(List_Story[0], "r")      # Read File
        self.Read               = ""                            # Text in File

        # State
        self.Event              = False                         # Continue/Stop Reading
        self.Input              = False                         # Writing

        # Left
        self.L_Character    = ""                            # Character Name
        self.L_Line         = ["","","","","","","","",""]  # Text
        self.L_Order        = 1                             # Line

        # Right
        self.R_Character    = ""                            # Character Name
        self.R_Line         = ["","","","","","","","",""]  # Text
        self.R_Order        = 1                             # Line
Text = Text()



class Button():
    def __init__(self, text, font, x,y,w,h,b,border,center, active,inactive, selection, action=None):
        self.text       = text
        self.font       = font

        self.x = x              # Position x
        self.y = y              # Position y
        self.w = w              # Width
        self.h = h              # Height
        self.b = b              # Border width
        self.border = border    # Border
        self.center = center    # Center
        
        self.color      = inactive
        self.active     = active    # Active Color
        self.inactive   = inactive  # Inactive Color

        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)

        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.color = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None:
                    if self.selection != None:
                        self.action(self.selection)
                    else:
                        self.action()
        else:
            self.color = self.inactive

    def update(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, self.rect, self.b)
        pygame.draw.rect(gameDisplay, self.color, self.rect)

        # Text
        textSurf, textRect = self.font(self.text)
        textRect.center = self.x+self.w/2, self.y+self.h/2
        gameDisplay.blit(textSurf, textRect)



class Button_Image():
    def __init__(self, x, y, center, active, inactive, selection, action=None):
        self.x = x              # Position x
        self.y = y              # Position y
        self.center = center    # Center
        
        self.image      = inactive.convert()
        self.active     = active.convert()      # Active image
        self.inactive   = inactive.convert()    # Inactive image

        if self.center == False:
            self.rect = self.active.get_rect(topleft=(x,y))

        if self.center == True:
            self.rect = self.active.get_rect(center=(x,y))

        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.image = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None:
                    if self.selection != None:
                        self.action(self.selection)
                    else:
                        self.action()
        else:
            self.image = self.inactive

    def update(self, index):
        # Button
        gameDisplay.blit(self.image, self.rect)



class Sprite():
    def __init__(self):
        self.Number         = 0
        self.Index          = 0
        
        self.x              = []
        self.y              = []
        self.center         = []
        self.action         = []
        
        self.path           = []    # Make sure to provide the relative or full path to the images directory.
        self.player         = []    # AnimatedSprite()
        self.all_sprites    = []    # Creates a sprite group and adds 'player' to it.
        
        self.dt             = []    # Amount of seconds between each loop.
        self.animation      = []    # Amount of time/frame before update
Sprite = Sprite()
        


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        # Image
        self.images         = AnimatedSprite.load_images(path=Sprite.path[Sprite.index])            # Load all images in the directory
        self.images_right   = self.images                                                           # Normal image
        self.images_left    = [pygame.transform.flip(image, True, False) for image in self.images]  # Flipping image.
        
        self.index = 0                                      # Current index
        self.image = self.images[self.index]                # Current image

        self.image_rect = self.image.get_rect()             # Surface of the image
        size = (self.image_rect[2], self.image_rect[3])     # This should match the size of the images.

        # Centering image
        if Sprite.center[Sprite.index] == False:
            self.rect = pygame.Rect((Sprite.x[Sprite.index], Sprite.y[Sprite.index]), size)
        
        if Sprite.center[Sprite.index] == True:
            self.rect = pygame.Rect((Sprite.x[Sprite.index]-self.image_rect[2]/2, Sprite.y[Sprite.index]-self.image_rect[3]/2), size)

        # Update
            #self.animation_time    = 0.1
        self.animation_time     = Sprite.animation[Sprite.index]    # Time before update
        self.current_time       = 0

            #self.animation_frames  = 6
        self.animation_frames   = Sprite.animation[Sprite.index]    # Frame before update
        self.current_frame      = 0

    def load_images(path):
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
        
    def button_image(index, x, y, event, action=None):
        """
        Calls the function Selection when clicking oh the image
        """
        mouse = pygame.mouse.get_pos()
        if Sprite.player[index].rect.collidepoint(mouse):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if action != None:
                    action()

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        
        self.current_time += dt
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

    def update(self, dt):
        """
        This is the method that's being called when 'all_sprites.update(dt)' is called.
        """
        # Switch between the two update methods by commenting/uncommenting.
        # self.update_time_dependent(dt)
        self.update_frame_dependent()



def Setup(Background, OST):
    # Tools
    Tools.Button, Tools.Button_Image = [], []

    # Background
    Tools.Background = Background

    # OST
    pygame.mixer.music.load(OST)
    pygame.mixer.music.play(-1)
    
def Setup_Loop(Button=None, Text=None, Sprite=None, Fight=None):
    # Tools
    pygame.display.update()
    Tools.events = pygame.event.get()

    # Background
    if Tools.Background != None:
        gameDisplay.blit(Tools.Background, (0,0))

    # Text
    if Text == True:
        Text_Input()
        Story_Text_Display()

    # Button
    if Button == True:
        for index in range(len(Tools.Button)):
            Tools.Button[index].update(index)
        for index in range(len(Tools.Button_Image)):
            Tools.Button_Image[index].update(index)

    for event in Tools.events:
        # Tools
        Tools.event = event

        if Button == True:
            # Button
            for index in range(len(Tools.Button)):
                Tools.Button[index].check(index)
            for index in range(len(Tools.Button_Image)):
                Tools.Button_Image[index].check(index)

    # Fight
    if Fight == True:
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
            Combat.End_Turn = False
            Tools.Button = []
            Combat.Button_Action = False
            Combat.Button_Turn = False

def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup(Background_Title_Screen_1, OST_Title_Screen)

    # Buttons
    Tools.Button.append(Button("Start",    Text_Button_1, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Prologue))
    Tools.Button.append(Button("Gallery",  Text_Button_1, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, OST_Gallery))
    Tools.Button.append(Button("Debug",    Text_Button_1, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Debug))
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup_Loop(Button=True)
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()  
        Text_Display_Center(Project_Title, display_width/2, display_height/4, Text_Title_Screen)



def OST_Gallery():
    # Setup
    Setup(Background_Title_Screen_2, OST_Title_Screen)

    # Music Button
    Music_Selection = 0
    for row in range(round(len(List_OST)/6)) :
        for col in range(6):
            if Music_Selection < len(List_OST):
                Tools.Button.append(Button("Music %i" % (Music_Selection+1), Text_Button_1, 60+(40+display_width/8)*col, 100+(40+display_height/10)*row, display_width/8, display_height/10, 12, True, False, Color_Green, Color_Red, Music_Selection, Music_Play))
                Music_Selection += 1

    # Exit Button
    Tools.Button_Image.append(Button_Image(1255, 25, True, Icon_Exit, Icon_Exit, None, Title_Screen))
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup_Loop(Button=True)
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

            

def Prologue():
    # Setup
    Setup(Background_Prologue, OST_Cutscene_1_1)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup_Loop(Text=True)
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()



def Debug():
    # Setup
    Setup(Background_Main_1, OST_Menu_Main_1_1)

    # Sprite Setup
    Sprite.Number = 2                             # Number of Sprite
    Sprite.x = [615, 1230]                        # Position x
    Sprite.y = [435, 520]                         # Position y
    Sprite.center = [True, True]                  # Center Sprite
    Sprite.action = [Training, Debug_Fight]       # Function
    Sprite.path = ["Data\Sprite_Button\Sprite_Button_Traning", "Data\Sprite_Button\Sprite_Button_Fight"]  # Sprite Path
    
    for Sprite.index in range(Sprite.Number):
        Sprite.animation.append(4)                # Frame before update
        Sprite.dt.append(clock.tick(FPS))
        Sprite.player.append(AnimatedSprite())
        Sprite.all_sprites.append(pygame.sprite.Group(AnimatedSprite()))
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup_Loop(Button=True)
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

            # Sprite Button
            for index in range(Sprite.Number):
                if callable(Sprite.action[index]) == True:   # Check Function
                    AnimatedSprite.button_image(index, Sprite.x[index], Sprite.y[index], Tools.event, Sprite.action[index])

        # Sprite Update
        for Sprite.index in range(Sprite.Number):
            Sprite.dt[Sprite.index] = clock.tick(FPS)   # No effects (using frames)
            Sprite.all_sprites[Sprite.index].update(Sprite.dt[Sprite.index])
            Sprite.all_sprites[Sprite.index].draw(gameDisplay)



def Training():
    # Setup
    Setup(Interface_Fight, List_OST[random.randint(7, 16)])

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
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()
        Setup_Loop(Button=True, Fight=True)



def Debug_Fight():
    # Setup
    Setup(Interface_Fight, OST_Menu_Victory_2)
    # Player / Enemy
    GameState.Character         = [PlayerIG, IrisIG, GyreiIG,   WolfIG, DirewolfIG, GhoulIG]
    GameState.Character_Slot    = [True,     True,   True,      True,   True,       True]
    GameState.Character_Death   = [False,    False,  False,     False,  False,      False]
    
    # Loop
    gameExit = False
    while not gameExit:
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()
        Setup_Loop(Button=True, Fight=True)
        print(Tools.Button)

            


def Game_ui_Fight():
    # Information
    Text_Display_Center("Turn: %s"     % Combat.Turn_Count      , Turn_Count_X  , Turn_Count_Y  , Text_Interface)
    Text_Display_Center("Stage: %s"    % GameState.Stage  , Stage_X       , Stage_Y       , Text_Interface)

    # Commands
    if Combat.Turn_Phase != "" and Combat.Turn_Phase <= 2:
        if Combat.Button_Action == False:
            Combat.Button_Action = True
            Tools.Button.append(Button("Attack", Text_Button_1, 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, Attack_Choice))
            Tools.Button.append(Button("Skill",  Text_Button_1, 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None))
            Tools.Button.append(Button("Potion", Text_Button_1, 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None))

    # Player / Enemy
    for i in range(6):
        if GameState.Character_Slot[i] == True:
            # Sprite
            if GameState.Character_Death[i] == False:
                gameDisplay.blit(GameState.Character[i].Sprite, (Sprite_Character_X[i], Sprite_Character_Y[i]))

            # Icon
            gameDisplay.blit(GameState.Character[i].Icon, (Status_Icon_X[i], Status_Bar_Image_Y[i]))

            # Text
            Text_Display_Center("%s"           % GameState.Character[i].name, Status_Name_X[i], Status_Bar_Text_Y[i], Text_Interface)
            Text_Display_Center("HP: %i/%i"    % (GameState.Character[i].Health, GameState.Character[i].Maxhealth), Status_Health_X[i], Status_Bar_Text_Y[i], Text_Interface)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[i], Status_Action_Bar_Y[i], 1.48 * GameState.Character[i].Action_Point, 38))
            Text_Display_Center("AP: %i/100"   % (GameState.Character[i].Action_Point), Status_Action_X[i], Status_Bar_Text_Y[i], Text_Interface)


def Fight_Action_Point():
    if all(i < 100 for i in Combat.Action_Point):    
        for i in range(6):
            if GameState.Character_Death[i] == False :
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
                Tools.Button.append(Button(None, Text_Interface, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, 8, True, False, Color_Red, Color_Green, i, Attack))


                
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
        if GameState.Character[i].Health <= 0:
            GameState.Character_Death[i] = True
            GameState.Character[i].Action_Point = 0


    Combat.End_Turn = True
            

# Gallery Music
def Music_Play(Selection):
    pygame.mixer.music.load(List_OST[Selection])
    pygame.mixer.music.play(-1)



# Text - Main Function
def Text_Display(msg, x, y, Text_Font):
    textSurf, textRect = Text_Font(msg)
    gameDisplay.blit(textSurf, (x,y))
    
def Text_Display_Center(msg, x, y, Text_Font):
    textSurf, textRect = Text_Font(msg)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)

# Text - Secondary Functions
def Text_Title_Screen(msg):
    font = pygame.font.SysFont(None, 100)
    textSurface = font.render(msg, True, Color_Title_Screen)
    return textSurface, textSurface.get_rect()

def Text_Button_1(msg):
    font = pygame.font.SysFont(None, 40)
    textSurface = font.render(msg, True, Color_Blue)
    return textSurface, textSurface.get_rect()

def Text_Interface(msg):
    font = pygame.font.SysFont(None, 35)
    textSurface = font.render(msg, True, Color_Black)
    return textSurface, textSurface.get_rect()


def Text_Input():
    # Read Text
    if Text.textinput.update(Tools.events):
        # Text Input
        Text.Line_Input = Text.textinput.get_text()
        Text.textinput  = pygame_textinput.TextInput()


        # Input Name Event
        if Text.Line_Input != "":
            Text.Input = False
            Text.Event = False
            
            PlayerIG.name   = Text.Line_Input
            Text.Line_Input = ""
            Text.Read       = "(NEXT)"


        # Next File
        if "(NEXT)" in Text.Read:
            Text.File.close()
            GameState.Story += 1
            Text.File = open(List_Story[GameState.Story], "r")
            Text.Read = ""

        # Event == Stop Reading
        if Text.Event == False:
            
            # Read File
            Text.Read = Text.File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

            # Event State
            if "(EVENT)" in Text.Read:
                Text.Event = True

            # Input State
            if "(INPUT)" in Text.Read:
                Text.Read       = Text.Read.strip("(INPUT)")
                Text.Line_Input = ""
                Text.Input      = True


        # Left Side
            if "[L]" in Text.Read:
            # Character Name
                if "(NAME)" in Text.Read:
                    Text.L_Character = Text.Read.replace("(NAME)[L]", "")
                    Text.Read = Text.File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))
            # Text
                Text.L_Line[Text.L_Order]   = Text.Read.replace("[L]", "")
                Text.L_Line[Text.L_Order+1] = "(-> Press Enter)"
                Text.R_Line[Text.R_Order+1] = ""
                Text.L_Order += 1

                # Reset Text
                if Text.L_Order == 7:
                    Text.L_Line     = 8*[""]
                    Text.L_Order    = 1

                

        # Right Side
            if "[R]" in Text.Read:
            # Character Name
                if "(NAME)" in Text.Read:
                    Text.R_Character = Text.Read.replace("(NAME)[R]", "")
                    Text.Read = Text.File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

            # Text
                Text.R_Line[Text.R_Order]   = Text.Read.replace("[R]", "")
                Text.R_Line[Text.R_Order+1] = "(-> Press Enter)"
                Text.L_Line[Text.L_Order+1] = ""
                Text.R_Order += 1

                # Reset Text
                if Text.R_Order == 7:
                    Text.R_Line     = 8*[""]
                    Text.R_Order    = 1



def Story_Text_Display():
    # Background
    gameDisplay.blit(Interface_Cutscene, (0,0))

    # Character Name
    Text_Display_Center(Text.L_Character, 100, 535, Text_Interface)
    Text_Display_Center(Text.R_Character, 1180, 535, Text_Interface) 

    # Text Left
    Text_Display(Text.L_Line[1], 5, 565, Text_Interface)
    Text_Display(Text.L_Line[2], 5, 585, Text_Interface)
    Text_Display(Text.L_Line[3], 5, 605, Text_Interface)
    Text_Display(Text.L_Line[4], 5, 625, Text_Interface)
    Text_Display(Text.L_Line[5], 5, 645, Text_Interface)
    Text_Display(Text.L_Line[6], 5, 665, Text_Interface)
    Text_Display(Text.L_Line[7], 5, 685, Text_Interface)

    # Text Right
    Text_Display(Text.R_Line[1], 725, 565, Text_Interface)
    Text_Display(Text.R_Line[2], 725, 585, Text_Interface)
    Text_Display(Text.R_Line[3], 725, 605, Text_Interface)
    Text_Display(Text.R_Line[4], 725, 625, Text_Interface)
    Text_Display(Text.R_Line[5], 725, 645, Text_Interface)
    Text_Display(Text.R_Line[6], 725, 665, Text_Interface)
    Text_Display(Text.R_Line[7], 725, 685, Text_Interface)

    # Input State
    if Text.Input == True:
        # Text Box
        pygame.draw.rect(gameDisplay, Color_Grey,   [540, 340, 200, 40])
        pygame.draw.rect(gameDisplay, Color_Black,  [540, 340, 200, 40], 5)

        # Text Center
        Text_Rect   = Text.textinput.get_surface()
        Width       = Text_Rect.get_width()
        Height      = Text_Rect.get_height()
        gameDisplay.blit(Text.textinput.get_surface(), (640-Width//2, 360-Height//2))


Title_Screen()
