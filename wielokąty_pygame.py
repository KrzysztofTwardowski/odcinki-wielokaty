import pygame, klasy
pygame.init()

okno = pygame.display.set_mode((1440, 900))
zegar = pygame.time.Clock()

punkty_wielokąta = []
punkty = []
for x in range(0, okno.get_width(), 10):
    for y in range(0, okno.get_height(), 10):
        punkty.append(klasy.Punkt(x, y))

kolor = "#ffffff"
wielokąt = None
punkty_obraz = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            punkty_wielokąta.append(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            wielokąt = klasy.Wielokąt(*[klasy.Punkt(x, y) for x, y in punkty_wielokąta])
            punkty_wielokąta.append(punkty_wielokąta[0])
    
    okno.fill("#000000")
    if punkty_obraz:
        okno.blit(punkty_obraz, (0, 0))
    for indeks in range(len(punkty_wielokąta)-1):
        pygame.draw.line(okno, kolor, punkty_wielokąta[indeks], punkty_wielokąta[indeks+1])

    if wielokąt and not punkty_obraz:
        if wielokąt.wypukły():
            kolor = "#00ff00"
            punkty_obraz=pygame.surface.Surface(pygame.display.get_window_size())
            for point in punkty:
                if point.należy_do_wielokąta(wielokąt):
                    pygame.draw.circle(punkty_obraz, "#00ff00", (point.x, point.y), 1)
                else:
                    pygame.draw.circle(punkty_obraz, "#ff0000", (point.x, point.y), 1)
        else:
            kolor = "#ff0000"

    pygame.display.update()
    zegar.tick(60)