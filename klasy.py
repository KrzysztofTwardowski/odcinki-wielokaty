from __future__ import annotations


class Punkt:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    

class Prosta:
    def __init__(self, a: float, b: float, c: float):
        if (a, b) == (0, 0):
            raise ValueError("a i b nie mogą jednocześnie wynosić 0")
        if a == 0:
            self.a = a/b
            self.b = 1
            self.c = c/b
        else:
            self.a = 1
            self.b = b/a
            self.c = c/a

    def punk_przecięcia(self, prosta2: Prosta) -> Punkt | bool:
        W = (self.a*prosta2.b)-(prosta2.a*self.b)
        Wx = -(self.c*prosta2.b)+(prosta2.c*self.b)
        Wy = -(self.a*prosta2.c)+(self.a*prosta2.c)

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

        # Proste nie są równoległe, przecinają się w jednym punkcie
        if isinstance(punkt_przecięcia, Punkt):
            return all((
                self.początek.x <= punkt_przecięcia.x <= self.koniec.x,
                odcinek2.początek.x <= punkt_przecięcia.x <= odcinek2.koniec.x
            ))
        
        # Oba odcinki należą do tej samej prostej
        elif punkt_przecięcia:
            if self.prosta.b == 0:
                return self.początek.y <= odcinek2.koniec.y and odcinek2.początek.y <= self.koniec.y
            else:
                return self.początek.x <= odcinek2.koniec.x and odcinek2.początek.x <= self.koniec.x
        
        # Proste, do których należą odcinki, się nie przecinają
        else:
            return False