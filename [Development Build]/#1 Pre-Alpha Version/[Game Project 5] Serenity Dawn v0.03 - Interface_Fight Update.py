import os
import pygame
import time
import pickle           # Load/Save Game
import random
import re               # re.split()

from Ressources     import *

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
        self.event = ""

class GameState():
    def __init__(self, name):
        self.Player = []
        self.Player_Slot = []
        self.Player_Death = []
        
        self.Enemy  = []
        self.Enemy_Slot = []
        self.Enemy_Death = []
GameState.Press = [0] * 300



def Quit_Game():
    pygame.quit()
    quit()

class Player:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Ellesia
        self.Sprite = Sprite_Ellesia
        self.Class  = "Lancer"
        
        self.Level      = 1
        self.Experience = 0
        self.Gold       = 0
        self.Action_Point = 100
        
        self.Maxhealth  = 44
        self.Health     = self.Maxhealth
        self.Strength   = 6
        self.Magic      = 10
        self.Speed      = 4
        self.Defense    = 2
        self.Resistance = 0
PlayerIG = Player("NightFore")

class Wolf:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Wolf
        self.Sprite = Sprite_Wolf
        
        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 10 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 3 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
WolfIG = Wolf("Wolf")


    
# Game - Main Function
def Title_Screen():

# Background
    gameDisplay.blit(Background_Title_Screen_1, (0,0))

# BGM
    pygame.mixer.music.load(OST_Title_Screen)
    pygame.mixer.music.play(-1)
    
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            pygame.display.update()
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
            
            Text_Display(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            Button("Start"  , "", 15, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Debug_Fight)
            Button("Gallery"  , "", 15, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, OST_Gallery)
            Button("Exit"   , "", 15, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Quit_Game)



def Debug_Fight():
# Background
    gameDisplay.blit(Background_Fight_1, (0,0))

# BGM
    pygame.mixer.music.load(OST_Menu_Victory_2)
    pygame.mixer.music.play(-1)

# Player / Enemy
    GameState.Player    = [PlayerIG,PlayerIG,PlayerIG]
    GameState.Player_Slot = [True,True,True]
    GameState.Player_Death = [False,False,False]
    
    GameState.Enemy     = [WolfIG,WolfIG,WolfIG]
    GameState.Enemy_Slot = [True,True,True]
    GameState.Enemy_Death = [False,False,False]

# Loop
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            pygame.display.update()
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
        gameDisplay.blit(ui_Fight_1, (0,0))
        Game_ui_Fight()
        

def Game_ui_Fight():
    # Commands
    Button("Attack", "", 0, 640, 590, 150, 45, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)
    Button("Skill" , "", 0, 640, 640, 150, 45, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)
    Button("Potion", "", 0, 640, 690, 150, 45, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)

    for i in range(3):
    # Player
        if GameState.Player_Slot[i] == True:
            # Sprite
            if GameState.Player_Death[i] == False:
                gameDisplay.blit(GameState.Player[i].Sprite,
                                 (Sprite_Player_X[i], Sprite_Player_Y[i]))

            # Icon
            gameDisplay.blit(GameState.Player[i].Icon, (Status_Icon_X[0], Status_Bar_Image_Y[i]))

            # Text
            Text_Display("%s"           % GameState.Player[i].name, Status_Name_X[0], Status_Bar_Text_Y[i], Text_Fight)
            Text_Display("HP: %i/%i"    % (GameState.Player[i].Health, GameState.Player[i].Maxhealth), Status_Health_X[0], Status_Bar_Text_Y[i], Text_Fight)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[0], Status_Action_Bar_Y[i], 1.48 * GameState.Player[i].Action_Point, 38))
            Text_Display("AP: %i/100"   % (GameState.Player[i].Action_Point), Status_Action_X[0], Status_Bar_Text_Y[i], Text_Fight)

    # Enemy   
        if GameState.Enemy_Slot[i] == True:
            # Sprite
            if GameState.Enemy_Death[i] == False:
                gameDisplay.blit(GameState.Enemy[i].Sprite,  (Sprite_Enemy_X[i], Sprite_Enemy_Y[i]))

            # Icon
            gameDisplay.blit(GameState.Enemy[i].Icon, (Status_Icon_X[1], Status_Bar_Image_Y[i]))

            # Text
            Text_Display("%s"           % GameState.Enemy[i].name, Status_Name_X[1], Status_Bar_Text_Y[i], Text_Fight)
            Text_Display("HP: %i/%i"    % (GameState.Enemy[i].Health,  GameState.Enemy[i].Maxhealth),    Status_Health_X[1], Status_Bar_Text_Y[i], Text_Fight)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[1], Status_Action_Bar_Y[i], 1.48 * GameState.Enemy[i].Action_Point, 38))
            Text_Display("AP: %i/100"   % (GameState.Enemy[i].Action_Point), Status_Action_X[1], Status_Bar_Text_Y[i], Text_Fight)


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

def Text_Button_2(msg):
    font = pygame.font.SysFont(None, 100)
    textSurface = font.render(msg, True, Color_Blue)
    return textSurface, textSurface.get_rect()

def Text_Fight(msg):
    font = pygame.font.SysFont(None, 35)
    textSurface = font.render(msg, True, Color_Black)
    return textSurface, textSurface.get_rect()
    
# Tools
def Grid_Draw(Row,Col,Gap, x,y,w,h,Color):
    Grid = [[0]*Row for n in range(Col)]
    x0 = x
    
    for row in Grid:
        for col in row:
            Rectangle = (x,y,w,h)
            # Border
            pygame.draw.rect(gameDisplay, Color_Black, Rectangle, 10)

            # Fill
            Grid_Color(Grid, Rectangle, col, Color)

            # Position
            x = x+w
        y = y+h+Gap     # Gap = Space between row
        x = x0          # Rectification



def Grid_Color(Grid, Rectangle, col, Color):
    if Color == "":
        pygame.draw.rect(gameDisplay, Color_Black, Rectangle)
        
    if Color == "Standard":
##        Grid[5][2] = 1
##        Grid[5][3] = 2
##        Grid[5][4] = 3
        
        for i in range(4):
            if col == i:
                pygame.draw.rect(gameDisplay, Color_Grid[i], Rectangle)
        


def Button(msg, Selection, width, x,y,w,h, ac,ic, Text_Font, event, Center, action=None):
    # msg       = Message insde Button
    # Selection = Button Number (Multiple)
    # width     = Border witdh
    # x,y,w,h   = Position
    # ac/ic     = Active/Inactive Color

    if Center == True:
        x = x-(w/2)                         # Center X (Box)
        y = y-(h/2)                         # Center Y (Box)
        
    Box = pygame.Rect(x,y,w,h)              # Box Surface
    x = x+(w/2)                             # Center X (Message)
    y = y+(h/2)                             # Center Y (Message)
    
    mouse = pygame.mouse.get_pos()

    pygame.draw.rect(gameDisplay, Color_Black, Box, width)
    
    # Active Color
    if Box.collidepoint(mouse):
        pygame.draw.rect(gameDisplay, ac, Box)
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

Title_Screen()

##            
##def Game_Intro_1():
##    pygame.mixer.music.load(Serenity)
##    pygame.mixer.music.play(-1)
##    
##    GameStateIG.Text_File = open("0.0.1_Cutscene_Introduction.txt", "r")
##    
### Setup
##    gameExit = False
##    while not gameExit:
##        events = pygame.event.get()
##        pygame.display.update()
##        gameDisplay.blit(Game_ui_Screen, (0,0))
##        gameDisplay.blit(Background_Introduction, (0,0))
##        Game_Text_Event()
##        
### "0.0.1_Cutscene_Introduction.txt"
##        if GameStateIG.Event[1] == False :
##            Text_Input(events, GameStateIG.Text_File)
##            
##            if GameStateIG.Text_Order == 4:
##                GameStateIG.State = "Character Name"
##                
##            if GameStateIG.State == "Character Name":
##                if GameStateIG.Text_Line_Input != "":
##                    PlayerIG = Player(GameStateIG.Text_Line_Input)
##                    GameStateIG.Player[0] = PlayerIG
##
##                    GameStateIG.Text_File = open("0.0.2_Cutscene_Introduction.txt", "r")
##                    Game_State_Reset("Event")
##                    GameStateIG.Event[1] = True
##
### "0.0.2_Cutscene_Introduction.txt"
##        elif GameStateIG.Event[2] == False:
##            Text_Input(events, GameStateIG.Text_File)
##
##            if GameStateIG.Text_Order == 18:
##                Game_Intro_2()
##
##        for event in events:
##            GameStateIG.event = event
##            if event.type == pygame.QUIT:
##                exit()
##
##
##
##
##def Game_Intro_2():
##    pygame.mixer.music.load(Around_a_Campfire)
##    pygame.mixer.music.play(-1)
##
##    Game_State_Reset("All")
##    GameStateIG.Text_File = open("0.1.1_Cutscene_Introduction_2.txt", "r")
##
### Setup
##    gameExit = False
##    while not gameExit:
##        events = pygame.event.get()
##        pygame.display.update()
##        gameDisplay.blit(Game_ui_Screen, (0,0))
##        gameDisplay.blit(Background_House, (0,0))
##        Game_Text_Event()
##
### "0.1.1_Cutscene_Introduction.txt"
##        if GameStateIG.Event[1] == False:
##            Text_Input(events, GameStateIG.Text_File)
##            
##            if GameStateIG.Text_Order == 0:
##                gameDisplay.blit(Game_ui_Screen_Black, (0,0))
##                Text_Display("1 Week Later...", display_width/2, display_height*3/8, Text_Introduction)
##
##            if GameStateIG.Text_Order == 3:
##                if GameStateIG.Sound == False:
##                    Sound_Wolf_Roar.play()
##                    GameStateIG.Sound = True
##
##            if GameStateIG.Text_Order == 4:
##                GameStateIG.Sound = False
##
##            if GameStateIG.Text_Order == 6:
##                if GameStateIG.Sound == False:
##                    Sound_Wolf_Roar.play()
##                    GameStateIG.Sound = True
##                    
##            if GameStateIG.Text_Order == 7:
##                GameStateIG.State = "Level_Fight"
##                GameStateIG.Background = "Level_Fight"
##                Main_Menu()
##
##
##        for event in events:
##            GameStateIG.event = event
##            if event.type == pygame.QUIT:
##                exit()
##        
##
##def Main_Menu():
##    gameExit = False
##    while not gameExit:
##        events = pygame.event.get()
##        pygame.display.update()
##        
##        if GameStateIG.Background == "Cutscene":
##            gameDisplay.blit(Game_ui_Screen, (0,0))
##
##        Game_Text_Event()
##        for event in events:
##            GameStateIG.event = event
##            if event.type == pygame.QUIT:
##                exit()
##                
##    # Main_Menu
##            if GameStateIG.State == "":
##                # Background
##                if GameStateIG.Zone_Progress == 1:
##                    if GameStateIG.Background == "":
##                        gameDisplay.blit(Background_Main_Menu_1, (0,0))
##
##                # Menu
##                Interface_Main_Menu()
##                if GameStateIG.Menu == "Inventory":
##                    Inventory()
##
##                if GameStateIG.Menu == "Shop":
##                    Shop()
##                        
##
##
##            # Fight
##            if GameStateIG.State == "Level_Fight":
##                Level_Fight()
##                Player_Enemy_Check()
##                Action_Point()
##
##                if GameStateIG.Attack_Choice == True:
##                    Attack_Choice()
##                Win_Condition()
##
##            # Win
##            elif GameStateIG.State == "Win":
##                Win(events)
##
##            # Results
##            elif GameStateIG.State == "Result":
##                Game_State_Reset("Text")
##                GameStateIG.Background = "Result"
##                gameDisplay.blit(Interface_Results, (0,0))
##                Battle_Result()
##
##
##def Player_Enemy_Check():
##    if GameStateIG.Player[0] != "":
##        GameStateIG.Player_Slot[0] = True
##        
##    if GameStateIG.Player[1] != "":
##        GameStateIG.Player_Slot[1] = True
##        
##    if GameStateIG.Player[2] != "":
##        GameStateIG.Player_Slot[2] = True
##        
##    if GameStateIG.Enemy[0] != "" and GameStateIG.Enemy[0] != NoMonsterIG:
##        GameStateIG.Enemy_Slot[0] = True
##        
##    if GameStateIG.Enemy[1] != "" and GameStateIG.Enemy[1] != NoMonsterIG:
##        GameStateIG.Enemy_Slot[1] = True
##        
##    if GameStateIG.Enemy[2] != "" and GameStateIG.Enemy[2] != NoMonsterIG:
##        GameStateIG.Enemy_Slot[2] = True
##        
##
##def Win_Condition():
##    if GameStateIG.Enemy[0].Health <= 0:
##        GameStateIG.Enemy_Death[0] = True
##        
##    if GameStateIG.Enemy[1].Health <= 0:
##        GameStateIG.Enemy_Death[1] = True
##        
##    if GameStateIG.Enemy[2].Health <= 0:
##        GameStateIG.Enemy_Death[2] = True
##
##    if GameStateIG.Enemy_Death == [True,True,True]:
##        Game_State_Reset("Win")
##
##def Win(events):
##    if GameStateIG.Zone_Progress == 1:
##        if GameStateIG.Music == False:
##            pygame.mixer.music.load(Finally_Some_Rest)
##            pygame.mixer.music.play(-1)
##            GameStateIG.Music = True
##        
##        if GameStateIG.Stage_Progress == 0:
##            if GameStateIG.Text_Cutscene == False:
##                GameStateIG.Text_File = open("1.0.0_Victory.txt", "r")
##                GameStateIG.Text_Cutscene = True
##                
##            if GameStateIG.Text_Cutscene == True:
##                Text_Input(events, GameStateIG.Text_File)
##
##            if GameStateIG.Text_Order == 5:
##                GameStateIG.State = "Result"
##
##
##GameStateIG.Player = [PlayerIG, IrisIG, GyreiIG]
##Game_Intro_2()
