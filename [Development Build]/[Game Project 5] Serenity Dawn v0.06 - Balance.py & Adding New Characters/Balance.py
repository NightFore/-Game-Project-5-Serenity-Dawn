import random

from Ressources import *


        # Player
class Player:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Ellesia
        self.Sprite = Sprite_Ellesia
        self.Class  = "Lancer"
        
        self.Level      = 1
        self.Experience = 0
        self.Gold       = 0
        self.Action_Point = 0
        
        self.Maxhealth  = 44
        self.Health     = self.Maxhealth
        self.Strength   = 6
        self.Magic      = 10
        self.Speed      = 7
        self.Defense    = 2
        self.Resistance = 0
PlayerIG = Player("NightFore")



class Iris:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Iris
        self.Sprite    = Sprite_Iris
        self.Class  = "Archer"
        
        self.Level      = 1
        self.Experience = 0
        self.Action_Point = 0
        
        self.Maxhealth  = 44
        self.Health     = self.Maxhealth
        self.Strength   = 6
        self.Magic      = 10
        self.Speed      = 9
        self.Defense    = 2
        self.Resistance = 0
IrisIG = Iris("Iris")



class Gyrei:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Gyrei
        self.Sprite    = Sprite_Gyrei
        self.Class = "Dual Wielder"
        
        self.Level      = 1
        self.Experience = 0
        self.Action_Point = 0
        
        self.Maxhealth  = 44
        self.Health     = self.Maxhealth
        self.Strength   = 6
        self.Magic      = 10
        self.Speed      = 6
        self.Defense    = 2
        self.Resistance = 0
GyreiIG = Gyrei("Gyrei")





        # Enemy
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
        self.Speed      = 4 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
WolfIG = Wolf("Wolf")


class Direwolf:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Direwolf
        self.Sprite    = Sprite_Direwolf

        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 6 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
DirewolfIG = Direwolf("Direwolf")


class Ghoul:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Ghoul
        self.Sprite    = Sprite_Ghoul

        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 3 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
GhoulIG = Ghoul("Ghoul")


class Zombie:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Zombie
        self.Sprite    = Sprite_Zombie

        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0

        self.Maxhealth  = 40 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 3 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
ZombieIG = Zombie("Zombie")


class Shadow_Red:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Shadow_Red
        self.Sprite    = Sprite_Shadow_Red

        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 3 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
Shadow_RedIG = Shadow_Red("Shadow_Red")


class Shadow_Blue:
    def __init__(self, name):
        self.name   = name
        self.Icon   = Icon_Shadow_Blue
        self.Sprite    = Sprite_Shadow_Blue

        self.Level      = 1
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.Level - 1)
        self.Health     = self.Maxhealth
        self.Attack     = 4 + 1 * (self.Level - 1)
        self.Speed      = 3 + 1 * (self.Level - 1)
        self.Defense    = 1 + 0.5 * (self.Level - 1)
        self.Resistance = 0 + 0.5 * (self.Level - 1)
Shadow_BlueIG = Shadow_Blue("Shadow_Blue")
