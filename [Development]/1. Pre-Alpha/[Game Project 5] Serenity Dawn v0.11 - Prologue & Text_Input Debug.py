import os
import pygame
import time
import pickle           # Load/Save Game
import random
import re               # re.split()

import pygame_textinput
from Ressources     import *
from Balance        import *

pygame.init()
clock = pygame.time.Clock()

# Title
Project_Title = "Serenity Dawn"
pygame.display.set_caption(Project_Title)

# Screen Size
display_width   = 1280
display_height  = 720
gameDisplay = pygame.display.set_mode((display_width, display_height))



class Tools():
    def __init__(self, name):
        self.event              = ""                                # Button
        self.events             = ""                                # Text

        self.Background         = ""

        # Text
        self.Text_File          = ""                                # Read File

        self.Text               = ""                                # Read
        self.Text_Line          = ["","","","","","","","",""]      # Text Displayed
        self.Text_Order         = 1                                 # Order

        self.Input_State        = False 
        self.textinput          = pygame_textinput.TextInput()      # Input
        self.Text_Line_Input    = ""                                # Text Input

Tools = Tools("Tools")

class GameState():
    def __init__(self, name):
        # Interface Fight
        self.Character = [PlayerIG]
        self.Character_Slot = []
        self.Character_Death = []

        # State
        self.Attack_Choice = False
        self.Turn_Count     = 1
        self.Stage_Progress = 1
        
        # Fight Status
        self.Turn = [False,False,False,False,False,False]
        self.Turn_Order = 0
        
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
        self.Turn_Phase     = ""
GameState = GameState("GameState")



def Quit_Game():
    pygame.quit()
    quit()




    
# Game - Main Function
def Title_Screen():

# Background
    Tools.Background = Background_Title_Screen_1
    Background()
    
# BGM
    pygame.mixer.music.load(OST_Title_Screen)
    pygame.mixer.music.play(-1)

# Setup
    gameExit = False
    while not gameExit:
        pygame.display.update()
        Tools.events = pygame.event.get()
        
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
                
            Text_Display(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            Button("Start"      , "", 15, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Prologue)
            Button("Gallery"    , "", 15, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, OST_Gallery)
            Button("Debug"      , "", 15, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Debug_Fight)
        


def Prologue():
# Background
    Tools.Background = Background_Prologue
    Background()
    
# BGM
    pygame.mixer.music.load(OST_Cutscene_1_1)
    pygame.mixer.music.play(-1)

# Story
    Tools.Text_File = open(List_Story[0], "r")
    
# Setup
    gameExit = False
    while not gameExit:
        pygame.display.update()
        Tools.events = pygame.event.get()
        Text_Input()
        Story_Text_Display()
        
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
            
            Text_Display(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            Button("Start"      , "", 15, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Prologue)
            Button("Gallery"    , "", 15, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, OST_Gallery)
            Button("Debug"      , "", 15, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Debug_Fight)                


def Debug_Fight():
# Background
    gameDisplay.blit(Background_Fight_1, (0,0))

# BGM
    pygame.mixer.music.load(OST_Menu_Victory_2)
    pygame.mixer.music.play(-1)

# Player / Enemy
    GameState.Character         = [PlayerIG ,IrisIG     ,GyreiIG,
                                   WolfIG   ,DirewolfIG ,GhoulIG]
    GameState.Character_Slot    = [True,True,True,True,True,True]
    GameState.Character_Death   = [False,False,False,False,False,False]
    
# Loop
    gameExit = False
    while not gameExit:
        pygame.display.update()
        Tools.events = pygame.event.get()
        
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
        gameDisplay.blit(ui_Fight_1, (0,0))
        Game_ui_Fight()

        # State - Action Point
        Fight_Action_Point()

        # State - Turn Phase
        if GameState.Turn_Phase != "":
            Turn_Phase()
            
        # State - Attack Selection
        if GameState.Attack_Choice == True:
            Attack_Choice()
            
        pygame.display.update()



def Game_ui_Fight():
    # Information
    Text_Display("Turn: %s"     % GameState.Turn_Count      , Turn_Count_X  , Turn_Count_Y  , Text_Interface)
    Text_Display("Stage: %s"    % GameState.Stage_Progress  , Stage_X       , Stage_Y       , Text_Interface)
    
    # Commands
    if GameState.Turn_Phase != "" and GameState.Turn_Phase <= 2:
        Button("Attack", "", 6, 640, 590, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, Attack_Choice)
        Button("Skill" , "", 6, 640, 640, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)
        Button("Potion", "", 6, 640, 690, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)

    # Player / Enemy
    for i in range(6):
        if GameState.Character_Slot[i] == True:
            # Sprite
            if GameState.Character_Death[i] == False:
                gameDisplay.blit(GameState.Character[i].Sprite, (Sprite_Character_X[i], Sprite_Character_Y[i]))

            # Icon
            gameDisplay.blit(GameState.Character[i].Icon, (Status_Icon_X[i], Status_Bar_Image_Y[i]))

            # Text
            Text_Display("%s"           % GameState.Character[i].name, Status_Name_X[i], Status_Bar_Text_Y[i], Text_Interface)
            Text_Display("HP: %i/%i"    % (GameState.Character[i].Health, GameState.Character[i].Maxhealth), Status_Health_X[i], Status_Bar_Text_Y[i], Text_Interface)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[i], Status_Action_Bar_Y[i], 1.48 * GameState.Character[i].Action_Point, 38))
            Text_Display("AP: %i/100"   % (GameState.Character[i].Action_Point), Status_Action_X[i], Status_Bar_Text_Y[i], Text_Interface)


def Fight_Action_Point():
    if all(i < 100 for i in GameState.Action_Point):    
        for i in range(6):
            if GameState.Character_Death[i] == False :
                GameState.Character[i].Action_Point += GameState.Character[i].Speed/10
                GameState.Action_Point[i]   = GameState.Character[i].Action_Point

                # Max Action Point = 100
                if GameState.Character[i].Action_Point > 100:
                    GameState.Character[i].Action_Point = 100

    else:
        for i in range(6):
            if GameState.Action_Point[i] >= 100 and GameState.Turn_Phase == "":
                GameState.Turn_Phase = i



def Turn_Phase():
    # Player Phase
    if GameState.Turn_Phase <= 2:
        # Active Turn Phase
        Sprite_Rect = GameState.Character[GameState.Turn_Phase].Sprite.get_rect(topleft=(Sprite_Character_X[GameState.Turn_Phase], Sprite_Character_Y[GameState.Turn_Phase]))
        pygame.draw.rect(gameDisplay, Color_Red, Sprite_Rect, 5)

    # Enemy Phase
    else:
        # Random Target Player
        Target_Player = random.randint(0,2)

        # Attack
        Attack(Target_Player)



def Attack_Choice():
    # State - Attack Selection
    GameState.Attack_Choice = True
    
    # Checking for Enemies
    for i in range(3,6):
        if GameState.Character_Slot[i] == True and GameState.Character_Death[i] == False:
            # Getting Sprite_Rect
            Sprite_Rect = GameState.Character[i].Sprite.get_rect(topleft=(Sprite_Character_X[i], Sprite_Character_Y[i]))

            # Selection Buttons
            Button("", i, -8, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, Color_Red, Color_Button, Text_Interface, Tools.event, "", Attack)


def Attack(Selection):
    GameState.Attack_Choice = False
    # Turn Phase Character
    Character = GameState.Character[GameState.Turn_Phase]
        
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
    GameState.Character[GameState.Turn_Phase].Action_Point = 0

    GameState.Action_Point[GameState.Turn_Phase] = 0
    GameState.Turn_Phase = ""

    # Death Check
    for i in range(6):
        if GameState.Character[i].Health <= 0:
            GameState.Character_Death[i] = True
            GameState.Character[i].Action_Point = 0


def OST_Gallery():
# Background
    gameDisplay.fill(Color_Blue)

# Loop
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            pygame.display.update()
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game() 

            Music_Selection = 0
            for row in range(5):
                if Music_Selection >= len(List_OST):
                    break
                
                for col in range(6):
                    Button("Music %i" % (Music_Selection+1), Music_Selection, 12, 60+(40+display_width/8)*col, 100+(40+display_height/10)*row, display_width/8, display_height/10, Color_Green, Color_Red, Text_Button_1, event, False, Music_Play)
                    Music_Selection += 1
                    if Music_Selection >= len(List_OST):
                        break

            Button_Image(1240, 10, Icon_Exit, Icon_Exit, event, "", Title_Screen)

# Gallery Music
def Music_Play(Selection):
        pygame.mixer.music.load(List_OST[Selection])
        pygame.mixer.music.play(-1)



# Text - Main Function
def Text_Display(msg, x, y, Text_Font):
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
        


def Button(msg, Selection, width, x,y,w,h, ac,ic, Text_Font, event, Center, action=None):
    # msg       = Message insde Button
    # Selection = Button Number (Multiple)
    # width     = Border witdh
    # x,y,w,h   = Position
    # ac/ic     = Active/Inactive Color

    # if width < 0 : no fill
    mouse = pygame.mouse.get_pos()
    
    if Center == True:
        x = x-(w/2)                         # Center X (Box)
        y = y-(h/2)                         # Center Y (Box)
        
    Box = pygame.Rect(x,y,w,h)              # Box Surface
    x = x+(w/2)                             # Center X (Message)
    y = y+(h/2)                             # Center Y (Message)
    
    pygame.draw.rect(gameDisplay, Color_Black, Box, abs(width))

    # Active Color
    if Box.collidepoint(mouse):
        if width >= 0:
            pygame.draw.rect(gameDisplay, ac, Box)
        else:   # No Fill
            pygame.draw.rect(gameDisplay, ac, Box, abs(width))
            
        # Action
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if action != None:
                    if Selection != "":
                        action(Selection)
                    else:
                        action()
    # Inactive Color
    else:
        if width >= 0:
            pygame.draw.rect(gameDisplay, ic, Box)

    # Button Message
    textSurf, textRect = Text_Font(msg)

    # Button Rect
    textRect.center = x, y
    gameDisplay.blit(textSurf, textRect)


    
def Button_Image(x, y, Inactive, Active, event, Selection, action=None):
    mouse = pygame.mouse.get_pos()  
    Icon_ic = Inactive.convert()
    Icon_ac = Active.convert()
    Icon_ic_rect = Icon_ic.get_rect(topleft=(x,y))
    Icon_ac_rect = Icon_ac.get_rect(topleft=(x,y))

    
    if Icon_ic_rect.collidepoint(mouse):
        gameDisplay.blit(Active, Icon_ac_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if action != None:
                if Selection == "":
                    action()
                else:
                    action(Selection)
    else:
        gameDisplay.blit(Inactive, Icon_ic_rect)



def Background():
    gameDisplay.blit(Tools.Background, (0,0))

def Text_Input():
    # Text Read
    if Tools.textinput.update(Tools.events):
        # Background (Erase Text)
        Background()

        # Text Input
        Tools.Text_Line_Input   = Tools.textinput.get_text()
        Tools.textinput         = pygame_textinput.TextInput()

        
        # Read File
        Tools.Text = Tools.Text_File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

        Tools.Text_Line[Tools.Text_Order]   = Tools.Text
        Tools.Text_Line[Tools.Text_Order+1] = "(-> Press Enter)"
        
        Tools.Text_Order += 1

        # Reset Text
        if Tools.Text_Order == 7:
            Tools.Text_Line = ["","","","","","","","",""]
            Tools.Text_Order = 1

    if Tools.Input_State == True:
        pygame.draw.rect(gameDisplay, Color_Black, [295, 395, 210, 40])
        pygame.draw.rect(gameDisplay, Color_Grey, [300, 400, 200, 30])
        gameDisplay.blit(Tools.textinput.get_surface(), (305, 405))



def Story_Text_Display():
    # Text
    Text_Display(Tools.Text_Line[1], 300, 350, Text_Interface)
    Text_Display(Tools.Text_Line[2], 300, 370, Text_Interface)
    Text_Display(Tools.Text_Line[3], 300, 390, Text_Interface)
    Text_Display(Tools.Text_Line[4], 300, 410, Text_Interface)
    Text_Display(Tools.Text_Line[5], 300, 430, Text_Interface)
    Text_Display(Tools.Text_Line[6], 300, 450, Text_Interface)
    Text_Display(Tools.Text_Line[7], 300, 470, Text_Interface)


Title_Screen()
