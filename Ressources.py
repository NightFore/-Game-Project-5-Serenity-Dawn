import pygame
pygame.init()

# Colors
Color_Red           = 255, 20,  0
Color_Green         = 60,  210, 120
Color_Blue          = 0,   160, 230
Color_Black         = 0,   0,   0
Color_Grey          = 150, 170, 210
Color_White         = 255, 255, 255

Color_Button        = 140, 205, 245
Color_Title_Screen  = 210, 100, 240
    
# Backgrounds
Background_Title_Screen_1   = pygame.image.load("Data\Background\Background_Title_Screen_1.png")
Background_Title_Screen_2   = pygame.image.load("Data\Background\Background_Title_Screen_2.png")
Background_Prologue         = pygame.image.load("Data\Background\Background_Altar.png")
Background_Cutscene_1       = pygame.image.load("Data\Background\Background_House.png")



# UIs
Interface_Main_Menu         = pygame.image.load("Data\Interface\Interface_Main_Menu.png")
Interface_Cutscene          = pygame.image.load("Data\Interface\Interface_Cutscene.png")
Interface_Fight             = pygame.image.load("Data\Interface\Interface_Fight.png")
Interface_Inventory         = pygame.image.load("Data\Interface\Interface_Inventory.png")



# Icons
Icon_Ellesia        = pygame.image.load("Data\Icon\Icon_Ellesia.png")
Icon_Ellesia_Status = pygame.image.load("Data\Icon\Icon_Ellesia_Status.png")
Icon_Iris           = pygame.image.load("Data\Icon\Icon_Iris.png")
Icon_Iris_Status    = pygame.image.load("Data\Icon\Icon_Iris_Status.png")
Icon_Gyrei          = pygame.image.load("Data\Icon\Icon_Gyrei.png")
Icon_Gyrei_Status   = pygame.image.load("Data\Icon\Icon_Gyrei_Status.png")

Icon_Direwolf       = pygame.image.load("Data\Icon\Icon_Direwolf.png")
Icon_Ghoul          = pygame.image.load("Data\Icon\Icon_Ghoul.png")
Icon_Shadow_Red     = pygame.image.load("Data\Icon\Icon_Shadow_Red.png")
Icon_Shadow_Blue    = pygame.image.load("Data\Icon\Icon_Shadow_Blue.png")
Icon_Wolf           = pygame.image.load("Data\Icon\Icon_Wolf.png")
Icon_Zombie         = pygame.image.load("Data\Icon\Icon_Zombie.png")

Icon_World_Map_ac   = pygame.image.load("Data\Icon\Icon_World_Map_ac.png")
Icon_World_Map_ic   = pygame.image.load("Data\Icon\Icon_World_Map_ic.png")
Icon_Exit           = pygame.image.load("Data\Icon\Icon_Exit.png")

Icon_Arrow_A = pygame.image.load("Data\Icon\Icon_Arrow_A.png")
Icon_Arrow_B = pygame.image.load("Data\Icon\Icon_Arrow_B.png")
Arrow_A_Rect = Icon_Arrow_A.get_rect()
Arrow_B_Rect = Icon_Arrow_B.get_rect()



# Sprites
Sprite_Ellesia      = pygame.image.load("Data\Sprite\Sprite_Ellesia.png")
Sprite_Iris         = pygame.image.load("Data\Sprite\Sprite_Iris.png")
Sprite_Gyrei        = pygame.image.load("Data\Sprite\Sprite_Gyrei.png")

Sprite_Direwolf     = pygame.image.load("Data\Sprite\Sprite_Direwolf.png")
Sprite_Ghoul        = pygame.image.load("Data\Sprite\Sprite_Ghoul.png")
Sprite_Shadow_Red   = pygame.image.load("Data\Sprite\Sprite_Shadow_Red.png")
Sprite_Shadow_Blue  = pygame.image.load("Data\Sprite\Sprite_Shadow_Blue.png")
Sprite_Zombie       = pygame.image.load("Data\Sprite\Sprite_Zombie.png")
Sprite_Wolf         = pygame.image.load("Data\Sprite\Sprite_Wolf.png")



# Sound Effects
SFX_Wolf_Growl  = pygame.mixer.Sound("Data\SFX\SFX_Wolf_Growl.wav")

SFX_Hit_1       = pygame.mixer.Sound("Data\SFX\SFX_Hit_1.wav")
SFX_Hit_2       = pygame.mixer.Sound("Data\SFX\SFX_Hit_2.wav")
SFX_Slash       = pygame.mixer.Sound("Data\SFX\SFX_Slash.wav")
SFX_Miss        = pygame.mixer.Sound("Data\SFX\SFX_Miss.wav")
SFX_Defeated    = pygame.mixer.Sound("Data\SFX\SFX_Defeated.wav")



# OSTs
OST_Title_Screen    = "Data/OST/Title_Screen_Undisturbed_Place.mp3"

OST_Cutscene_1_1    = "Data/OST/Serenity.mp3"
OST_Cutscene_1_2    = "Data/OST/Around_a_Campfire.mp3"
OST_Cutscene_1_3    = "Data/OST/Departure.mp3"

OST_Cutscene_2_1    = "Data/OST/Behind_the_Curtains.mp3"
OST_Cutscene_2_2    = "Data/OST/Danger_to_our_Lives.mp3"
OST_Cutscene_2_3    = "Data/OST/Welcome_Back_Party.mp3"

OST_Fight_1_1       = "Data/OST/Fierce_Assault.mp3"
OST_Fight_1_2       = "Data/OST/Striking_Back.mp3"
OST_Fight_1_3       = "Data/OST/Facing_a_Wall.mp3"
OST_Fight_1_4       = "Data/OST/Intimidating_Foe.mp3"

OST_Fight_2_1       = "Data/OST/Desperate_Situation.mp3"
OST_Fight_2_2       = "Data/OST/The_Hunt_is_On.mp3"
OST_Fight_2_3       = "Data/OST/Blazing_Power.mp3"
OST_Fight_2_4       = "Data/OST/Taking_Down_the_Mastermind.mp3"
OST_Fight_2_5       = "Data/OST/Ruler_of_the_Hills.mp3"
OST_Fight_2_6       = "Data/OST/Tense_Fight.mp3"

OST_Menu_Main_1_1   = "Data/OST/The_Soul_of_the_Adventurer.mp3"
OST_Menu_Main_2_1   = "Data/OST/Time_of_Crisis.mp3"
OST_Menu_Main_2_2   = "Data/OST/Calm_Before_the_Storm.mp3"

OST_Menu_Shop       = "Data/OST/Shopping_in_Town.mp3"
OST_Menu_Victory_1  = "Data/OST/Resting_Around_the_Campfire.mp3"
OST_Menu_Victory_2  = "Data/OST/Glory_Ride.mp3"


List_OST = [OST_Title_Screen,
            OST_Cutscene_1_1, OST_Cutscene_1_2, OST_Cutscene_1_3,
            OST_Cutscene_2_1, OST_Cutscene_2_2, OST_Cutscene_2_3,
            OST_Fight_1_1, OST_Fight_1_2, OST_Fight_1_3, OST_Fight_1_4,
            OST_Fight_2_1, OST_Fight_2_2, OST_Fight_2_3, OST_Fight_2_4, OST_Fight_2_5, OST_Fight_2_6,
            OST_Menu_Main_1_1, OST_Menu_Main_2_1, OST_Menu_Main_2_2,
            OST_Menu_Shop, OST_Menu_Victory_1, OST_Menu_Victory_2]



# Story
List_Story = []
List_Story.append("Data/Story/1_1_1_Story_Prologue.txt")
List_Story.append("Data/Story/1_1_2_Story_Prologue.txt")
List_Story.append("Data/Story/1_2_1_Story_Prologue.txt")
List_Story.append("Data/Story/1_2_2_Story_Prologue.txt")
