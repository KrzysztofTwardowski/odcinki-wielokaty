from __future__ import annotations

class Punkt:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def czy_należy_do(self, wielokąt: Wielokąt):
        if not wielokąt.czy_wypukły():
            raise ValueError("Wielokąt musi być wypukły")
        for indeks in range(len(wielokąt.wierzchołki)):
            bok = (wielokąt.wierzchołki[indeks], wielokąt.wierzchołki[(indeks+1)%len(wielokąt.wierzchołki)])
            inny_wierzchołek = wielokąt.wierzchołki[(indeks+2)%len(wielokąt.wierzchołki)]
            prosta_boku = Odcinek(*bok).prosta
            if prosta_boku.b != 0:
                położenie_wierzchołka = (bok[1].x - bok[0].x) * (inny_wierzchołek.y - (-prosta_boku.a*inny_wierzchołek.x-prosta_boku.c)/prosta_boku.b)
                położenie_punktu = (bok[1].x - bok[0].x) * (self.y - (-prosta_boku.a*self.x-prosta_boku.c)/prosta_boku.b)
            else:
                położenie_wierzchołka = (bok[1].y - bok[0].y) * ((-prosta_boku.c/prosta_boku.a) - inny_wierzchołek.x)
                położenie_punktu = (bok[1].y - bok[0].y) * ((-prosta_boku.c/prosta_boku.a) - inny_wierzchołek.x)
            if inny_wierzchołek == 0:
                continue
            elif położenie_punktu * położenie_wierzchołka < 0:
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

    def czy_wypukły(self):
        kierunek = 0
        for indeks in range(len(self.wierzchołki)):
            bok = (self.wierzchołki[indeks], self.wierzchołki[(indeks+1)%len(self.wierzchołki)])
            nast_wierzchołek = self.wierzchołki[(indeks+2)%len(self.wierzchołki)]
            prosta_boku = Odcinek(*bok).prosta
            if prosta_boku.b != 0:
                nowy_kierunek = (bok[1].x - bok[0].x) * (nast_wierzchołek.y - (-prosta_boku.a*nast_wierzchołek.x-prosta_boku.c)/prosta_boku.b)
            else:
                nowy_kierunek = (bok[1].y - bok[0].y) * ((-prosta_boku.c/prosta_boku.a)-nast_wierzchołek.x)
            if nowy_kierunek == 0:
                continue
            nowy_kierunek //= abs(nowy_kierunek)
            if kierunek == 0:
                kierunek = nowy_kierunek
            elif kierunek != nowy_kierunek:
                return False
        return True