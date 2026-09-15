import pygame
pygame.init()

print("Greetings, traveler. Please state your name.")
name = input(">> ")
print(f"{name}. It has... a presence to it. Like the smell of petrichor, or perhaps - the stench of a sweaty athlete's foot.")
wait(5)
font = pygame.font.SysFont("Arial", 60)
text_surface = font.render("RUNE OF FOOT", True, (255, 255, 255))
print("Created by Idhant")
