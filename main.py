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

def line(lines=1):
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
    def __init__(self, name, health, maxHealth, effects, abilities, inventory):
        self.name = name
        self.health = math.ceil(health)
        self.maxHealth = math.ceil(maxHealth)
        self.effects = effects
        self.abilities = abilities
        self.defending = False
        self.inventory = inventory
    def attack(self, target):
        move = random.choice(self.abilities)
        damage = move["damage"]
        wait(1)
        type(f"{self.name} used {move['name']}!")
        if self.effects in ["enraged", "strengthened"]:
            damage = damage*1.5
        elif self.effects in ["injured", "weakened"]:
            damage = damage*0.7
        elif self.effects in ["confused", "blinded"]:
            if random.choice([True, False]):
                damage = 0
                type("...", delay=0.7)
                wait(1)
                type(f"{self.name} missed.")
            else:
                pass
        elif self.effects == "short of breath":
            if random.choice([True, False]):
                damage = 0
                type(f"G a s p .", delay=0.45)
                wait(1)
                type(f"{self.name} couldn't catch their breath and missed!")
            else:
                damage = damage*0.8
        elif self.effects == "bleeding":
            damage = damage*0.5
            type(f"As {self.name} touches their skin, they realize that there's a concerning amount of blood.")
            wait(1)
            type(f"It's warm.", delay = 0.23)
        elif self.effects == "bleeding severely":
            damage = damage*0.2
            type(f"{self.name} feels incredibly dizzy. They grab a nearby surface to keep themselves steady.")
            wait(1)
            type(f"They're covered in blood. Everything hurts.")
        else:
            pass
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
            if self.effects not in ["None", None]:
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
    def heal(self, amt):
        if self.maxHealth - self.health >= amt:
            self.health += amt
        else:
            self.health = self.maxHealth
    def defend(self, target):
        self.defending = True
        type(f"{self.name} defended against {target.name}!")
    def check(self, target):
        type(f"{target.name}\nHealth: {target.health}\n")
        type(f"Max Health: {target.maxHealth}")
        if target.effects != "None":
            type(f"{target.name} is currently {target.effects}.")
        if target.name == "Frail Psychopath":
            if random.choice([True, False]):
                type(f"One of his eyes is purple. It glints. It twitches.")
            else:
                type(f"It looks like he knows more than he lets on. The bulging veins on his foot disturb you.")
        elif target.name == "Baby Handrew":
            if random.choice([True, False]):
                type(f'"It must be the result of bad parenting," you think. Well then, bad parenting must kill.')
            else:
                type(f"His fingers twitch with the excitement of youth and the bloodthirst of a vampire.")
        elif target.name == "Foot Cultist":
            if random.choice([True, False]):
                type(f"He's wearing a dazzling white cloak. You can't help but notice that there's blood stains.")
            else:
                type(f"He's wearing a foot-shaped mask. It fits his head almost perfectly.")
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
    type("You've entered a brawl!")
    wait(1)
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
frail = Character("Frail Psychopath", 9, 9, "None", frailAbilities, ["Band-Aid"])

# Handrew Lineage (Forest)
handrewAbilitiesForest = [
    {"name":"Chokehold", "damage":6, "statusGive":"short of breath"},
    {"name":"Thumb Pinned", "damage":9},
    {"name":"Pinch", "damage":5},
    {"name":"Nail Scratch", "damage":7, "statusGive":"bleeding"},
    {"name":"Prolonged, Incessant, and Incredibly Annoying Poking", "damage":8}
]
forestHandrew = Character("Handrew", 17, 17, "None", handrewAbilitiesForest, ["Nail Polish"])

babyHandrewAbilities = [
    {"name":"Tap", "damage": 2},
    {"name": "Baby Scratch", "damage": 3, "statusGive":"injured"},
    {"name":"Hyperactivity", "damage": 3, "statusGive":"confused"},
    {"name": "Pacifier Throw", "damage":2}
]
babyHandrew = Character("Baby Handrew", 9, 9, "None", babyHandrewAbilities, [])

# Rock, Paper, Scissors
rpsAbilities = [
    {"name":"Rock", "damage":20},
    {"name":"Rock", "damage":15},
    {"name": "Rock", "damage":17},
    {"name":"Scissors", "damage": 10, "statusGive":"injured"},
    {"name":"Scissors", "damage":12},
    {"name": "Scissors", "damage":13},
    {"name": "Paper", "damage":5, "statusGive":"bleeding"},
    {"name": "Paper", "damage":5, "statusGive":"short of breath"},
    {"name": "Paper", "damage": 3, "statusGive":"bleeding severely"}
]
rockPaperScissor = Character("Rock, Paper, Scissors", 25, 25, "None", rpsAbilities, ["A Rock", "A Piece of Paper", "A Pair of Scissors"])

# Foot Cultists
weakCultistAbilities = [
    {"name":"their staff", "damage":2},
    {"name":"a fragment of the Rune", "damage":5},
    {"name":"Thunderclap", "damage":4},
    {"name":"Thunderclap", "damage":4},
    {"name":"a small fireball", "damage":3},
    {"name": "a shard of glass", "damage": 3}
]
weakCultist = Character("Foot Cultist", 16, 16, "None", weakCultistAbilities, ["Serum"])

entities = [
    {"enemy": forestHandrew, "hard": 4, "location":["forest"]},
    {"enemy": babyHandrew, "hard":2, "location":["forest", "village"]},
    {"enemy": rockPaperScissor, "hard": 6, "location":["village", "castle", "sanctuary"]},
    {"enemy": weakCultist, "hard":3, "location":["forest", "village"]}
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
    enemy = random.choice(possibleEnemies)["enemy"]

    return Character(
        enemy.name,
        enemy.maxHealth,
        enemy.maxHealth,
        "None",
        enemy.abilities.copy(),
        enemy.inventory.copy()
    )

# The Pocket
pocket = []

def usePocket(player):
    type("P O C K E T")

    if pocket:
        type(f"Inside: {pocket[0]}")
    else:
        type("The Pocket is empty.")

    type("Do you want to put an item in (1), take an item out (2), or leave (3)?")
    choice = input(">> ")

    if choice == "1":
        if not player.inventory:
            type("Your inventory is empty.")
            return

        type("What item do you want to put in?")
        for i, item in enumerate(player.inventory, 1):
            type(f"{i}. {item}")

        choice = int(input(">> ")) - 1
        item = player.inventory[choice]

        if pocket:
            type(f"The Pocket is already holding {pocket[0]}.")
            type("Replace it with this item? (Y/N)")

            replace = input(">> ").lower()

            if replace == "y":
                oldItem = pocket.pop(0)
                pocket.append(item)

                player.inventory[choice] = oldItem

                type(f"You replaced {oldItem} with {item}.")
            else:
                type("You left the Pocket unchanged.")

        else:
            player.inventory.pop(choice)
            pocket.append(item)

            type(f"You put {item} into the Pocket.")

    elif choice == "2":
        if not pocket:
            type("The Pocket is empty.")
            return

        item = pocket.pop(0)
        player.inventory.append(item)

        type(f"You took {item} out of the Pocket.")

    elif choice == "3":
        type("You left the Pocket alone.")

# Beginning of the game
type("Greetings, traveler. Please state your name.")
name = input(">> ")
type(f"{name}. It has... a presence to it. Like the smell of petrichor, or perhaps - the stench of a sweaty athlete's foot.")
player = Character(name, 15, 15, "None", abilities, [])
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
player.maxHealth = 25
wait(1)
type("You huff, not knowing what just happened.")
wait(1)
type(f"You decide to follow his footprints.")
wait(1)
type("As you follow them, you reach a... pond.")
wait(1)
type("Birds are chirping, and you see a innocent-looking duck waddling gently through the water.")
wait(1)
type("It's all so tranquil. You could just fall asle -")
wait(4)
line()
type("R i s e  a n d  s h i n e .", delay = 0.45)
wait(1)
type("You look at the positions of the shadows. It seems like a few hours have passed since you fell asleep.")
player.heal(5)
wait(1)
type("You get up and start looking around. You walk down to the foot of the pond, letting your hand dip in so that you can feel the cool water on your skin.")
wait(1)
type("You use some sticks and spare string to make a makeshift fishing rod.")
wait(1)
type("You feel something bite your hook.")
wait(1)
type("You reel it in. \nIt's a raw fish!")
wait(1)
type("You cast your line again.")
wait(4)
type("Something bites.")
wait(1)
type("This is not a fish.")
wait(1)
brawlIntro(player, spawn("forest", [2, 3]))
