class HP:
    def __init__(self, merk, harga, stok):
        self.merk = merk
        self.harga = harga
        self.stok = stok

    def tampilkan_info(self):
        print("Merk HP   :", self.merk)
        print("Harga     : Rp", self.harga)
        print("Stok      :", self.stok)

    def beli(self, jumlah):
        if jumlah <= self.stok:
            self.stok -= jumlah
            total = self.harga * jumlah
            print(f"Berhasil membeli {jumlah} unit {self.merk}")
            print(f"Total bayar: Rp {total}")
        else:
            print("Stok tidak mencukupi!")