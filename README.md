# Badanie przecinania się odcinków, przynależności punktu do trójkątów i wielokątów wypukłych

## 1. Badanie przecinania się prostych
Do zbadania przecinania się odcinków potrzebna jest informacja o punkcie przecięcia prostych do których należą te odcinki

```python
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
```
Zmienne `self.a`, `self.b` i `self.c` są współczynnikami równania prostej w postaci ogólnej: 
$$ax + by + c = 0$$
Metoda `punkt_przecięcia` zwraca punkt przecięcia danych prostych. Jeżeli proste są równoległe, metoda zwraca `True` lub `False` w zależności od tego, czy proste mają punkty wspólne.

## 2. Badanie przecinania się odcinków
### Konstruktor klasy `Odcinek`

Konstruktor klasy `Odcinek` sprawdza, czy podane punkty się od siebie różnią. Następnie zmienia on kolejność podanych punktów tak, żeby $x_1<x_2$, lub $y_1<y_2$ w przypadku, gdy $x_1=x_2$. Taka kolejność punktów będzie potrzebna przy sprawdzaniu, czy punkt przecięcia prostych należy do odcinka.  
 
$x_1$ i $y_1$ to współrzędne punktu `self.początek`, a $x_2$ i $y_2$ to współrzędne punktu `self.koniec` 



```python
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

        self._prosta = None
```
### Metoda `prosta`
Metoda `prosta` znajduje prostą do której należy odcinek
```python
    @property
    def prosta(self):
        if self._prosta is not None:
            return self._prosta
        a = self.początek[1] - self.koniec[1]
        b = self.koniec[0] - self.początek[0]
        c = -(a*self.początek[0] + b*self.początek[1])
        self._prosta = Prosta(a, b, c)
        return self._prosta
```
Równanie prostej wyznaczane jest poprzez podstawienie współrzędnych skrajnych punktów odcinka do równania prostej:  
$$ax_1 + by_1 + c = 0$$  
$$ax_2 + by_2 + c = 0$$  
Po przekształceniu układu równań otrzymujemy:  
$$a = y_1 - y_2$$  
$$b = x_2 - x_1$$  
$$c = -ax_1 -by_1$$  
### Metoda `przecina`

```python
    def przecina(self, odcinek2: Odcinek) -> bool:
        punkt_przecięcia = self.prosta.punk_przecięcia(odcinek2.prosta)
        if isinstance(punkt_przecięcia, tuple):
            return all((
                self.początek[0] <= punkt_przecięcia[0] <= self.koniec[0],
                odcinek2.początek[0] <= punkt_przecięcia[0] <= odcinek2.koniec[0]
            ))
        elif punkt_przecięcia:
            if self.prosta.b == 0:
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
```

## 2. Badanie przynależności punktu do wielokątów wypukłych
### Sprawdzanie czy wielokąt jest wypukły
```python
    @property
    def wypukły(self):
        if self._wypukły is not None:
            return self._wypukły
        kierunek = 0
        for indeks in range(self.ilość_boków):
            bok = (
                self.wierzchołki[indeks],
                self.wierzchołki[(indeks+1)%self.ilość_boków]
            )
            prosta = Odcinek(*bok).prosta
            nast_punkt = self.wierzchołki[(indeks+2)%self.ilość_boków]
            if prosta.b == 0:
                nowy_kierunek = (bok[1][1] - bok[0][1]) *\
                                ((-prosta.c/prosta.a)-nast_punkt[0])
            else:
                nowy_kierunek = (bok[1][0] - bok[0][0]) *\
                                (nast_punkt[1] + (prosta.a*nast_punkt[0]+prosta.c)/prosta.b)
            if nowy_kierunek == 0:
                continue
            elif kierunek == 0:
                kierunek = nowy_kierunek
            elif kierunek * nowy_kierunek < 0:
                self._wypukły = False
                return self._wypukły
        self._wypukły = True
        return self._wypukły
```
### Sprawdzanie czy punkt należy do wielokąta wypukłego
```python
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
                elif (prosta.a*punkt[0] + prosta.b*punkt[1] + prosta.c) *\
                     (prosta.a*nast_punkt[0] + prosta.b*nast_punkt[1] + prosta.c) >= 0:
                    continue
                else:
                    return False
        return True

```