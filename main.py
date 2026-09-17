"""
Some notes:
- In battles, you can attack, defend, or check.
- Attack -> chooses a random one of your abilities and uses it against the target. It does the depicted amount of damage,
  and also applies any status effects listed to the target.
- Defend -> Flips a coin. If heads, you block 40% of the damage you'd normally take. If tails, your defense fails. Either
  way, however, you block any status effects the move may have induced.
- Check: Provides information about your enemy, plus juicy lore :DDDDD
"""

import time
import random
import math
win = False
yourWin = False

#Quality of life functions
def header():
    print("---------------------------------")

def line(lines):
    for i in range(lines):
        print()

def wait(duration):
    time.sleep(duration)

def type(text, delay=0.05):
    for char in text:
        # end="" prevents shifting to a new line
        # flush=True forces the terminal to show the character immediately
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# Main things
abilities = [
    {"name":"the fact that they haven't showered in a while :I", "damage":1},
    {"name":"a shove", "damage":1},
    {"name":"a punch", "damage":2},
    {"name":"an uppercut", "damage":3},
    {"name":"a headbutt", "damage":3}
]
lockedAbilities = [
    {"name":"Knife Stab", "damage":6}
]
class Character:
    def __init__(self, name, health, effects, abilities, inventory):
        self.name = name
        self.health = math.ceil(health)
        self.effects = effects
        self.abilities = abilities
        self.defending = False
        self.inventory = inventory
    def attack(self, target):
        move = random.choice(self.abilities)
        damage = move["damage"]
        type(f"{self.name} used {move['name']}!")
        if self.effects == "enraged":
            damage = damage*1.5
        elif self.effects == "injured":
            damage = damage*0.7
        elif self.effects == "confused":
            if random.choice([True, False]):
                damage = 0
                type("...", delay=0.7)
                wait(1)
                type(f"{self.name} missed.")
            else:
                damage = damage
        else:
            damage = damage
        if target.defending:
            if random.choice([True, False]):
                damage *= 0.6
                type(f"{target.name} successfully blocked some of the damage!")
            else:
                type(f"{target.name}'s defense failed!")
            target.defending = False
        else:
            if move.get("statusGive") is not None:
                target.effects = move["statusGive"]
                type(f"{target.name} is now {target.effects}!")
        target.health = math.ceil(target.health - damage)
        if target.health <= 0:
            type(f"{target.name} was defeated.")
            self.effects = "None"
            return True
        elif target.health <= 10:
            type(f"{target.name} is critically injured.")
            if self.effects in ["enraged", "injured", "confused"]:
                if random.randint(1, 3) == 1:
                    self.effects = self.effects
                    type(f"{self.name} is still {self.effects}!")
                else:
                    self.effects = "None"
                    type(f"{self.name} is no longer affected!")
        else:
            type(f"{target.name} has {target.health} health remaining.")
            self.effects = "None"
        return False
    def defend(self, target):
        self.defending = True
        type(f"{self.name} defended against {target.name}!")
    def check(self, target):
        type(f"{target.name}\nHealth: {target.health}\n")
        if target.effects != "None":
            type(f"{target.name} is currently {target.effects}.")
        if target.name == "Frail Psychopath":
            if random.choice([True, False]):
                type(f"One of his eyes is purple. It glints. It twitches.")
            else:
                type(f"It looks like he knows more than he lets on. The bulging veins on his foot disturb you.")
    def abilityUnlock(self, target):
        abilityUnlocked = lockedAbilities[0]
        lockedAbilities.pop(0)
        self.abilities.append(abilityUnlocked)
        self.abilities.pop(0)
        type(f"{self.name} unlocked {abilityUnlocked['name']}!")
        wait(1)
        if target.inventory:
            item = random.choice(target.inventory)
            type(f"{target.name} dropped an item. Pick it up? (Y/N)")
            if input(">> ").lower() == "y":
                self.inventory.append(item)
                wait(1)
                type(f"You got {item}!")
            else:
                type("You ignored it and moved on.")


def brawlIntro(user, target):
    type(f"{user.name} and {target.name} are about to brawl!")
    wait(1)
    type(f"You have {user.health} health, and {target.name} has {target.health} health.")
    wait(1)
    type(f"Let the brawl begin!")

def loss(opp):
    type(f"{opp.name} has won the brawl against you.")
    wait(1)
    type(f"Remember, {player.name}. You are a warrior. You will rise again.")
    wait(1)
    type("After all, you have a tendency to be...")
    wait(2.1)
    type("f o r g e t f u l .", delay=0.41)

def brawl(user, target):
    while user.health > 0 and target.health > 0:
        type("Do you attack (1), defend (2), or check (3)?")
        choice = input(">> ")
        if choice == "2":
            user.defend(target)
        elif choice == "3":
            user.check(target)
        else:
            user.attack(target)

        if target.health <= 0:
            break

        target.attack(user)

    if user.health <= 0:
        loss(target)
        return False

    type(f"You have won the brawl against {target.name}!")
    user.abilityUnlock(target)
    header()
    line(1)
    return True

#Enemy types and abilities

# Frail Psychopath
frailAbilities = [
    {"name":"a weak punch", "damage":1},
    {"name":"a weak slap", "damage":1},
    {"name":"a finger jab to the eyes", "damage":2}
]
frail = Character("Frail Psychopath", 9, "None", frailAbilities, ["Band-Aid"])

# 

entities = [
    {"enemy":frail, "hard":1, "location":["forest"]}
]

def spawn(area, difficulty):
    if isinstance(difficulty, list):
        diff = random.choice(difficulty)
    else:
        diff = difficulty
    possibleEnemies = [
        entity for entity in entities
        if entity["hard"] == diff
        and area.lower() in entity["location"]
    ]
    return random.choice(possibleEnemies)["enemy"]

# Beginning of the game
type("Greetings, traveler. Please state your name.")
name = input(">> ")
type(f"{name}. It has... a presence to it. Like the smell of petrichor, or perhaps - the stench of a sweaty athlete's foot.")
player = Character(name, 15, "None", abilities, [])
line(1)
wait(3)




header()
type("RUNE OF FOOT")
wait(1)
type("CREATED BY IDHANT GUPTA")
header()
wait(5)




# [cinematic introduction, i think]
line(2)
type(f"You wake up on soft ground.")
wait(0.5)
type("Grass.")
wait(1)
type("It's wet.")
wait(1)
type("*You feel a strange sensation, one that makes your mind buzz with rushing memories.* \n*They're too vague to recall.*")
wait(1)
type("You clutch your head as you get up, looking around. The sky is dazzling blue. \nClouds loom over your head.")
wait(1)
type("Suddenly, a scream rattles your ears. You look in its direction, seeing nothing but trees glistening in the sunlight.")
wait(1)
choice = input("Do you yell back at it (1), investigate the source of the scream (2), or ignore it (3)?\n>> ")
if choice == "1":
    type(f'"{input("What do you yell?\n>> ")}" you scream at the top of your lungs.')
    wait(1)
    type("No response.")
    wait(1)
    type("You take a step forward, and the scream gets louder. It sounds like someone is crying for help.")
elif choice == "2":
    type("It sounds like someone is crying for help. You take a step forward, and the scream comes again.")
    wait(1)
elif choice == "3":
    type("You're better than this, you tell yourself.")
    wait(1)
    type("You won't get distracted by a scream. Not again, at least.")
    wait(1)
    type("Wait. Not again?")
    wait(1)
    type("*You fall to the ground, disoriented. Your head throbs with pain and your vision blurs.*")
    wait(1)
    type("*Memories are flooding back, but you can't make sense of them.*")
    wait(1)
    type("Your legs stand up on their own accord as you clutch your head.")
else:
    type("You can't decide what to do. You stand there, frozen in place.")
    wait(1)
    type("Indecisiveness kills. So you take a step forward, and the scream grows in intensity. It sounds like someone is crying for help.")
wait(2)
type("Suddenly you find yourself running at full speed, your legs moving faster than you can comprehend.")
wait(1)
type("Suddenly, you trip over a rock and fall to the ground. You look up, and see a figure standing over you.")
wait(1)
type("The figure is a frail man, looking at you with what looks like deathly intent.")
wait(1)
type("You've entered a brawl!")
wait(1)
brawlIntro(player, frail)
wait(1)
brawl(player, frail)
