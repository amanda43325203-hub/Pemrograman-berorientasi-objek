import geometri

def main():
    luas_persegi = geometri.hitung_luas_persegi(5)
    print(f"Luas persegi: {luas_persegi}")

    luas_persegi_panjang = geometri.hitung_luas_persegi_panjang(10, 5)
    print(f"Luas persegi panjang: {luas_persegi_panjang}")

    luas_lingkaran = geometri.hitung_luas_lingkaran(7)
    print(f"Luas lingkaran: {luas_lingkaran}")

if __name__ == "__main__":
    main()