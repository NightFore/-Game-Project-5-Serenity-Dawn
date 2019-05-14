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
        
        self.Background     = ""
        self.Button         = []

Tools = Tools()

class Fight():
    def __init__(self):
        # State
        self.Attack         = False
        self.Skill          = False
        
        self.Turn           = [False,False,False,False,False,False]
        self.Turn_Phase     = ""
        self.Turn_Order     = 0
        self.Turn_Count     = 1
        
        self.Active_Time    = 0
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
Fight = Fight()
        

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

class Test_Button():
    def __init__(self, text, font, x,y,w,h,b,border,center, active,inactive, selection, action):
        self.text       = text
        self.font       = font
        

        self.x = x              # Position x
        self.y = y              # Position y
        self.w = w              # Width
        self.h = h              # Height
        self.b = b              # Border width
        self.border = border    # Border
        self.center = center    # Center

        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)
        
        self.active     = active    # Active Color
        self.inactive   = inactive  # Inactive Color
        self.color      = inactive

        self.selection  = selection
        self.action     = action

            
        
    def update(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, Tools.Button[index].rect, self.b)
            
        pygame.draw.rect(gameDisplay, Tools.Button[index].color, Tools.Button[index].rect)

        # Text
        textSurf, textRect = Tools.Button[index].font(Tools.Button[index].text)
        Text_x, Text_y = Tools.Button[index].x + Tools.Button[index].w/2, Tools.Button[index].y + Tools.Button[index].h/2
        
        textRect.center = Text_x, Text_y
        gameDisplay.blit(textSurf, textRect)

        self.check(index)###

        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if Tools.Button[index].rect.collidepoint(mouse):
            Tools.Button[index].color = Tools.Button[index].active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if Tools.Button[index].action != None:
                    Tools.Button[index].action()
        else:
            Tools.Button[index].color = Tools.Button[index].inactive

    
# Game - Main Function
def Title_Screen():
    Tools.Button.append(Test_Button("Start",    Text_Button_1, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, "", Prologue))
    Tools.Button.append(Test_Button("Gallery",  Text_Button_1, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, "", OST_Gallery))
    Tools.Button.append(Test_Button("Debug",    Text_Button_1, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, "", Debug))

    # Setup
    Tools.Background = Background_Title_Screen_1
    pygame.mixer.music.load(OST_Title_Screen)
    pygame.mixer.music.play(-1)
    
    # Loop
    gameExit = False
    while not gameExit:
        # Setup
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()

            index = 0
            for i in Tools.Button:
                Tools.Button[index].update(index)
                index += 1

            Text_Display_Center(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            
            pygame.display.update()
        


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



def OST_Gallery():
    # Setup
    Tools.Background = Background_Title_Screen_2
    pygame.mixer.music.load(OST_Title_Screen)
    pygame.mixer.music.play(-1)
    
    # Loop
    gameExit = False
    while not gameExit:
        # Setup
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()

            # Exit Button
            Button_Image(1240, 10, Icon_Exit, Icon_Exit, Tools.event, "", Title_Screen)

            # Music Button
            Music_Selection = 0
            Row = round(len(List_OST)/6)
            
            for row in range(Row):
                for col in range(6):
                    Button("Music %i" % (Music_Selection+1), Music_Selection, 12, 60+(40+display_width/8)*col, 100+(40+display_height/10)*row, display_width/8, display_height/10, Color_Green, Color_Red, Text_Button_1, Tools.event, False, Music_Play)
                    Music_Selection += 1
                    if Music_Selection >= len(List_OST):
                        break

            pygame.display.update()



def Quit_Game():
    pygame.quit()
    quit()


def Prologue():
    # Setup
    Tools.Background = Background_Prologue
    pygame.mixer.music.load(OST_Cutscene_1_1)
    pygame.mixer.music.play(-1)
    
    # Loop
    gameExit = False
    while not gameExit:
        # Setup
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Tools
        Text_Input()
        Story_Text_Display()

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()

            pygame.display.update()




    
# Game - Main Function
def Debug():
    # Setup
    Tools.Background = Background_Main_1
    pygame.mixer.music.load(OST_Menu_Main_1_1)
    pygame.mixer.music.play(-1)

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
        # Setup
        pygame.display.update()
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Sprite Update
        for Sprite.index in range(Sprite.Number):
            Sprite.dt[Sprite.index] = clock.tick(FPS)   # No effects (using frames)
            Sprite.all_sprites[Sprite.index].update(Sprite.dt[Sprite.index])
            Sprite.all_sprites[Sprite.index].draw(gameDisplay)
        
        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()

            # Sprite Button
            for index in range(Sprite.Number):
                if callable(Sprite.action[index]) == True:   # Check Function
                    AnimatedSprite.button_image(index, Sprite.x[index], Sprite.y[index], Tools.event, Sprite.action[index])
                    

def Debug_Action_1():
    print("Click 1!")
    
def Debug_Action_2():
    print("Click 2!")



def Training():
    # Setup
    Tools.Background = Interface_Fight
    pygame.mixer.music.load(List_OST[random.randint(7, 16)])
    pygame.mixer.music.play(-1)

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
        # Setup
        pygame.display.update()
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Interface
        Game_ui_Fight()

        # State - Action Point
        Fight_Action_Point()

        # State - Turn Phase
        if Fight.Turn_Phase != "":
            Turn_Phase()
            
        # State - Attack Selection
        if Fight.Attack == True:
            Attack_Choice()

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
    
            
        


def Debug_Fight():
    # Setup
    Tools.Background = Interface_Fight
    pygame.mixer.music.load(OST_Menu_Victory_2)
    pygame.mixer.music.play(-1)

    # Player / Enemy
    GameState.Character         = [PlayerIG, IrisIG, GyreiIG,   WolfIG, DirewolfIG, GhoulIG]
    GameState.Character_Slot    = [True,     True,   True,      True,   True,       True]
    GameState.Character_Death   = [False,    False,  False,     False,  False,      False]
    
    # Loop
    gameExit = False
    while not gameExit:
        # Setup
        pygame.display.update()
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))

        # Interface
        Game_ui_Fight()

        # State - Action Point
        Fight_Action_Point()

        # State - Turn Phase
        if Fight.Turn_Phase != "":
            Turn_Phase()
            
        # State - Attack Selection
        if Fight.Attack == True:
            Attack_Choice()

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
            


def Game_ui_Fight():
    # Information
    Text_Display_Center("Turn: %s"     % Fight.Turn_Count      , Turn_Count_X  , Turn_Count_Y  , Text_Interface)
    Text_Display_Center("Stage: %s"    % GameState.Stage  , Stage_X       , Stage_Y       , Text_Interface)
    
    # Commands
    if Fight.Turn_Phase != "" and Fight.Turn_Phase <= 2:
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
            Text_Display_Center("%s"           % GameState.Character[i].name, Status_Name_X[i], Status_Bar_Text_Y[i], Text_Interface)
            Text_Display_Center("HP: %i/%i"    % (GameState.Character[i].Health, GameState.Character[i].Maxhealth), Status_Health_X[i], Status_Bar_Text_Y[i], Text_Interface)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[i], Status_Action_Bar_Y[i], 1.48 * GameState.Character[i].Action_Point, 38))
            Text_Display_Center("AP: %i/100"   % (GameState.Character[i].Action_Point), Status_Action_X[i], Status_Bar_Text_Y[i], Text_Interface)


def Fight_Action_Point():
    if all(i < 100 for i in Fight.Action_Point):    
        for i in range(6):
            if GameState.Character_Death[i] == False :
                GameState.Character[i].Action_Point += GameState.Character[i].Speed/10
                Fight.Action_Point[i]   = GameState.Character[i].Action_Point

                # Max Action Point = 100
                if GameState.Character[i].Action_Point > 100:
                    GameState.Character[i].Action_Point = 100

    else:
        for i in range(6):
            if Fight.Action_Point[i] >= 100 and Fight.Turn_Phase == "":
                Fight.Turn_Phase = i



def Turn_Phase():
    # Player Phase
    if Fight.Turn_Phase <= 2:
        # Active Turn Phase
        Sprite_Rect = GameState.Character[Fight.Turn_Phase].Sprite.get_rect(topleft=(Sprite_Character_X[Fight.Turn_Phase], Sprite_Character_Y[Fight.Turn_Phase]))
        pygame.draw.rect(gameDisplay, Color_Red, Sprite_Rect, 5)

    # Enemy Phase
    else:
        # Random Target Player
        Target_Player = random.randint(0,2)

        # Attack
        Attack(Target_Player)



def Attack_Choice():
    # State - Attack Selection
    Fight.Attack = True
    
    # Checking for Enemies
    for i in range(3,6):
        if GameState.Character_Slot[i] == True and GameState.Character_Death[i] == False:
            # Getting Sprite_Rect
            Sprite_Rect = GameState.Character[i].Sprite.get_rect(topleft=(Sprite_Character_X[i], Sprite_Character_Y[i]))

            # Selection Buttons
            Button("", i, -8, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, Color_Red, Color_Green, Text_Interface, Tools.event, "", Attack)


def Attack(Selection):
    Fight.Attack = False
    # Turn Phase Character
    Character = GameState.Character[Fight.Turn_Phase]
        
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
    GameState.Character[Fight.Turn_Phase].Action_Point = 0

    Fight.Action_Point[Fight.Turn_Phase] = 0
    Fight.Turn_Phase = ""

    # Death Check
    for i in range(6):
        if GameState.Character[i].Health <= 0:
            GameState.Character_Death[i] = True
            GameState.Character[i].Action_Point = 0
            

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
        else:
            pygame.draw.rect(gameDisplay, ic, Box, abs(width))
            

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
