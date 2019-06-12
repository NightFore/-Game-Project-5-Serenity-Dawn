import random

from Ressources import *


        # Player
class Player:
    def __init__(self, name, level=10):
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
        
        self.Maxhealth      = 40    + (6.00 + 0.525 * self.level) * (self.level-1)
        self.Strength       = 8     + (1.10 + 0.150 * self.level) * (self.level-1)
        self.speed          = 10    + (0.85 + 0.035 * self.level) * (self.level-1)
        self.Defense        = 4     + (0.80 + 0.115 * self.level) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
        

PlayerIG = Player("NightFore")



class Iris:
    def __init__(self, name, level=10):
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
        
        self.Maxhealth      = 26    + (7.00 + 0.325 * self.level) * (self.level-1)
        self.Strength       = 9     + (1.25 + 0.180 * self.level) * (self.level-1)
        self.speed          = 8     + (1.00 + 0.025 * self.level) * (self.level-1)
        self.Defense        = 2     + (1.20 + 0.075 * self.level) * (self.level-1)
        
        self.Magic          = 0
        self.Resistance     = 0

        self.Health         = self.Maxhealth
        self.Action_Point   = 0
IrisIG = Iris("Iris")



class Gyrei:
    def __init__(self, name, level=10):
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
        
        self.Maxhealth      = 25    + (8.00 + 0.375 * self.level) * (self.level-1)
        self.Strength       = 6     + (0.90 + 0.145 * self.level) * (self.level-1)
        self.speed          = 12    + (1.10 + 0.050 * self.level) * (self.level-1)
        self.Defense        = 2     + (0.70 + 0.105 * self.level) * (self.level-1)
        
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

        self.base_level     = 0
        self.level          = self.base_level + level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 40    + (3.75 + 0.210 * self.level) * (self.level-1)
        self.Strength       = 6     + (0.85 + 0.110 * self.level) * (self.level-1)
        self.speed          = 12    + (0.95 + 0.040 * self.level) * (self.level-1)
        self.Defense        = 2     + (0.95 + 0.055 * self.level) * (self.level-1)
        
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

        self.base_level     = 2
        self.level          = self.base_level + level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 70    + 6 * (self.level-1)
        self.Strength       = 4     + 1 * (self.level-1)
        self.speed          = 12    + 1 * (self.level-1)
        self.Defense        = 1     + 1 * (self.level-1)
        
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

        self.base_level     = 4
        self.level          = self.base_level + level
        self.EXP_Gain       = 10
        self.Gold_Gain      = 10
        
        self.Maxhealth      = 100   + 6 * (self.level-1)
        self.Strength       = 25    + 1 * (self.level-1)
        self.speed          = 6     + 1 * (self.level-1)
        self.Defense        = 1     + 1 * (self.level-1)
        
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

        self.base_level     = 3
        self.level          = self.base_level + level
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

        self.base_level     = 5
        self.level          = self.base_level + level
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

        self.base_level     = 9
        self.level          = self.base_level + level
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


list_enemy = [Wolf, Direwolf, Ghoul, Zombie, Shadow_Red, Shadow_Blue]
