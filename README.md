# Badanie przecinania się odcinków, przynależności punktu do trójkątów i wielokątów wypukłych

## Badanie przecinania się odcinków

### Jeżeli odcinki nie są równoległe

- Wyznaczenie punktu przecięcia protych, do których należą te odcinki
- Sprawdzenie, czy znaleziony punkt należy do obu odcinków

### Jeżeli odcinki leżą na tej samej prostej

- Sprawdzenie, czy conajmniej jeden koniec jednego z odcinków należy do drugiego

### Jeżeli odcinki leżą na różnych, równoległych prostych

- Odcinki się nie przecinają

```python
    def przecina(self, odcinek2: Odcinek) -> bool:
        if not self.prosta().czy_równoległa(odcinek2.prosta()):
            punkt_przecięcia = self.prosta().punk_przecięcia(odcinek2.prosta())
            return self.czy_zawiera_punkt(punkt_przecięcia) and odcinek2.czy_zawiera_punkt(punkt_przecięcia)
        if self.prosta() == odcinek2.prosta():
            return self.czy_zawiera_punkt(odcinek2.początek) or self.czy_zawiera_punkt(odcinek2.koniec)
        else:
            return False
```

### Sprawdzanie czy proste są równoległe

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
class Wielokąt:
    def __init__(self, *wierzchołki: Punkt):
        if len(wierzchołki) < 3:
            raise ValueError("Wielokąt musi mieć conajmniej 3 wierzchołki")
        self.wierzchołki = list(wierzchołki)

    def czy_zawiera_punkt(self, punkt: Punkt) -> bool:
        for indeks in range(len(self.wierzchołki)):
            wierzchołek1 = self.wierzchołki[indeks]
            wierzchołek2 = self.wierzchołki[(indeks+1)%len(self.wierzchołki)]
            wierzchołek3 = self.wierzchołki[(indeks+2)%len(self.wierzchołki)]
            prosta = Odcinek(wierzchołek1, wierzchołek2).prosta()
            a, b, c = prosta.a, prosta.b, prosta.c
            if (a*wierzchołek3[0] + b*wierzchołek3[1] + c) * (a*punkt[0] + b*punkt[1] + c) < 0:
                return False
        return True
```