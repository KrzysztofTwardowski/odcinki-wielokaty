import pygame, klasy
pygame.init()

okno = pygame.display.set_mode((1440, 900))
zegar = pygame.time.Clock()

punkty_wielokąta = []
punkty = []

kolor = "#ffffff"
wielokąt = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if wielokąt is None:
                punkty_wielokąta.append(pygame.mouse.get_pos())
            elif wielokąt.wypukły:
                punkty.append(pygame.mouse.get_pos())
                print(punkty[-1])
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print(punkty_wielokąta)
            if wielokąt is None:
                wielokąt = klasy.Wielokąt(*punkty_wielokąta)
                if wielokąt.wypukły:
                    kolor = "#00ff00"
                else:
                    kolor = "#ff0000"
                punkty_wielokąta.append(punkty_wielokąta[0])
    

    for indeks in range(len(punkty_wielokąta)-1):
        pygame.draw.line(okno, kolor, punkty_wielokąta[indeks], punkty_wielokąta[indeks+1])
    
    while wielokąt and len(punkty) > 0:
        punkt = punkty.pop()
        if wielokąt.czy_zawiera_punkt(punkt):
            kolor_punktu = "#00ff00"
        else:
            kolor_punktu = "#ff0000"
        pygame.draw.circle(okno, kolor_punktu, punkt, 3)


    pygame.display.update()
    zegar.tick(60)
