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