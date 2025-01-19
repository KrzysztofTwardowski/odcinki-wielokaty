from __future__ import annotations

Punkt = tuple[float, float]

def iloczyn_wektorowy(w1, w2):
    return w1[0] * w2[1] - w1[1] * w2[0]

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
        
        if any((
                początek[0] > koniec[0],
                początek[0] == koniec[0] and początek[1] > koniec[1]
            )):
            self.początek = koniec
            self.koniec = początek
        else:
            self.początek = początek
            self.koniec = koniec

    
    def prosta(self):
        a = self.początek[1] - self.koniec[1]
        b = self.koniec[0] - self.początek[0]
        c = -(a*self.początek[0] + b*self.początek[1])
        return Prosta(a, b, c)

    def przecina(self, odcinek2: Odcinek) -> bool:
        punkt_przecięcia = self.prosta().punk_przecięcia(odcinek2.prosta())
        if isinstance(punkt_przecięcia, tuple):
            return all((
                self.początek[0] <= punkt_przecięcia[0] <= self.koniec[0],
                odcinek2.początek[0] <= punkt_przecięcia[0] <= odcinek2.koniec[0]
            ))
        elif punkt_przecięcia:
            if self.prosta().b == 0:
                return all((
                    self.początek[1] <= odcinek2.koniec[1],
                    odcinek2.początek[1] <= self.koniec[1]
                ))
            else:
                return all((self.początek[0] <= odcinek2.koniec[0],
                            odcinek2.początek[0] <= self.koniec[0]
                ))
        else:
            return False


class Wielokąt:
    def __init__(self, *wierzchołki: Punkt):
        if len(wierzchołki) < 3:
            raise ValueError(f"Wielokąt musi mieć conajmniej 3 wierzchołki")
        self.wierzchołki = list(wierzchołki)
        self.wypukły = self.czy_wypukły()
    
    def czy_wypukły(self):
        kierunek = 0
        for indeks in range(len(self.wierzchołki)):
            punkt1 = self.wierzchołki[indeks]
            punkt2 = self.wierzchołki[(indeks+1)%len(self.wierzchołki)]
            punkt3 = self.wierzchołki[(indeks+2)%len(self.wierzchołki)]
            wektor1 = (punkt2[0]-punkt1[0], punkt2[1]-punkt1[1])
            wektor2 = (punkt3[0]-punkt2[0], punkt3[1]-punkt2[1])
            iloczyn = iloczyn_wektorowy(wektor1, wektor2)
            if kierunek == 0:
                kierunek = iloczyn
            else:
                if kierunek * iloczyn < 0:
                    return False
        return True

    def czy_zawiera_punkt(self, punkt: Punkt) -> bool:
        kierunek = 0
        for indeks in range(len(self.wierzchołki)):
            punkt1 = self.wierzchołki[indeks]
            punkt2 = self.wierzchołki[(indeks+1)%len(self.wierzchołki)]
            punkt3 = punkt
            wektor1 = (punkt2[0]-punkt1[0], punkt2[1]-punkt1[1])
            wektor2 = (punkt3[0]-punkt2[0], punkt3[1]-punkt2[1])
            iloczyn = iloczyn_wektorowy(wektor1, wektor2)
            if kierunek == 0:
                kierunek = iloczyn
            else:
                if kierunek * iloczyn < 0:
                    return False
        return True
