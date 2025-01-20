# Badanie przecinania się odcinków, przynależności punktu do trójkątów i wielokątów wypukłych

## Badanie przecinania się odcinków

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

### Zasada działania

1. Jeżeli odcinki leżą na różnych, przecinających się prostych:
    - wyznaczenie punktu przecięcia tych prostych
    - sprawdzenie, czy punkt przecięcia prostych należy do dwóch odcinków
2. Jeżeli odcinki leżą na jednej prostej
    - sprawdzenie, czy conajmniej jeden koniec jednego z odcinków należy do drugiego
3. Jeżeli odcinki leżą na różnych, równoległych prostych
    - odcinki się nie przecinają


## Badanie przynależności punktu do wielokąta wypukłego

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

### Zasada działania

1. Dla każdych dwóch kolejnych wierzchołków wielokąta:
    - Utworzenie zmiennych `wektor1` i `wektor2`
        - `wektor1` - wektor od pierwszego do drugiego wierzchołka
        - `wektor2` - wektor od drugiego wierzchołka do badanego punktu
    - Obliczenie wartości iloczynu tych wektorów
    - Sprawdzenie, czy iloczyn jest tego samego znaku dla dowolnego boku
