# Badanie przecinania się odcinków, przynależności punktu do trójkątów i wielokątów wypukłych

## Badanie przecinania się odcinków

### Zasada działania

- Jeżeli odcinki leżą na różnych, przecinających się prostych:
    - Wyznaczenie punktu przecięcia prostych.
    - Sprawdzenie, czy punkt przecięcia należy do obu odcinków.
- Jeżeli odcinki leżą na jednej prostej:
    - Sprawdzenie, czy conajmniej jeden koniec jednego z odcinków należy do drugiego.
- Jeżeli odcinki leżą na różnych, równoległych prostych:
    - Odcinki się nie przecinają.

### Implementacja w pythonie

```python
    def przecina(self, odcinek2: Odcinek) -> bool:
        if not self.prosta.czy_równoległa(odcinek2.prosta):
            punkt_przecięcia = self.prosta.punk_przecięcia(odcinek2.prosta)
            return self.czy_zawiera_punkt(punkt_przecięcia) and odcinek2.czy_zawiera_punkt(punkt_przecięcia)
        if self.prosta == odcinek2.prosta:
            return self.czy_zawiera_punkt(odcinek2.początek) or self.czy_zawiera_punkt(odcinek2.koniec)
        else:
            return False
```

#### Sprawdzanie czy proste są równoległe

```python
    def czy_równoległa(self, prosta2: Prosta):
        W = (self.a*prosta2.b)-(prosta2.a*self.b)
        return W == 0
```

### Spawdzenie czy proste są równe

```python
    def __eq__(self, prosta2):
        if isinstance(prosta2, Prosta):
            W = (self.a*prosta2.b)-(prosta2.a*self.b)
            Wx = -(self.c*prosta2.b)+(prosta2.c*self.b)
            Wy = -(self.a*prosta2.c)+(prosta2.a*self.c)
            return W == 0 and Wx == 0 and Wy == 0
        return False
```



## Badanie przynależności punktu do wielokąta wypukłego

### Zasada działania

Funkcja `czy_zawiera_punkt` sprawdza, czy punkt znajduje się wewnątrz wielokąta wypukłego. Dla każdego boku wielokąta obliczany jest iloczyn wektorowy, który pozwala określić, po której stronie boku znajduje się punkt. Jeżeli dla każdego boku wynik iloczynu wektorowego ma ten sam znak, punkt znajduje się wewnątrz wielokąta.

### Implementacja w pythonie

```python
    def czy_zawiera_punkt(self, punkt: Punkt) -> bool:
        if not self.czy_wypukły():
            raise ValueError("Wielokąt musi być wypukły")
        kierunek = 0
        for indeks in range(len(self.wierzchołki)):
            wierzchołek1 = self.wierzchołki[indeks]
            wierzchołek2 = self.wierzchołki[(indeks+1)%len(self.wierzchołki)]
            wektor1 = (wierzchołek2[0]-wierzchołek1[0], wierzchołek2[1]-wierzchołek1[1])
            wektor2 = (punkt[0]-wierzchołek2[0], punkt[1]-wierzchołek2[1])
            iloczyn = iloczyn_wektorowy(wektor1, wektor2)
            if kierunek == 0:
                kierunek = iloczyn
            else:
                if kierunek * iloczyn < 0:
                    return False
        return True
```

#### Funkcja `iloczyn_wektorowy`

```python
def iloczyn_wektorowy(w1, w2):
    return w1[0] * w2[1] - w1[1] * w2[0]
```