import random

from Ressources import *


        # Player
class Player:
    def __init__(self, name, level=5):
        self.name           = name
        self.Icon           = Icon_Ellesia
        self.Icon_Status    = Icon_Status_Ellesia
        self.Sprite         = Sprite_Ellesia
        self.SFX_Attack     = SFX_Stab

        self.Class          = "Lancer"
        self.level          = level
        self.Experience     = 0
        self.Gold           = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
        
        self.Maxhealth      = 45    + (7.90 + 0.525 * (self.level-1)) * (self.level-1)
        self.Strength       = 8     + (1.25 + 0.225 * (self.level-1)) * (self.level-1)
        self.speed          = 10    + (0.70 + 0.100 * (self.level-1)) * (self.level-1)
        self.Defense        = 4     + (0.75 + 0.190 * (self.level-1)) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
        

PlayerIG = Player("NightFore")



class Iris:
    def __init__(self, name, level=5):
        self.name           = name
        self.Icon           = Icon_Iris
        self.Icon_Status    = Icon_Status_Iris
        self.Sprite         = Sprite_Iris
        self.SFX_Attack     = SFX_Bow
        
        self.Class          = "Archer"
        self.level          = level
        self.Experience     = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
        
        self.Maxhealth      = 30    + (6.80 + 0.490 * (self.level-1)) * (self.level-1)
        self.Strength       = 9     + (0.95 + 0.240 * (self.level-1)) * (self.level-1)
        self.speed          = 8     + (0.60 + 0.080 * (self.level-1)) * (self.level-1)
        self.Defense        = 1     + (0.85 + 0.165 * (self.level-1)) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
IrisIG = Iris("Iris")



class Gyrei:
    def __init__(self, name, level=5):
        self.name           = name
        self.Icon           = Icon_Gyrei
        self.Icon_Status    = Icon_Status_Gyrei
        self.Sprite         = Sprite_Gyrei
        self.SFX_Attack     = SFX_Slash

        self.Class          = "Sword"
        self.level          = level
        self.Experience     = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
            
        self.Maxhealth      = 40    + (8.00 + 0.500 * (self.level-1)) * (self.level-1)
        self.Strength       = 7     + (1.05 + 0.210 * (self.level-1)) * (self.level-1)
        self.speed          = 12    + (0.80 + 0.110 * (self.level-1)) * (self.level-1)
        self.Defense        = 2     + (0.80 + 0.175 * (self.level-1)) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
GyreiIG = Gyrei("Gyrei")





        # Enemy
class Wolf:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Wolf
        self.Sprite         = Sprite_Wolf
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 40    + (4.20 + 0.200 * (self.level-1)) * (self.level-1)
        self.Strength       = 6     + (1.55 + 0.060 * (self.level-1)) * (self.level-1)
        self.speed          = 10    + (1.35 + 0.040 * (self.level-1)) * (self.level-1)
        self.Defense        = 2     + (0.80 + 0.055 * (self.level-1)) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
WolfIG = Wolf("Wolf")


class Direwolf:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Direwolf
        self.Sprite         = Sprite_Direwolf
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 55    + (5.35 + 0.225 * (self.level-1)) * (self.level-1)
        self.Strength       = 8     + (2.00 + 0.075 * (self.level-1)) * (self.level-1)
        self.speed          = 8     + (1.65 + 0.035 * (self.level-1)) * (self.level-1)
        self.Defense        = 3     + (0.95 + 0.075 * (self.level-1)) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
DirewolfIG = Direwolf("Direwolf")


class Shadow_Red:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Shadow_Red
        self.Sprite         = Sprite_Shadow_Red
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 70    + (6.50 + 0.290 * (self.level-1)) * (self.level-1)
        self.Strength       = 10    + (1.40 + 0.150 * (self.level-1)) * (self.level-1)
        self.speed          = 7     + (1.05 + 0.025 * (self.level-1)) * (self.level-1)
        self.Defense        = 5     + (0.85 + 0.100 * (self.level-1)) * (self.level-1)
        print(self.Strength)
        print(self.Defense)

        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
Shadow_RedIG = Shadow_Red("Shadow_Red")


class Zombie:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Zombie
        self.Sprite         = Sprite_Zombie
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10

        self.Maxhealth      = 72    + 6 * (self.level-1)
        self.Strength       = 14    + 1 * (self.level-1)
        self.speed          = 5     + 1 * (self.level-1)
        self.Defense        = 1     + 1 * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
ZombieIG = Zombie("Zombie")


class Ghoul:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Ghoul
        self.Sprite         = Sprite_Ghoul
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10

        self.Maxhealth      = 38    + 6 * (self.level-1)
        self.Strength       = 4     + 1 * (self.level-1)
        self.speed          = 9     + 1 * (self.level-1)
        self.Defense        = 1     + 1 * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
GhoulIG = Ghoul("Ghoul")


class Shadow_Blue:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Shadow_Blue
        self.Sprite         = Sprite_Shadow_Blue
        self.SFX_Attack     = SFX_Hit
    
        self.level          = level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10

        self.Maxhealth      = 150   + 6 * (self.level-1)
        self.Strength       = 20    + 1 * (self.level-1)
        self.speed          = 13    + 1 * (self.level-1)
        self.Defense        = 1     + 1 * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
Shadow_BlueIG = Shadow_Blue("Shadow_Blue")


list_enemy = [Wolf, Direwolf, Shadow_Red]#, Ghoul, Zombie, Shadow_Blue]
