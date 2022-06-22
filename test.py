import pygame
import time

for i in range(5):
    print(i)

pygame.init()
t0 = time.time()
fonts = pygame.font.get_fonts()
print(len(fonts))
for f in fonts:
    print(f)
# font = pygame.font.SysFont("impact", 72)
print("Time: " + str(time.time() - t0))

# from random import randrange
# 
# one = 0
# two = 0
# three = 0
# four = 0
# five = 0
# six = 0
# seven = 0

# def get_random():
#     return round(randrange(7) + 1)

# for i in range(10000):
#     rng = get_random()
#     if (rng == 1): one += 1
#     if (rng == 2): two += 1
#     if (rng == 3): three += 1
#     if (rng == 4): four += 1
#     if (rng == 5): five += 1
#     if (rng == 6): six += 1
#     if (rng == 7): seven += 1

# print(one)
# print(two)
# print(three)
# print(four)
# print(five)
# print(six)
# print(seven)
