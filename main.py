from math import sin, cos, pi
from klasy import Wielokąt, Odcinek, Punkt
from time import perf_counter_ns

def generuj_wielokąt_foremny(ilość_boków: int, środek: Punkt, promień: float):
    kąty = [2*pi/ilość_boków*i for i in range(ilość_boków)]
    wierzchołki = []

    for kąt in kąty:
        x = promień * sin(kąt) + środek[0]
        y = promień * cos(kąt) + środek[1]
        wierzchołki.append((x, y))

    return Wielokąt(*wierzchołki)

if __name__ == "__main__":
    wielokąt = generuj_wielokąt_foremny(
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


    odcinek1 = Odcinek((135, 126), (470, 417))
    odcinek2 = Odcinek((513, 213), (265, 364))
    
    start_czy_przecina = perf_counter_ns()
    print(f"czy odcinki się przecinają: {odcinek1.przecina(odcinek2)}")
    koniec_czy_przecina = perf_counter_ns()
    print(f"sprawdzanie zajęło {(koniec_czy_przecina-start_czy_przecina)/1000000}ms")