from __future__ import annotations

Punkt = tuple[float, float]

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
        
        return (Wx/W, Wy/W)
                

class Odcinek:
    def __init__(self, początek: Punkt, koniec: Punkt):
        if początek == koniec:
            raise ValueError("punkty muszą się od siebie różnić")
        
        if (początek[0] > koniec[0]) or (początek[0] == koniec[0] and początek[1] > koniec[1]):
            self.początek = koniec
            self.koniec = początek
        else:
            self.początek = początek
            self.koniec = koniec

        a = self.początek[1] - self.koniec[1]
        b = self.koniec[0] - self.początek[0]
        c = -(a*self.początek[0] + b*self.początek[1])
        self.prosta = Prosta(a, b, c)
    
    def przecina(self, odcinek2: Odcinek) -> bool:
        punkt_przecięcia = self.prosta.punk_przecięcia(odcinek2.prosta)
        if isinstance(punkt_przecięcia, tuple):
            return all((
                self.początek[0] <= punkt_przecięcia[0] <= self.koniec[0],
                odcinek2.początek[0] <= punkt_przecięcia[0] <= odcinek2.koniec[0]
            ))
        elif punkt_przecięcia:
            if self.prosta.b == 0:
                return self.początek[1] <= odcinek2.koniec[1] and odcinek2.początek[1] <= self.koniec[1]
            else:
                return self.początek[0] <= odcinek2.koniec[0] and odcinek2.początek[0] <= self.koniec[0]
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
                nowy_kierunek = (bok[1][1] - bok[0][1]) * ((-prosta.c/prosta.a)-nast_punkt[0])
            else:
                nowy_kierunek = (bok[1][0] - bok[0][0]) * (nast_punkt[1] - (-prosta.a*nast_punkt[0]-prosta.c)/prosta.b)
            if nowy_kierunek == 0:
                continue
            elif kierunek == 0:
                kierunek = nowy_kierunek
            elif kierunek * nowy_kierunek < 0:
                return False
        return True

    def czy_zawiera_punkt(self, punkt: Punkt) -> bool:
        if not self.wypukły:
            raise ValueError("Wielokąt musi być wypukły")
        for indeks in range(self.ilość_boków):
            prosta = Odcinek(
                self.wierzchołki[indeks],
                self.wierzchołki[(indeks+1)%self.ilość_boków]
            ).prosta
            nast_punkt = self.wierzchołki[(indeks+2)%self.ilość_boków]
            if prosta.b == 0:
                x_prostej = -prosta.c / prosta.a
                if (x_prostej - nast_punkt[0]) == 0:
                    continue
                elif (x_prostej - nast_punkt[0]) * (x_prostej - punkt[0]) >= 0:
                    continue
                else:
                    return False
            else:
                if (prosta.a*nast_punkt[0] + prosta.b*nast_punkt[1] + prosta.c) == 0:
                    continue
                elif (prosta.a*punkt[0] + prosta.b*punkt[1] + prosta.c) * (prosta.a*nast_punkt[0] + prosta.b*nast_punkt[1] + prosta.c) >= 0:
                    continue
                else:
                    return False
        return True
