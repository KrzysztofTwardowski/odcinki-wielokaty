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
Parametry `self.a`, `self.b` i `self.c` są współczynnikami równania prostej w postaci ogólnej: 
$$ax + by + c = 0$$
Metoda `punkt_przecięcia` zwraca rozwiązanie układu równań danych prostych. Jeżeli proste są równoległe, metoda zwraca `True` lub `False` w zależności od tego, czy proste mają punkty wspólne.

## 2. Badanie przecinania się odcinków
### Konstruktor klasy `Odcinek`
Konstruktor klasy `Odcinek` sprawdza, czy podane punkty się od siebie różnią. Następnie zmienia on kolejność podanych punktów, żeby $x$ punktu `początek` był mniejszy niż $x$ punktu `koniec`. w przypadku, gdy wartości współrzędnej $x$ obu punktów są równe kolejność tych punktów jest zmieniana tak, żeby $y$ punktu `początek` był mniejszy niż y punktu `koniec`. Taka kolejność punktów jest potrzebna przy sprawdzaniu, czy punkt przecięcia prostych należy do odcinka.

```python
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

        self._prosta = None
```
### Właściwość `prosta`
Właściwość `prosta` znajduje prostą do której należy odcinek
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
Gdzie $x_1$, $y_1$, $x_2$, $y_2$ to kolejno: `self.początek[0]`, `self.początek[1]`, `self.koniec[0]`, `self.koniec[1]`.  
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
                return self.początek[1] <= odcinek2.koniec[1] and odcinek2.początek[1] <= self.koniec[1]
            else:
                return self.początek[0] <= odcinek2.koniec[0] and odcinek2.początek[0] <= self.koniec[0]
        else:
            return False
```