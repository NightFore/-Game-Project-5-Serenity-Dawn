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
    def __init__(self, name):
        self.event              = ""        # Button
        self.events             = ""        # Text

        self.Background         = ""

        # Text
        self.Story_Order        = 0                                 # Story Progress
        self.Text_File          = open(List_Story[0], "r")          # Read File

        self.Text               = ""        # Text in File

        self.Text_Character_Left    = ""                            # Character Name
        self.Text_Line_Left         = ["","","","","","","","",""]  # Text
        self.Text_Order_Left        = 1                             # Line

        self.Text_Character_Right   = ""                            # Character Name
        self.Text_Line_Right        = ["","","","","","","","",""]  # Text
        self.Text_Order_Right       = 1                             # Line

        self.Event              = False     # Continue/Stop Reading
        self.Input_State        = False     # Writing
        self.textinput          = pygame_textinput.TextInput()
        self.Text_Line_Input    = ""

        # Animated Sprite
        self.Sprite_Number  = 0
        self.Sprite_Index   = 0
        
        self.Sprite_x = []
        self.Sprite_y = []
        self.Sprite_center = []
        self.Sprite_action = []
        
        self.Sprite_images = []         # Make sure to provide the relative or full path to the images directory.
        self.Sprite_player = []
        self.Sprite_all_sprites = []    # Creates a sprite group and adds 'player' to it.
        
        self.Sprite_dt = []             # Amount of seconds between each loop.
        self.Sprite_animation = []      # Amount of time/frame before update

Tools = Tools("Tools")

class GameState():
    def __init__(self, name):
        # Interface Fight
        self.Character          = [PlayerIG]
        self.Character_Slot     = []
        self.Character_Death    = []

        # State
        self.Attack_Choice  = False
        self.Turn_Count     = 1
        self.Stage_Progress = 1
        
        # Fight Status
        self.Turn       = [False,False,False,False,False,False]
        self.Turn_Order = 0
        
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
        self.Turn_Phase     = ""
GameState = GameState("GameState")


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, animation, center):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        self.images = Tools.Sprite_images[Tools.Sprite_index]                                   # Load all images
        self.images_right = self.images                                                         # Normal image
        self.images_left = [pygame.transform.flip(image, True, False) for image in self.images] # Flipping every image.
        
        self.index = 0                                                                          # First image
        self.image = self.images[self.index]                                                    # Current image of the animation.

        self.image_rect = self.image.get_rect()                                                 # Surface of the images
        size = (self.image_rect[2], self.image_rect[3])                                         # This should match the size of the images.

        if center == False:
            self.rect = pygame.Rect((Tools.Sprite_x[Tools.Sprite_index], Tools.Sprite_y[Tools.Sprite_index]), size)
        
        if center == True:
            self.rect = pygame.Rect((Tools.Sprite_x[Tools.Sprite_index]-self.image_rect[2]/2, Tools.Sprite_y[Tools.Sprite_index]-self.image_rect[3]/2), size)

        #self.animation_time = 0.1
        self.animation_time = animation
        self.current_time = 0

        #self.animation_frames = 6
        self.animation_frames = animation
        self.current_frame = 0

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
        
    def button_image(x, y, event, action=None):
        """
        Calls the function Selection when clicking oh the image
        """
        mouse = pygame.mouse.get_pos()  
        button = Tools.Sprite_player[Tools.Sprite_index].image.convert()
        button_rect = button.get_rect(topleft=(x,y))

        if Tools.Sprite_player[Tools.Sprite_index].rect.collidepoint(mouse):
            gameDisplay.blit(Tools.Sprite_player[Tools.Sprite_index].image, Tools.Sprite_player[Tools.Sprite_index].rect)
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



def Quit_Game():
    pygame.quit()
    quit()




    
# Game - Main Function
def Title_Screen():
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

            Text_Display_Center(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            Button("Start"      , "", 15, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Prologue)
            Button("Gallery"    , "", 15, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, OST_Gallery)
            Button("Debug"      , "", 15, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Debug)
            
            pygame.display.update()
        


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
    Tools.Sprite_Number = 2                             # Number of Sprite
    Tools.Sprite_x = [615, display_width/3]             # Position x
    Tools.Sprite_y = [435, display_height/3]            # Position y
    Tools.Sprite_images = [AnimatedSprite.load_images(path="Data\Sprite_Button\Sprite_Button_Traning"), AnimatedSprite.load_images(path="Data\Sprite_Button\Sprite_Button_Fight")]
    Tools.Sprite_center = [True, True]                  # Center Sprite
    Tools.Sprite_action = [Action_Test, Action_Test]    # Function

    for Tools.Sprite_index in range(Tools.Sprite_Number):
        Tools.Sprite_animation.append(4)                        # Frame before update
        Tools.Sprite_dt.append(clock.tick(FPS))
        Tools.Sprite_player.append(AnimatedSprite(animation=Tools.Sprite_animation[Tools.Sprite_index], center=Tools.Sprite_center[Tools.Sprite_index]))
        Tools.Sprite_all_sprites.append(pygame.sprite.Group(Tools.Sprite_player[Tools.Sprite_index]))
    
    # Loop
    gameExit = False
    while not gameExit:
        # Setup
        pygame.display.update()
        Tools.events = pygame.event.get()
        gameDisplay.blit(Tools.Background, (0,0))
                    
        for Tools.Sprite_index in range(Tools.Sprite_Number):
            Tools.Sprite_dt[Tools.Sprite_index] = clock.tick(FPS)   # No effects (using frames)
            Tools.Sprite_all_sprites[Tools.Sprite_index].update(Tools.Sprite_dt[Tools.Sprite_index])
            Tools.Sprite_all_sprites[Tools.Sprite_index].draw(gameDisplay)
        
        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
                
            for Tools.Sprite_index in range(Tools.Sprite_Number):
                if callable(Tools.Sprite_action[Tools.Sprite_Index]) == True:   # Check Function
                    AnimatedSprite.button_image(Tools.Sprite_x[Tools.Sprite_Index], Tools.Sprite_y[Tools.Sprite_Index], Tools.event, Tools.Sprite_action[Tools.Sprite_Index])



def Training():
    # Setup
    Tools.Background = Background_Title_Screen_2
    pygame.mixer.music.load(List_OST[6])
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

            Text_Display_Center(Project_Title, display_width/2, display_height/4, Text_Title_Screen)
            Button("Music"      , "", 15, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, OST_Gallery)
            Button("Fight"      , "", 15, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Debug_Fight)
            Button("Training"   , "", 15, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, Color_Green, Color_Red, Text_Button_1, Tools.event, True, Training)
    
            pygame.display.update()
            

def Action_Test():
    print("Click!")

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
        if GameState.Turn_Phase != "":
            Turn_Phase()
            
        # State - Attack Selection
        if GameState.Attack_Choice == True:
            Attack_Choice()

        # Event
        for event in Tools.events:
            Tools.event = event
            if event.type == pygame.QUIT:
                Quit_Game()
            


def Game_ui_Fight():
    # Information
    Text_Display_Center("Turn: %s"     % GameState.Turn_Count      , Turn_Count_X  , Turn_Count_Y  , Text_Interface)
    Text_Display_Center("Stage: %s"    % GameState.Stage_Progress  , Stage_X       , Stage_Y       , Text_Interface)
    
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
            Text_Display_Center("%s"           % GameState.Character[i].name, Status_Name_X[i], Status_Bar_Text_Y[i], Text_Interface)
            Text_Display_Center("HP: %i/%i"    % (GameState.Character[i].Health, GameState.Character[i].Maxhealth), Status_Health_X[i], Status_Bar_Text_Y[i], Text_Interface)

            # Action Bar
            pygame.draw.rect(gameDisplay, Color_Green, (Status_Action_Bar_X[i], Status_Action_Bar_Y[i], 1.48 * GameState.Character[i].Action_Point, 38))
            Text_Display_Center("AP: %i/100"   % (GameState.Character[i].Action_Point), Status_Action_X[i], Status_Bar_Text_Y[i], Text_Interface)


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
            Button("", i, -8, Sprite_Rect[0]-10, Sprite_Rect[1]-10, Sprite_Rect[2]+20, Sprite_Rect[3]+20, Color_Red, Color_Green, Text_Interface, Tools.event, "", Attack)


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
    if Tools.textinput.update(Tools.events):
        # Text Input
        Tools.Text_Line_Input   = Tools.textinput.get_text()
        Tools.textinput         = pygame_textinput.TextInput()


        # Input Name Event
        if Tools.Text_Line_Input != "":
            Tools.Input_State = False
            Tools.Event = False
            
            PlayerIG.name = Tools.Text_Line_Input
            Tools.Text_Line_Input = ""
            Tools.Text = "(NEXT)"


        # Next File
        if "(NEXT)" in Tools.Text:
            Tools.Text_File.close()
            Tools.Story_Order += 1
            Tools.Text_File = open(List_Story[Tools.Story_Order], "r")
            Tools.Text = ""

        # Event == Stop Reading
        if Tools.Event == False:
            
            # Read File
            Tools.Text = Tools.Text_File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

            # Event State
            if "(EVENT)" in Tools.Text:
                Tools.Event = True

            # Input State
            if "(INPUT)" in Tools.Text:
                Tools.Text = Tools.Text.strip("(INPUT)")
                Tools.Text_Line_Input = ""
                Tools.Input_State = True



            # Reset Text
            if Tools.Text_Order_Left == 7:
                Tools.Text_Line_Left = ["","","","","","","","",""]
                Tools.Text_Order_Left = 1

            if Tools.Text_Order_Right == 7:
                Tools.Text_Line_Right = ["","","","","","","","",""]
                Tools.Text_Order_Right = 1


        # Text
            # Left Side
            if "[L]" in Tools.Text:
                # Character Name
                if "(NAME)" in Tools.Text:
                    Tools.Text_Character_Left = Tools.Text.replace("(NAME)[L]", "")
                    Tools.Text = Tools.Text_File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

                # Text
                Tools.Text_Line_Left[Tools.Text_Order_Left]     = Tools.Text.replace("[L]", "")
                Tools.Text_Line_Left[Tools.Text_Order_Left+1]   = "(-> Press Enter)"
                Tools.Text_Line_Right[Tools.Text_Order_Right+1] = ""
                Tools.Text_Order_Left += 1

            # Right Side
            elif "[R]" in Tools.Text:
                # Character Name
                if "(NAME)" in Tools.Text:
                    Tools.Text_Character_Right = Tools.Text.replace("(NAME)[R]", "")
                    Tools.Text = Tools.Text_File.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % GameState.Character[0].name))

                # Text
                Tools.Text_Line_Right[Tools.Text_Order_Right]   = Tools.Text.replace("[R]", "")
                Tools.Text_Line_Right[Tools.Text_Order_Right+1] = "(-> Press Enter)"
                Tools.Text_Line_Left[Tools.Text_Order_Left+1]   = ""
                Tools.Text_Order_Right += 1


def Story_Text_Display():
    # Background
    gameDisplay.blit(Interface_Cutscene, (0,0))

    # Character Name
    Text_Display_Center(Tools.Text_Character_Left   , 100, 535, Text_Interface)
    Text_Display_Center(Tools.Text_Character_Right  , 1180, 535, Text_Interface) 

    # Text Left
    Text_Display(Tools.Text_Line_Left[1], 5, 565, Text_Interface)
    Text_Display(Tools.Text_Line_Left[2], 5, 585, Text_Interface)
    Text_Display(Tools.Text_Line_Left[3], 5, 605, Text_Interface)
    Text_Display(Tools.Text_Line_Left[4], 5, 625, Text_Interface)
    Text_Display(Tools.Text_Line_Left[5], 5, 645, Text_Interface)
    Text_Display(Tools.Text_Line_Left[6], 5, 665, Text_Interface)
    Text_Display(Tools.Text_Line_Left[7], 5, 685, Text_Interface)

    # Text Right
    Text_Display(Tools.Text_Line_Right[1], 725, 565, Text_Interface)
    Text_Display(Tools.Text_Line_Right[2], 725, 585, Text_Interface)
    Text_Display(Tools.Text_Line_Right[3], 725, 605, Text_Interface)
    Text_Display(Tools.Text_Line_Right[4], 725, 625, Text_Interface)
    Text_Display(Tools.Text_Line_Right[5], 725, 645, Text_Interface)
    Text_Display(Tools.Text_Line_Right[6], 725, 665, Text_Interface)
    Text_Display(Tools.Text_Line_Right[7], 725, 685, Text_Interface)

    # Write Text
    if Tools.Input_State == True:
        #Text_Display_Center(Tools.textinput.get_text(), 720, 600, Text_Interface)

        # Text Box
        pygame.draw.rect(gameDisplay, Color_Grey, [540, 340, 200, 40])
        pygame.draw.rect(gameDisplay, Color_Black, [540, 340, 200, 40], 5)

        # Text Center
        Text    = Tools.textinput.get_surface()
        Width   = Text.get_width()
        Height  = Text.get_height()
        gameDisplay.blit(Tools.textinput.get_surface(), (640-Width//2, 360-Height//2))


Title_Screen()
