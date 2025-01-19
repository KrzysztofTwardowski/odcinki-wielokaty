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

    def __eq__(self, prosta2):
        if not isinstance(prosta2, Prosta):
            return False
        W = (self.a*prosta2.b)-(prosta2.a*self.b)
        Wx = -(self.c*prosta2.b)+(prosta2.c*self.b)
        Wy = -(self.a*prosta2.c)+(prosta2.a*self.c)
        return W == 0 and Wx == 0 and Wy == 0

    def czy_równoległa(self, prosta2: Prosta):
        return (self.a*prosta2.b)-(prosta2.a*self.b) == 0

    def punk_przecięcia(self, prosta2: Prosta) -> Punkt:
        if self.czy_równoległa(prosta2):
            raise ValueError("Proste są równoległe")
        W = (self.a*prosta2.b)-(prosta2.a*self.b)
        Wx = -(self.c*prosta2.b)+(prosta2.c*self.b)
        Wy = -(self.a*prosta2.c)+(prosta2.a*self.c)

        return (Wx/W, Wy/W)
                

class Odcinek:
    def __init__(self, początek: Punkt, koniec: Punkt):
        if początek == koniec:
            raise ValueError("punkty muszą się od siebie różnić")
        
        self.początek = początek
        self.koniec = koniec

        a = self.początek[1] - self.koniec[1]
        b = self.koniec[0] - self.początek[0]
        c = -(a*self.początek[0] + b*self.początek[1])
        self.prosta = Prosta(a, b, c)

    def czy_zawiera_punkt(self, punkt: Punkt):
        return all((
            abs(self.koniec[0] - self.początek[0]) >= abs(self.koniec[0] - punkt[0]),
            abs(self.koniec[0] - self.początek[0]) >= abs(punkt[0] - self.początek[0]),
            abs(self.koniec[1] - self.początek[1]) >= abs(self.koniec[1] - punkt[1]),
            abs(self.koniec[1] - self.początek[1]) >= abs(punkt[1] - self.początek[1])
        ))

    def przecina(self, odcinek2: Odcinek) -> bool:
        # Odcinki nie są równoległe
        if not self.prosta.czy_równoległa(odcinek2.prosta):
            punkt_przecięcia = self.prosta.punk_przecięcia(odcinek2.prosta)
            return self.czy_zawiera_punkt(punkt_przecięcia) and odcinek2.czy_zawiera_punkt(punkt_przecięcia)
        # Odcinki leżą na tej samej prostej
        if self.prosta == odcinek2.prosta:
            return self.czy_zawiera_punkt(odcinek2.początek) or self.czy_zawiera_punkt(odcinek2.koniec)
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
