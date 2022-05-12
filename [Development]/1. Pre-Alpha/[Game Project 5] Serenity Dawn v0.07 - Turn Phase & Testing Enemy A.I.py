import os
import pygame
import time
import pickle           # Load/Save Game
import random
import re               # re.split()

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
        self.event = ""
Tools = Tools("Tools")

class GameState():
    def __init__(self, name):
        # Interface Fight
        self.Player = []
        self.Player_Slot = []
        self.Player_Death = []
        
        self.Enemy  = []
        self.Enemy_Slot = []
        self.Enemy_Death = []

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
    GameState.Player    = [PlayerIG,IrisIG,GyreiIG]
    GameState.Player_Slot = [True,True,True]
    GameState.Player_Death = [False,False,False]
    
    GameState.Enemy     = [WolfIG,DirewolfIG,GhoulIG]
    GameState.Enemy_Slot = [True,True,True]
    GameState.Enemy_Death = [False,False,False]
##################################
    
# Loop
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
        gameDisplay.blit(ui_Fight_1, (0,0))
        Game_ui_Fight()
        
        Fight_Action_Point()

        # State - Turn Phase
        if GameState.Turn_Phase != "":        
            Turn_Phase()
            
        # State - Attack Selection
        if GameState.Attack_Choice == True:
            Attack_Choice()
            
        pygame.display.update()






        
        
def Game_ui_Fight():
    # Commands
    if GameState.Turn_Phase != "" and GameState.Turn_Phase <= 3:
        Button("Attack", "", 6, 640, 590, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, Attack_Choice)
        Button("Skill" , "", 6, 640, 640, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)
        Button("Potion", "", 6, 640, 690, 140, 40, Color_Button, Color_Red, Text_Button_1, Tools.event, True, None)

    Text_Display("Turn: %s"     % GameState.Turn_Count      , Turn_Count_X  , Turn_Count_Y  , Text_Fight)
    Text_Display("Stage: %s"    % GameState.Stage_Progress  , Stage_X       , Stage_Y       , Text_Fight)

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


def Fight_Action_Point():
    if all(i <= 100 for i in GameState.Action_Point):    
        for i in range(3):
            GameState.Player[i].Action_Point += GameState.Player[i].Speed/10
            GameState.Enemy[i].Action_Point += GameState.Enemy[i].Speed/10
            GameState.Action_Point[i]   = GameState.Player[i].Action_Point
            GameState.Action_Point[i+3] = GameState.Enemy[i].Action_Point

    else:
        for i in range(6):
            if GameState.Action_Point[i] >= 100:
                GameState.Turn_Phase = i

def Turn_Phase():
    # Player Phase
    if GameState.Turn_Phase <= 2:
        Sprite_Rect = GameState.Player[GameState.Turn_Phase].Sprite.get_rect(topleft=(Sprite_Player_X[GameState.Turn_Phase], Sprite_Player_Y[GameState.Turn_Phase]))
        pygame.draw.rect(gameDisplay, Color_Red, Sprite_Rect, 5)

    # Enemy Phase
    else:
        Target_Player = random.randint(0,2)
        Attack(Target_Player)

        




    
def Attack_Choice():
    # State - Attack Selection
    GameState.Attack_Choice = True
    
    # Checking for Enemies
    for i in range(3):
        if GameState.Enemy_Slot[i] == True and GameState.Enemy_Death[i] == False:
            # Getting Sprite_Rect
            Sprite_Rect = GameState.Enemy[i].Sprite.get_rect(topleft=(Sprite_Enemy_X[i], Sprite_Enemy_Y[i]))

            # Selection Buttons
            Button("", i, -8, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, Color_Red, Color_Button, Text_Fight, Tools.event, "", Attack)


def Attack(Selection):
    GameState.Attack_Choice = False
    # Turn Phase Character
    if GameState.Turn_Phase <= 3:
        Character = GameState.Player[GameState.Turn_Phase]
    else:
        Character = GameState.Enemy[GameState.Turn_Phase-3]
    
    # RNG
    Hit = random.randint(0, 100)

    # Hit Chance (50+0.5*Level) * (Player.Speed^2/Enemy.Speed^2)
    Accuracy = (50 + (0.5*Character.Level)) * (Character.Speed**2 / GameState.Enemy[Selection].Speed**2)

    # Critical Chance (10+0.5*Level) * (Speed*Strength) / (5*Enemy.Defense*Player.Defense)
    Crit = (10 + (0.5*Character.Level)) * (Character.Speed*Character.Strength) / (GameState.Enemy[Selection].Defense*Character.Defense*5)

    if Accuracy >= Hit:
        # Damage
        if Crit<=Hit:
            GameState.Enemy[Selection].Health -= Character.Strength

        # Crit Damage
        else:
            GameState.Enemy[Selection].Health -= Character.Strength*2

        # HP Loss Cap
        if GameState.Enemy[Selection].Health < 0:
            GameState.Enemy[Selection].Health = 0

    End_Turn()

def End_Turn():
    # Turn Phase Character
    if GameState.Turn_Phase <= 3:
        GameState.Player[GameState.Turn_Phase].Action_Point = 0
    else:
        GameState.Enemy[GameState.Turn_Phase-3].Action_Point = 0

    GameState.Action_Point[GameState.Turn_Phase] = 0
    GameState.Turn_Phase = ""


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
