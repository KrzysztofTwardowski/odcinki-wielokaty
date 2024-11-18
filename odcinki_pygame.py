import pygame
from klasy import *

pygame.init()

okno = pygame.display.set_mode((640, 480))
zegar = pygame.time.Clock()

punkty = []
kolor = "#ffffff"

odcinek1 = None
odcinek2 = None
stworzono_odcinki = False

# odcinek1 = Odcinek((135, 126), (470, 417))
# odcinek2 = Odcinek((513, 213), (265, 364))
# stworzono_odcinki = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(punkty) < 4:
                punkty.append(pygame.mouse.get_pos())
            if len(punkty) == 2:
                odcinek1 = Odcinek(punkty[0], punkty[1])
            elif len(punkty) == 4:
                print(*[(punkt[0], punkt[1]) for punkt in punkty])
                if odcinek1 is None:
                    odcinek1 = Odcinek(punkty[0], punkty[1])
                odcinek2 = Odcinek(punkty[2], punkty[3])
                stworzono_odcinki = True

    okno.fill("#000000")
    if stworzono_odcinki:
        if odcinek1.przecina(odcinek2):
            kolor = "#00ff00"
        else:
            kolor = "#ff0000"

    if isinstance(odcinek1, Odcinek):
        pygame.draw.line(okno, kolor, (odcinek1.początek[0], odcinek1.początek[1]), (odcinek1.koniec[0], odcinek1.koniec[1]))
    if isinstance(odcinek2, Odcinek):
        pygame.draw.line(okno, kolor, (odcinek2.początek[0], odcinek2.początek[1]), (odcinek2.koniec[0], odcinek2.koniec[1]))
    pygame.display.update()
    zegar.tick(60)