import pygame


def inputMouse():
    if pattern1:
        pattern = open("patterns/gliter_gun.txt", "r")
        for i in range(9):
            riadok = pattern.readline()
            for j in range(len(riadok) - 1):
                a = int(riadok[j])
                hernePole[mousePos[1] // SIZE + i][mousePos[0] // SIZE + j] = a
    else:
        hernePole[mousePos[1] // SIZE][mousePos[0] // SIZE] = 1


def draw():
    black = (0, 0, 0)
    grey = 0x4d544f
    for i in range(HEIGHT // SIZE):
        for j in range(WIDTH // SIZE):
            if hernePole[i][j] == 1:
                pygame.draw.rect(window, black, [j * SIZE, i * SIZE, SIZE, SIZE])


def countNeighbours(x, y):
    neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                if WIDTH // SIZE > x + i >= 0 <= y + j < HEIGHT // SIZE:
                    neighbours += hernePole[y + i][x + j]
            except(IndexError):
                pass
    neighbours -= hernePole[y][x]
    return neighbours

def rules(hernePole):
    hernePole2 = []
    for i in range(HEIGHT // SIZE):
        riadok = []
        for j in range(WIDTH // SIZE):
            riadok.append(0)
        hernePole2.append(riadok)
    # cyklus na overenie susedov
    for i in range(HEIGHT // SIZE):
        for j in range(WIDTH // SIZE):
            if hernePole[i][j] == 1:
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if a == b or hernePole[i + a][j + b] == 0:
                            neighbours = countNeighbours(j + b, i + a)
                            # overenie zivota a smrti
                            if hernePole[i + a][j + b] == 1 and HEIGHT // SIZE > i + a >= 0 <= j + b < WIDTH // SIZE:
                                if neighbours < 2 or neighbours > 3:
                                    hernePole2[i + a][j + b] = 0
                                else:
                                    hernePole2[i + a][j + b] = 1
                            if hernePole[i + a][j + b] == 0:
                                if neighbours == 3:
                                    hernePole2[i + a][j + b] = 1
                                else:
                                    hernePole2[i + a][j + b] = 0
    hernePole = hernePole2.copy()
    return hernePole


pygame.init()
WIDTH = 800
HEIGHT = 600
SIZE = 4
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
done = False
clock = pygame.time.Clock()
hernePole = []
for i in range(HEIGHT // SIZE):
    riadok = []
    for j in range(WIDTH // SIZE):
        riadok.append(0)
    hernePole.append(riadok)
mousePos = []
pause = True
click = False
pattern1 = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_1:
                pattern1 = not pattern1
    window.fill((255, 255, 255))
    mousePos = pygame.mouse.get_pos()
    if click:
        inputMouse()
    draw()
    if not pause:
        hernePole = rules(hernePole)
    pygame.display.flip()
    if not pause:
        clock.tick(60)
pygame.quit()
