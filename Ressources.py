import pygame
import os
pygame.init()


def load_file(path):
    """
    Load    : All texts/images in directory. The directory must only contain texts/images.
    Path    : The relative or absolute path to the directory to load texts/images from.
    Image   : Load and convert image in the direcoty path.
    Return  : List of files.
    """
    file = []
    for file_name in os.listdir(path):
            file.append(path + os.sep + file_name)
    return file

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
Background_Prologue_1       = pygame.image.load("Data\Background\Background_Altar.png")
Background_Prologue_2       = pygame.image.load("Data\Background\Background_House.png")



# UIs
Interface_Main_Menu         = pygame.image.load("Data\Interface\Interface_Main_Menu.png")
Interface_Cutscene          = pygame.image.load("Data\Interface\Interface_Cutscene.png")
Interface_Fight             = pygame.image.load("Data\Interface\Interface_Fight.png")
Interface_Inventory         = pygame.image.load("Data\Interface\Interface_Inventory.png")
Interface_Result            = pygame.image.load("Data\Interface\Interface_Result.png")



# Icons
Icon_Ellesia        = pygame.image.load("Data\Icon\Icon_Ellesia.png")
Icon_Status_Ellesia = pygame.image.load("Data\Icon\Icon_Status_Ellesia.png")
Icon_Iris           = pygame.image.load("Data\Icon\Icon_Iris.png")
Icon_Status_Iris    = pygame.image.load("Data\Icon\Icon_Status_Iris.png")
Icon_Gyrei          = pygame.image.load("Data\Icon\Icon_Gyrei.png")
Icon_Status_Gyrei   = pygame.image.load("Data\Icon\Icon_Status_Gyrei.png")

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
List_SFX = load_file("Data/SFX")

SFX_Bow, SFX_Hit, SFX_Metal, SFX_Slash, SFX_Stab = [], [], [], [], []
[SFX_Bow.append(SFX)    for SFX in List_SFX if "Bow"    in SFX]
[SFX_Hit.append(SFX)    for SFX in List_SFX if "Hit"    in SFX]
[SFX_Metal.append(SFX)  for SFX in List_SFX if "Metal"  in SFX]
[SFX_Slash.append(SFX)  for SFX in List_SFX if "Slash"  in SFX]
[SFX_Stab.append(SFX)   for SFX in List_SFX if "Stab"   in SFX]

SFX_Battle_Bow_battle16	         = pygame.mixer.Sound("Data\SFX\Battle_Bow_battle16.wav")
SFX_Battle_Bow_battle18	         = pygame.mixer.Sound("Data\SFX\Battle_Bow_battle18.wav")
SFX_Battle_Hit_battle06	         = pygame.mixer.Sound("Data\SFX\Battle_Hit_battle06.wav")
SFX_Battle_Hit_battle12	         = pygame.mixer.Sound("Data\SFX\Battle_Hit_battle12.wav")
SFX_Battle_Metal_battle05	 = pygame.mixer.Sound("Data\SFX\Battle_Metal_battle05.wav")
SFX_Battle_Metal_battle10	 = pygame.mixer.Sound("Data\SFX\Battle_Metal_battle10.wav")
SFX_Battle_Slash_battle17	 = pygame.mixer.Sound("Data\SFX\Battle_Slash_battle17.wav")
SFX_Battle_Stab_battle01	 = pygame.mixer.Sound("Data\SFX\Battle_Stab_battle01.wav")
SFX_Battle_Stab_battle03	 = pygame.mixer.Sound("Data\SFX\Battle_Stab_battle03.wav")

SFX_Battle_Debuff_system04       = pygame.mixer.Sound("Data\SFX\Battle_Debuff_system04.wav")
SFX_Battle_Debuff_system09	 = pygame.mixer.Sound("Data\SFX\Battle_Debuff_system09.wav")
SFX_Battle_Fire_element_fire01	 = pygame.mixer.Sound("Data\SFX\Battle_Fire_element_fire01.wav")
SFX_Battle_Fire_explosion06	 = pygame.mixer.Sound("Data\SFX\Battle_Fire_explosion06.wav")
SFX_Battle_Heal_magical25	 = pygame.mixer.Sound("Data\SFX\Battle_Heal_magical25.wav")
SFX_Battle_Water_element_water06 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water06.wav")
SFX_Battle_Water_element_water08 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water08.wav")
SFX_Battle_Water_element_water14 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water14.wav")
SFX_Battle_Wind_magical16	 = pygame.mixer.Sound("Data\SFX\Battle_Wind_magical16.wav")

SFX_Battle_Defeated_battle02	 = pygame.mixer.Sound("Data\SFX\Battle_Defeated_battle02.wav")
SFX_Battle_Escape_battle19	 = pygame.mixer.Sound("Data\SFX\Battle_Escape_battle19.wav")
SFX_Battle_Miss_battle14	 = pygame.mixer.Sound("Data\SFX\Battle_Miss_battle14.wav")

SFX_Event_Bell_chime07	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime07.wav")
SFX_Event_Bell_chime08	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime08.wav")
SFX_Event_Bell_chime09	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime09.wav")
SFX_Event_Creepy_effect07	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect07.wav")
SFX_Event_Creepy_effect12	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect12.wav")
SFX_Event_Creepy_effect13	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect13.wav")
SFX_Event_Creepy_magical13	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_magical13.wav")
SFX_Event_Creepy_magical14	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_magical14.wav")
SFX_Event_Future_effect04	 = pygame.mixer.Sound("Data\SFX\Event_Future_effect04.wav")
SFX_Event_se_door01	         = pygame.mixer.Sound("Data\SFX\Event_se_door01.wav")
SFX_Event_se_door05	         = pygame.mixer.Sound("Data\SFX\Event_se_door05.wav")
SFX_Event_se_footstep01	         = pygame.mixer.Sound("Data\SFX\Event_se_footstep01.wav")
SFX_Event_se_footstep02	         = pygame.mixer.Sound("Data\SFX\Event_se_footstep02.wav")
SFX_Event_se_stairs	         = pygame.mixer.Sound("Data\SFX\Event_se_stairs.wav")
SFX_Event_Summon_magical10	 = pygame.mixer.Sound("Data\SFX\Event_Summon_magical10.wav")
SFX_Map_element_fire12	         = pygame.mixer.Sound("Data\SFX\Map_element_fire12.wav")
SFX_Map_element_thunder01	 = pygame.mixer.Sound("Data\SFX\Map_element_thunder01.wav")
SFX_Map_element_wind03	         = pygame.mixer.Sound("Data\SFX\Map_element_wind03.wav")
SFX_Map_se_car02	         = pygame.mixer.Sound("Data\SFX\Map_se_car02.wav")
SFX_Map_se_car04	         = pygame.mixer.Sound("Data\SFX\Map_se_car04.wav")
SFX_Map_se_car07	         = pygame.mixer.Sound("Data\SFX\Map_se_car07.wav")
SFX_Map_se_vehicle02	         = pygame.mixer.Sound("Data\SFX\Map_se_vehicle02.wav")
SFX_System_Cancel_system10	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system10.wav")
SFX_System_Cancel_system42	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system42.wav")
SFX_System_Cancel_system43	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system43.wav")
SFX_System_Complete_jingle05	 = pygame.mixer.Sound("Data\SFX\System_Complete_jingle05.wav")
SFX_System_Confirm_system23	 = pygame.mixer.Sound("Data\SFX\System_Confirm_system23.wav")
SFX_System_Confirm_system46	 = pygame.mixer.Sound("Data\SFX\System_Confirm_system46.wav")
SFX_System_Error_onepoint14	 = pygame.mixer.Sound("Data\SFX\System_Error_onepoint14.wav")
SFX_System_Game_Over_jingle01	 = pygame.mixer.Sound("Data\SFX\System_Game_Over_jingle01.wav")
SFX_System_Hint_onepoint09	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint09.wav")
SFX_System_Hint_onepoint12	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint12.wav")
SFX_System_Hint_onepoint16	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint16.wav")
SFX_System_Navigation_system48	 = pygame.mixer.Sound("Data\SFX\System_Navigation_system48.wav")
SFX_System_Navigationse_sound15	 = pygame.mixer.Sound("Data\SFX\System_Navigationse_sound15.wav")
SFX_System_Story_End_jingle02	 = pygame.mixer.Sound("Data\SFX\System_Story_End_jingle02.wav")
SFX_System_Tutorial_onepoint10	 = pygame.mixer.Sound("Data\SFX\System_Tutorial_onepoint10.wav")
SFX_Voice_element_darkness01	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness01.wav")
SFX_Voice_element_darkness02	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness02.wav")
SFX_Voice_element_darkness03	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness03.wav")
SFX_Voice_element_darkness04	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness04.wav")
SFX_Voice_voice_human01          = pygame.mixer.Sound("Data\SFX\Voice_voice_human01.wav")
SFX_Voice_voice_monster01	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster01.wav")
SFX_Voice_voice_monster02	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster02.wav")
SFX_Voice_voice_monster03	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster03.wav")
SFX_Voice_voice_tiger01	         = pygame.mixer.Sound("Data\SFX\Voice_voice_tiger01.wav")


# BGM
List_BGM = load_file("Data/BGM")

BGM_Event_0_1_1 = "Data/BGM/Event_0_1_1_Serenity.mp3"
BGM_Event_0_1_2 = "Data/BGM/Event_0_1_2_Around_a_Campfire.mp3"
BGM_Event_1_1   = "Data/BGM/Event_1_1_Exploring_the_Danger.mp3"
BGM_Event_1_2_1 = "Data/BGM/Event_1_2_1_Time_of_Crisis.mp3"
BGM_Event_1_2_2 = "Data/BGM/Event_1_2_2_Time_of_Crisis_Piano.mp3"
BGM_Event_1_3   = "Data/BGM/Event_1_3_Danger_to_our_Lives.mp3"
BGM_Event_1_4   = "Data/BGM/Event_1_4_Behind_the_Curtains.mp3"
BGM_Event_1_5   = "Data/BGM/Event_1_5_Departure.mp3"

BGM_Fight_0_1   = "Data/BGM/Fight_0_1_Fierce_Assault.mp3"
BGM_Fight_1_1   = "Data/BGM/Fight_1_1_Ruler_of_the_Hills.mp3"
BGM_Fight_1_2   = "Data/BGM/Fight_1_2_Desperate_Situation.mp3"
BGM_Fight_1_3   = "Data/BGM/Fight_1_3_Facing_the_Danger.mp3"
BGM_Fight_1_4   = "Data/BGM/Fight_1_4_Intimidating_Foe.mp3"

BGM_Menu_1      = "Data/BGM/Menu_1_The_Soul_of_the_Adventurer.mp3"
BGM_Menu_2      = "Data/BGM/Menu_2_Calm_Before_the_Storm.mp3"
BGM_Shop        = "Data/BGM/Shop_Shopping_in_Town.mp3"
BGM_Title_Screen = "Data/BGM/Title_Screen_Undisturbed_Place.mp3"
BGM_Victory_1   = "Data/BGM/Victory_1_Resting_Around_the_Campfire.mp3"
BGM_Victory_2   = "Data/BGM/Victory_2_Glory_Ride.mp3"
