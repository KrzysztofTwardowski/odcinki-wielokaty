import pygame
from klasy import *

pygame.init()

okno = pygame.display.set_mode((640, 480))
punkty = []
kolor = "#ffffff"
odcinek1 = None
odcinek2 = None
# odcinek1 = Odcinek(Punkt(100, 100), Punkt(200, 100))
# odcinek2 = Odcinek(Punkt(202, 100), Punkt(250, 100))
# if odcinek1.przecina(odcinek2):
#     kolor = "#00ff00"
# else:
#     kolor = "#ff0000"
zegar = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(punkty) < 4:
                punkty.append(Punkt(*pygame.mouse.get_pos()))
            if len(punkty) == 2:
                odcinek1 = Odcinek(punkty[0], punkty[1])
            elif len(punkty) == 4:
                odcinek1 = Odcinek(punkty[0], punkty[1])
                odcinek2 = Odcinek(punkty[2], punkty[3])
                if odcinek1.przecina(odcinek2):
                    kolor = "#00ff00"
                else:
                    kolor = "#ff0000"
    okno.fill("#000000")
    if isinstance(odcinek1, Odcinek):
        pygame.draw.line(okno, kolor, (odcinek1.początek.x, odcinek1.początek.y), (odcinek1.koniec.x, odcinek1.koniec.y))
    if isinstance(odcinek2, Odcinek):
        pygame.draw.line(okno, kolor, (odcinek2.początek.x, odcinek2.początek.y), (odcinek2.koniec.x, odcinek2.koniec.y))
    pygame.display.update()
    zegar.tick(30)