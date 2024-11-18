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
Metoda `przecina` zwraca `True`, gdy:  
  - Proste, do których należą odcinki, przecinają się w jednym punkcie oraz punkt przecięcia prostych należy do obu odcinków  
  - Oba odcinki leżą na tej samej prostej i mają punkty wspólne  

Gdy żaden z powyższych warunków nie jest spełniony metoda zwraca `False`.  

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

## Przykłady użycia
### 1. plik `main.py`
```python
from klasy import Wielokąt, Odcinek
from time import perf_counter_ns

if __name__ == "__main__":
    # sprawdzanie przecinania się odcinków
    odcinek1 = Odcinek((135, 126), (470, 417))
    odcinek2 = Odcinek((513, 213), (265, 364))
    start_czy_przecina = perf_counter_ns()
    print(f"czy odcinki się przecinają: {odcinek1.przecina(odcinek2)}")
    koniec_czy_przecina = perf_counter_ns()
    print(f"sprawdzanie zajęło {(koniec_czy_przecina-start_czy_przecina)/1000000}ms")

    # sprawdzanie przynależności punktu do wielokąta wypukłego
    wielokąt = Wielokąt.generuj_foremny(
        ilość_boków=10_000,
        środek=(10, 10),
        promień=100
    )
    punkt = (50, 50)

    start_czy_wypukły = perf_counter_ns()
    print(f"czy wypukły: {wielokąt.wypukły}")
    koniec_czy_wypukły = perf_counter_ns()
    print(f"sprawdzanie zajęło {(koniec_czy_wypukły - start_czy_wypukły)/1000000}ms")

    start_przynależność_punktu = perf_counter_ns()
    print(f"czy punkt należy do wielokąta: {wielokąt.czy_zawiera_punkt(punkt)}")
    koniec_przynależność_punktu = perf_counter_ns()
    print(f"sprawdzanie zajęło {(koniec_przynależność_punktu - start_przynależność_punktu)/1000000}ms")
```

### 2. plik `odcinki_pygame.py`
```python
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

odcinek1 = Odcinek((135, 126), (470, 417))
odcinek2 = Odcinek((513, 213), (265, 364))
stworzono_odcinki = True

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
```

### 3. plik `wielokąty_pygame.py`
```python
import pygame, klasy
pygame.init()

okno = pygame.display.set_mode((1440, 900))
zegar = pygame.time.Clock()

punkty = []
punkty_wielokąta = []
kolor = "#ffffff"

wielokąt = None
stworzono_wielokąt = False

wielokąt = klasy.Wielokąt.generuj_foremny(25, (720, 450), 400)
stworzono_wielokąt = True

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
                stworzono_wielokąt = True
    
    if stworzono_wielokąt:
        if wielokąt.wypukły:
            kolor = "#00ff00"
        else:
            kolor = "#ff0000"
        punkty_wielokąta = wielokąt.wierzchołki + [wielokąt.wierzchołki[0]]

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
```