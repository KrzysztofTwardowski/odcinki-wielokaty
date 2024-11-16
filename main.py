import klasy

if __name__ == "__main__":
    wielokąt = klasy.Wielokąt(
        (-128.111, 478.32), (150.645, 314.45), (453.342, 387.7), (593.43, 631.345), (54.12, 854.435), (-171.23, 712.345)
    )
    punkt = (38.676, 449.333)
    odcinek1 = klasy.Odcinek((159.6, -213.77), (524.78, -344.91))
    odcinek2 = klasy.Odcinek((322, -409.5), (408.22, -193.875))
    print(f"Czy punkt należy do wielokąta: {wielokąt.czy_zawiera_punkt(punkt)}")
    print(f"Czy odcinki się przecinają: {odcinek1.przecina(odcinek2)}")