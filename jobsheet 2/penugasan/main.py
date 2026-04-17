import penjualan

def main():
    # Membuat objek
    hp1 = penjualan.HP("Samsung", 3000000, 10)
    hp2 = penjualan.HP("Xiaomi", 2500000, 5)

    print("=== DAFTAR HP ===")
    hp1.tampilkan_info()
    print()
    hp2.tampilkan_info()

    print("\n=== TRANSAKSI ===")
    hp1.beli(2)
    hp2.beli(3)

if __name__ == "__main__":
    main()