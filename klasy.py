from __future__ import annotations

class Punkt:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Punkt) and (value.x, value.y) == (self.x, self.y)

    def należy_do_wielokąta(self, wielokąt: Wielokąt) -> bool:
        if not wielokąt.wypukły:
            raise ValueError("Wielokąt musi być wypukły")
        for indeks in range(wielokąt.ilość_boków):
            prosta = Odcinek(
                wielokąt.wierzchołki[indeks],
                wielokąt.wierzchołki[(indeks+1)%wielokąt.ilość_boków]
            ).prosta
            nast_punkt = wielokąt.wierzchołki[(indeks+2)%wielokąt.ilość_boków]
            if prosta.b == 0:
                x_prostej = -prosta.c / prosta.a
                if (x_prostej - nast_punkt.x) == 0:
                    continue
                elif (x_prostej - nast_punkt.x) * (x_prostej - self.x) >= 0:
                    continue
                else:
                    return False
            else:
                if (prosta.a*nast_punkt.x + prosta.b*nast_punkt.y + prosta.c) == 0:
                    continue
                elif (prosta.a*self.x + prosta.b*self.y + prosta.c) * (prosta.a*nast_punkt.x + prosta.b*nast_punkt.y + prosta.c) >= 0:
                    continue
                else:
                    return False
        return True

class Prosta:
    def __init__(self, a: float, b: float, c: float):
        if (a, b) == (0, 0):
            raise ValueError("a i b nie mogą jednocześnie wynosić 0")
        self.a = a
        self.b = b
        self.c = c

    def punk_przecięcia(self, prosta2: Prosta) -> Punkt | bool:
        W = (self.a*prosta2.b)-(prosta2.a*self.b)
        Wx = -(self.c*prosta2.b)+(prosta2.c*self.b)
        Wy = -(self.a*prosta2.c)+(prosta2.a*self.c)

        if W == 0:
            return (Wx, Wy) == (0, 0)
        
        return Punkt(Wx/W, Wy/W)
                

class Odcinek:
    def __init__(self, początek: Punkt, koniec: Punkt):
        if początek == koniec:
            raise ValueError("punkty muszą się od siebie różnić")
        
        if (początek.x > koniec.x) or (początek.x == koniec.x and początek.y > koniec.y):
            self.początek = koniec
            self.koniec = początek
        else:
            self.początek = początek
            self.koniec = koniec

        a = self.początek.y - self.koniec.y
        b = self.koniec.x - self.początek.x
        c = -(a*self.początek.x + b*self.początek.y)
        self.prosta = Prosta(a, b, c)
    
    def przecina(self, odcinek2: Odcinek) -> bool:
        punkt_przecięcia = self.prosta.punk_przecięcia(odcinek2.prosta)
        if isinstance(punkt_przecięcia, Punkt):
            return all((
                self.początek.x <= punkt_przecięcia.x <= self.koniec.x,
                odcinek2.początek.x <= punkt_przecięcia.x <= odcinek2.koniec.x
            ))
        elif punkt_przecięcia:
            if self.prosta.b == 0:
                return self.początek.y <= odcinek2.koniec.y and odcinek2.początek.y <= self.koniec.y
            else:
                return self.początek.x <= odcinek2.koniec.x and odcinek2.początek.x <= self.koniec.x
        else:
            return False


class Wielokąt:
    def __init__(self, *wierzchołki: Punkt):
        if len(wierzchołki) < 3:
            raise ValueError(f"Wielokąt musi mieć conajmniej 3 wierzchołki, a podano {len(wierzchołki)}")
        self.wierzchołki = wierzchołki
        self.ilość_boków = len(self.wierzchołki)
        self.wypukły = self.czy_wypukły()
    
    def czy_wypukły(self) -> bool:
        kierunek = 0
        for indeks in range(self.ilość_boków):
            bok = (
                self.wierzchołki[indeks],
                self.wierzchołki[(indeks+1)%self.ilość_boków]
            )
            prosta = Odcinek(*bok).prosta
            nast_punkt = self.wierzchołki[(indeks+2)%self.ilość_boków]
            if prosta.b == 0:
                nowy_kierunek = (bok[1].y - bok[0].y) * ((-prosta.c/prosta.a)-nast_punkt.x)
            else:
                nowy_kierunek = (bok[1].x - bok[0].x) * (nast_punkt.y - (-prosta.a*nast_punkt.x-prosta.c)/prosta.b)
            if nowy_kierunek == 0:
                continue
            elif kierunek == 0:
                kierunek = nowy_kierunek
            elif kierunek * nowy_kierunek < 0:
                return False
        return True