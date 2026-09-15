import time

print("Greetings, traveler. Please state your name.")
name = input(">> ")
print(f"{name}. It has... a presence to it. Like the smell of petrichor, or perhaps - the stench of a sweaty athlete's foot.")
time.sleep(3)
def type(text, delay=0.05):
    for char in text:
        # end="" prevents shifting to a new line
        # flush=True forces the terminal to show the character immediately
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
type("RUNE OF FOOT")
type("CREATED BY IDHANT GUPTA")
