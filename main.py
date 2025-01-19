from klasy import Wielokąt, Odcinek

if __name__ == "__main__":
    # sprawdzanie przecinania się odcinków
    odcinek1 = Odcinek((0, 10), (100, 10))
    odcinek2 = Odcinek((-10, 15), (10, 15))
    print(f"czy odcinki się przecinają: {odcinek1.przecina(odcinek2)}")

    # sprawdzanie przynależności punktu do wielokąta wypukłego
    wielokąt = Wielokąt((10, 10), (100, 10), (100, 100), (10, 100))
    punkt = (50, 50)
    print(f"czy punkt należy do wielokąta: {wielokąt.czy_zawiera_punkt(punkt)}")