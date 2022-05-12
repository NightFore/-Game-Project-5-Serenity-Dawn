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


############################################################


class Setup():
    def __init__(self):
        """
        Information :
            Background  : Path to the background
            Music       : Path to the music

        State :
            Button      : Displays the buttons in the list of buttons
            Sprite      : Displays the sprites in the sprite list
            Text        : Display the texts of the text list
        
            Fight       : Enable combat status and display user interfaces
            Story       : Enables reading of the text files of the story and displays the user interfaces

            Inventory   : Displays the inventory user interface
            Result      : Displays the results user interface

        State Update    : Lists of objects displayed when the respective states are enabled
        """
        
        # Information
        self.background = False
        self.music = False

        # State
        self.button = False
        self.sprite = False
        self.text   = False
        
        self.fight  = False
        self.story  = False

        self.inventory  = False
        self.result     = False

        # State Update
        self.list_text          = []
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.



    def update_music(self, music):
        """
        Update : Load Music
        """
        if self.music != music:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)

        

    def update_init(self, background=False, music=False, button=False, sprite=False,  fight=False, text=False, story=False):
        """
        Update :
            Setup   : Load all states
            Reset   : Clean all lists and reset user interface states
            Load    : Load Background & Music
            
        """
        # Setup
        self.button = button
        self.sprite = sprite
        self.fight  = fight
        self.story  = story
        self.text   = text

        # Reset
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []
        
        self.inventory  = False
        self.status     = None
        self.result     = False
        
        # Load
        self.background = background

        self.music = music
        if music != False: 
            self.update_music(music)

            

    def update(self):
        """
        Setup :
            Update game screen and background
            Retrieves game events in global variables
            
        """
        pygame.display.update()
        if self.background != False:
            gameDisplay.blit(self.background, (0,0))
            
        Tools.events = pygame.event.get()
        for event in Tools.events:
            Tools.event = event

        self.update_state()

    def update_state(self):
        """
        User Interface :
            Inventory
            Result Screen
        """
        # Inventory
        if self.inventory == True:
            gameDisplay.blit(Interface_Inventory, (0, 0))
            
            for index in range(3):
                # Icon - Player
                if Fight.slot[0][index] == True:
                    gameDisplay.blit(Fight.character[0][index].Icon_Status, (300, 70+150*index))


        # Result
        if self.result == True:
            gameDisplay.blit(Interface_Result, (0, 0))
            
            for index in range(3):
                # Icon - Player
                if Fight.slot[0][index] == True:
                    gameDisplay.blit(Fight.character[0][index].Icon_Status, (300, 70+150*index))

                # Icon - Enemy
                if Fight.slot[1][index] == True:
                    gameDisplay.blit(Fight.character[1][index].Icon, (660, 115+95*index))
            
        


        """
        Interactive interface :
            Button & Sprite:
                Display buttons from the list and check for mouse position.
                Call function action() if clicking on it
        """
        # Button
        if self.button == True:
            # Display Button
            for index in range(len(self.list_button)):
                self.list_button[index].display(index)
            for index in range(len(self.list_button_image)):
                self.list_button_image[index].display(index)

            # Check Mouse Position & Action
            for event in Tools.events:
                for index in range(len(self.list_button)):
                    self.list_button[index].update(index)
                for index in range(len(self.list_button_image)):
                    self.list_button_image[index].update(index)


        # Sprite
        if self.sprite == True:
            # Update & Display Sprite
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
        Game State Interface :
            Fight
            Story
            Text
        """
        # Fight
        if self.fight == True:
            self.button = True
            self.text = True
            Fight.update()

         
        # Story
        if self.story == True:
            StoryIG.update()


        # Text
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()

            
    def inventory_init(self):
        """
        Inventory == False :
            Activate inventory status and pause sprite updates
            Launch the status interface with the main character
            Displays buttons to navigate between character statuses

        Inventory == True :
            Reset user interfaces
        """
        if self.inventory == False:
            self.inventory = True
            self.sprite = False
            self.update_status(0)
            
            for index in range(3):
                if Fight.slot[0][index] == True:
                    Button(Fight.character[0][index].name, "Text_Interface", 340, 180+150*index, 146, 38, 5, True, True, Color_Red, Color_Green, index, self.update_status)
                
        elif self.inventory == True:
            Menu_Zone()


    def update_status(self, status=None):
        if self.status!=status and status!=None:
            self.status = status
            self.list_text = []
            
            Text("Status",      540, 85, True, "Text_Interface")
            Text("Equipment",   760, 85, True, "Text_Interface")
            Text("Inventory",   960, 85, True, "Text_Interface")
            
            Text(("Class : %s"      % Fight.character[0][status].Class),       450, 120, False, "Text_Interface")
            Text(("Level : %i"      % Fight.character[0][status].level),       450, 150, False, "Text_Interface")
            Text(("EXP : %i/100"    % Fight.character[0][status].Experience),  450, 180, False, "Text_Interface")
            
            Text(("Health : %i"     % Fight.character[0][status].Maxhealth),   450, 220, False, "Text_Interface")
            Text(("Strength : %i"   % Fight.character[0][status].Strength),    450, 250, False, "Text_Interface")
            Text(("Magic : %i"      % Fight.character[0][status].Magic),       450, 280, False, "Text_Interface")
            Text(("Speed : %i"      % Fight.character[0][status].speed),       450, 310, False, "Text_Interface")
            Text(("Defense : %i"    % Fight.character[0][status].Defense),     450, 340, False, "Text_Interface")
            Text(("Resistance : %i" % Fight.character[0][status].Resistance),  450, 370, False, "Text_Interface")

            Text(("Accuracy : %i"   % Fight.character[0][status].Resistance),  450, 410, False, "Text_Interface")
            Text(("Evasion : %i"    % Fight.character[0][status].Resistance),  450, 440, False, "Text_Interface")
            Text(("Critical : %i"   % Fight.character[0][status].Resistance),  450, 470, False, "Text_Interface")
        
Setup = Setup()



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, center, path, dt, animation, action):
        """
        Setup       :
            Enable sprite
            Add button to list_sprite
            Animated sprite object
            
        Image      :
            Path    : Path to the images folder
            Load    : Load all images in the directory
            Images  : Images to use in the animation
            Index   : Index of the image used
            Image   : Current displayed image
        
        Position    :
            x, y, center
            
        Update       :
            dt      : Time elapsed between each frame
            Time    : Time before sprite update
            Frame   : Frame before sprite update
        
        Action      :
            Action      : Button action
        """
        # Setup
        Setup.sprite = True
        Setup.list_sprite.append(self)
        
        super(AnimatedSprite, self).__init__()
        Setup.all_sprites.append(pygame.sprite.Group(self))

        # Image
        self.path = path
        self.images = load_file(self.path, image=True)
        self.images_right = self.images
        self.image_left = [pygame.transform.flip(image, True, False) for image in self.images]
        
        self.index = 0
        self.image = self.images[self.index]
        
        # Position
        self.x = x
        self.y = y
        self.center = center

        if self.center == False:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.center == True:
            self.rect = self.image.get_rect(center=(self.x, self.y))

        # Update
        self.dt = dt
    
        self.animation_time     = animation     # self.animation_time    = 0.1
        self.current_time       = 0
    
        self.animation_frames   = animation     # self.animation_frames  = 6
        self.current_frame      = 0

        # Action
        self.action = action


    def button(self):
        """
        Calls the function Selection when clicking on the image
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
        Switch between the two update methods by commenting/uncommenting.
        """
        # self.update_time_dependent()
        self.update_frame_dependent()



class Text():
    def __init__(self, text, x, y, center, font):
        """
        Setup       : Add text to the text_list
        Text        : Text string, font, color
        Position    : Position x, y, surface, center
        """
        # Setup
        Setup.list_text.append(self)

        # Text
        self.text = text
        self.font, self.color = eval("self." + font)()

        # Position
        self.x = x
        self.y = y
        self.center = center
        self.textSurface = self.font.render(self.text, True, self.color)

        if center == False:
            self.textRect = (self.x, self.y)
            
        if center == True:
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)
            
    def Text_Title_Screen(self):
        font = pygame.font.SysFont(None, 100)
        color = Color_Title_Screen
        return font, color

    def Text_Button(self):
        font = pygame.font.SysFont(None, 40)
        color = Color_Blue
        return font, color

    def Text_Interface(self):
        font = pygame.font.SysFont(None, 35)
        color = Color_Black
        return font, color

    def display(self):
        gameDisplay.blit(self.textSurface, self.textRect)



class Button():
    def __init__(self, text, font, x, y, w, h, b, border, center, active, inactive, selection, action=None):
        """
        Setup       :
            Enable buttons
            Add button to list_button
        
        Position    :
            x, y, width, height, border width, border, center
            
        Text        :
            Add the centered text of the button to the text list
            
        Color       :
            Active/Inactive color of the button
            Color changes depending of the mouse position
        
        Action      :
            Selection   : Button index
            Action      : Button action
        """
        # Setup
        Setup.button = True
        Setup.list_button.append(self)

        # Position
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.b = b
        self.border = border
        self.center = center
        
        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)

        # Text
        Text(text, self.x+self.w/2, self.y+self.h/2, True, font)

        # Color
        self.active     = active
        self.inactive   = inactive
        self.color      = inactive

        # Action
        self.selection  = selection
        self.action     = action

        
    def update(self, index):
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
        

    def display(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, self.rect, self.b)
        pygame.draw.rect(gameDisplay, self.color, self.rect)



class Button_Image():
    def __init__(self, x, y, center, active, inactive, selection, action=None):
        """
        Setup       :
            Enable buttons
            Add button to list_button_image
        
        Position    :
            x, y, center
            
        Image       :
            Active/Inactive image of the button
            Image changes depending of the mouse position
        
        Action      :
            Selection   : Button index
            Action      : Button action
        """
        # Tools
        Setup.list_button_image.append(self)

        # Position
        self.x = x
        self.y = y
        self.center = center
        
        if self.center == False:
            self.rect = self.active.get_rect(topleft=(x,y))

        if self.center == True:
            self.rect = self.active.get_rect(center=(x,y))

        # Image
        self.active     = active.convert()
        self.inactive   = inactive.convert()
        self.image      = inactive.convert()

        # Action
        self.selection  = selection
        self.action     = action
    
        
    def update(self, index):
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

    def display(self, index):
        gameDisplay.blit(self.image, self.rect)







class Fight():
    def __init__(self):
        # State
        self.training_mode  = False
        self.state_button   = False
        self.state_attack   = False
        self.turn_index     = None
        self.turn_side      = None
        
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
            average_level         : Calculate average level of the player team
            enemy_random    : Random type of enemy
            enemy_name      : Name of the enemy
        """
        if random_enemy == True:
            # Average level of the player
            average_level = []
            for index in range(3):
                if self.slot[0][index] == True:
                    average_level.append(self.character[0][index].level)
            average_level = sum(average_level)/len(average_level)

            # Generating random enemy
            enemy_count = random.randint(1, 3)
            for index in range(enemy_count):
                enemy_random    = list_enemy[random.randint(0, len(list_enemy)-1)]
                enemy_name      = "Monster %s" % (index+1)

                self.character[1][index] = enemy_random(enemy_name, average_level)
                self.slot[1][index]      = True
                self.death[1][index]     = False

        
    def update(self):
        """
        Update : User Interface
            Setup           : Refresh information each loop
            User Interface  : Display combat status and information
        """
        # Setup
        Setup.list_text = []

        # Information
        Text("Time: %s"  % self.time,   self.time_x,    self.time_y,    True, "Text_Interface")
        Text("Stage: %s" % self.stage,  self.stage_x,   self.stage_y,   True, "Text_Interface")

        for side in range(2):
            for index in range(3):
                if self.slot[side][index] == True:
                    character = self.character[side][index]

                    # Sprite & Icon
                    if self.death[side][index] == False:
                        gameDisplay.blit(character.Sprite, (self.character_x[side][index], self.character_y[side][index]))
                    gameDisplay.blit(character.Icon, (self.icon[side], self.ui_image[index]))

                    # Character Status
                    Text("%s"           % character.name,                           self.name[side],            self.ui_text[index],    True, "Text_Interface")
                    Text("HP: %i/%i"    % (character.Health, character.Maxhealth),  self.health[side],          self.ui_text[index],    True, "Text_Interface")
                    Text("AP: %i/100"   % character.Action_Point,                   self.action_text[side]+1,   self.ui_text[index]+1,  True, "Text_Interface")

                    # Action Point
                    pygame.draw.rect(gameDisplay, Color_Green, (self.action_bar[side]+1, self.ui_image[index]+1, 1.48 * character.Action_Point, 38))

                
        """
        Update : Action Point
            Generate action points until it reaches 100
            Give a turn to the character who reaches the threshold
            Resets the button list at the end of a turn
        """
        if self.turn_index == None:
            Setup.list_button = []

            for side in range(2):
                for index in range(3):
                    # Generate Action Point
                    if self.slot[side][index] == True and self.death[side][index] == False:
                        self.character[side][index].Action_Point += self.character[side][index].speed/10

                        # Turn Phase
                        if self.character[side][index].Action_Point > 100:
                            self.character[side][index].Action_Point = 100
                            self.turn_index     = index
                            self.turn_side      = side
                            self.state_button   = True


        """
        Update : Turn Phase
            Player Phase :
                Sprite_rect : Highlight the active character
                Button      : Displays available actions

            Enemy Phase :
                target          : List of alive playable characters
                random_target   : Randomly selects a character to attack
        """
        if self.turn_index != None:
            # Player Phase
            if self.turn_side == 0:
                sprite_rect = self.character[0][self.turn_index].Sprite.get_rect(topleft=(self.character_x[0][self.turn_index], self.character_y[0][self.turn_index]))
                pygame.draw.rect(gameDisplay, Color_Red, sprite_rect, 5)

                if self.state_button == True:
                    self.state_button = False
                    Button("Attack", "Text_Button", 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, self.attack_choice)
                    Button("Guard",  "Text_Button", 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)
                    Button("Potion", "Text_Button", 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)

            # Enemy Phase
            elif self.turn_side == 1:
                target = []
                for index in range(3):
                    if self.slot[0][index] == True and self.death[0][index] == False:
                        target.append(index)

                self.attack((random.choice(target), 0))
                


    def attack_choice(self):
        """
        self.state_attack   : Attack Choice State (Prevent from clicking multiple times)
        self.slot/death     : Check Enemy Slot and Death State
        Button              : Draw a Selection Button surrounding each Enemy
        """
        if self.state_attack == False:
            self.state_attack = True
            for index in range(3):
                if self.slot[1][index] == True and self.death[1][index] == False:
                    sprite_rect = self.character[1][index].Sprite.get_rect(topleft=(self.character_x[1][index-3], self.character_y[1][index-3]))
                    Button(None, Text_Interface, sprite_rect[0]-10, sprite_rect[1]-10, sprite_rect[2]+20, sprite_rect[3]+20, 8, True, False, Color_Red, Color_Green, (index, 1), self.attack)



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

        Attack      : Calculates the attacker's damage         
            (1) [Attack * (50 / (50 + Defense^1.25))]
            (2) [Attack * (10*Attack / (10*Attack + Defense^2*Attack/100))]
            (3) [10x^3 / (10x^2 + 100y^2)   (10*x**3) / (10*x**2 + 100*y**2)
            (4) [x^3 / (x^2 + 100y^2/x)
            (5) [x^3 / (x^2 + y^2 + y^3*100/(100+x^2))]
            (6) [x^3 / (x^2 + 1.5y^2 + y^3*100/(100+2x^2))]
            
        Damage      : Damage done is between 80% and 120% of the attack
        """

        # Setup
        target_side     = target[1]
        target_index    = target[0]
        attacker = self.character[self.turn_side][self.turn_index]
        defender = self.character[target_side][target_index]
        x, y = int(attacker.Strength), int(defender.Defense)

        # Formulas
        precision   = random.randint(0, 100)
        accuracy    = 2.5*attacker.level + attacker.speed**1.2/2 + 85
        evasion     = 2.5*defender.level + defender.speed/3
        critical    = 35 - 25*(attacker.Health/attacker.Maxhealth)**(0.5 + 0.25*(attacker.level-defender.level))
        attack      = x**3 / (x**2 + 2*y**2 + y**3*100/(100+1.5*x**2))
        damage      = random.randint(int(0.8*attack), int(1.2*attack))
        
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

        # Success hit
        if (accuracy-evasion) >= precision:
            # Attack Sound
            Random_SFX = random.randint(0, len(attacker.SFX_Attack)-1)
            pygame.mixer.Sound(attacker.SFX_Attack[Random_SFX]).play()
            
            # Normal Damage
            if critical < precision:
                defender.Health = int(defender.Health-damage)

            # Critical Damage
            else:
                defender.Health = int(defender.Health-damage*2)

            # Death
            if defender.Health <= 0:
                defender.Health = 0
                defender.Action_Point = 0
                self.death[target_side][target_index] = True

                pygame.mixer.Sound(SFX_Battle_Defeated_battle02).play()

        # Miss
        else :
            pygame.mixer.Sound(SFX_Battle_Miss_battle14).play()

        self.end_turn()

    

    def end_turn(self):
        """
        Setup Reset     : Resets all variables used during a turn
        Win Condition   : Check the dead status of all enemies
        Lose Condition  : Check the dead status of all players
        """
        # Setup Reset
        self.character[self.turn_side][self.turn_index].Action_Point = 0
        self.state_attack   = False
        self.turn_index     = None
        self.turn_side      = None

        # Win Condition
        Win = True
        for index in range(3):
            if self.slot[1][index] == True and self.death[1][index] == False:
                Win = False
                
        if Win == True:
            if self.training_mode == False:
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
        """
        Setup :
            Enable results, text and button states
            Calculates experience gain and gold

        Character Status :
            Displays the name, class, level, experience of the characters

        User Interface :
            Displays stage and inventory information

        Result Gain :
            Add experience gain to characters
            Add Gold Gain to Total Gold
        """
        # Setup
        if Setup.result == False:
            Setup.result    = True
            Setup.text      = True
            Setup.button    = True
            
            exp_gain  = 0
            gold_gain = 0
            for index in range(3):
                if self.slot[1][index] == True:
                    exp_gain  += self.character[1][index].EXP_Gain
                    gold_gain += self.character[1][index].Gold_Gain

        # Character Status
            for index in range(3):
                # Player
                if self.slot[0][index] == True:
                    Text(self.character[0][index].name, 340, 180+150*index, True, "Text_Interface")
                    Text(self.character[0][index].Class, 540, 90+150*index, True, "Text_Interface")
                    Text("Level : %i" % self.character[0][index].level, 540, 135+150*index, True, "Text_Interface")
                    Text("EXP : %i + %i" % (self.character[0][index].Experience, exp_gain), 540, 180+150*index, True, "Text_Interface")

                # Enemy
                if self.slot[1][index] == True:
                    Text(self.character[1][index].name, 785, 135+95*index,  True, "Text_Interface")
                    Text("Level : %i" % self.character[1][index].level, 785, 180+95*index,  True, "Text_Interface")

        # User Interface
            Text("Stage : %s" % Fight.stage, 760, 430, True, "Text_Interface")
            Text("Result",      760, 85,  True, "Text_Interface")
            Text("Inventory",   960, 85,  True, "Text_Interface")
            Text("Gold : %i + %i" % (PlayerIG.Gold, gold_gain), 760, 480, True, "Text_Interface")
            Button("Next", "Text_Button", 960, 455, 131, 86, 4, False, True, Color_Green, Color_Red, None, Menu_Zone)


        # Result Gain
            # Experience Gain
            for index in range(3):
                if self.slot[0][index] == True:
                    self.character[0][index].Experience += exp_gain

                    while self.character[0][index].Experience >= 100:
                        self.character[0][index].update_level()
                        StoryIG.text_line[1][index] = self.character[index].name + " has Leveled Up!"
                    self.character[0][index].update_level()

            # Gold Gain
            self.character[0][0].Gold += gold_gain
                
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
    Button("Start",    "Text_Button", 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Main_Story)
    Button("Gallery",  "Text_Button", 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Main",     "Text_Button", 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Menu_Zone)

    # Text
    Text(Project_Title, display_width/2, display_height/4, True, "Text_Title_Screen")
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()


def Menu_Zone():
    # Setup
    Setup.update_init(Interface_Main_Menu, BGM_Menu_1, text=True)

    # Setup - Sprite
    AnimatedSprite(1230, 470, True, "Data\Sprite_Button\Sprite_Button_Fight",   clock.tick(FPS), 4, Main_Story)
    AnimatedSprite(615,  385, True, "Data\Sprite_Button\Sprite_Button_Traning", clock.tick(FPS), 4, Main_Training)

    # Setup - Button
    Button("Inventory", "Text_Button", 120, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Setup.inventory_init)
    Button("Status",    "Text_Button", 284, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Status)
    Button("Save",      "Text_Button", 448, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Game_Save)
    Button("Music",     "Text_Button", 1083, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Credits",   "Text_Button", 1199, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, Credits)

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
    Fight.training_mode = True

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
                Button("Music %i" % (index+1), "Text_Button", 60+200*col, 100+112*row, 160, 72, 12, True, False, Color_Green, Color_Red, List_BGM[index], Music_Play)
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
