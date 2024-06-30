import random

c = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

# Random ID Generator
def generate_id() -> str:
    r = ""
    for _ in range(30): r += c[random.randrange(0, len(c))]
    return r
