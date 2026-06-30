from model    import Tugas, MataKuliah
from database import (
    tambah_tugas as db_tambah_tugas,
    get_semua_tugas,
    hapus_tugas as db_hapus_tugas,
    update_status_tugas,
    tambah_matkul as db_tambah_matkul,
    get_semua_matkul,
    hapus_matkul as db_hapus_matkul,
)


class ManajerTugas:
    def tambah_mata_kuliah(self, nama: str) -> bool:
        return db_tambah_matkul(nama.strip())

    def daftar_mata_kuliah(self):
        return get_semua_matkul()

    def hapus_mata_kuliah(self, id_matkul: int):
        db_hapus_matkul(id_matkul)

    def tambah_tugas(self, tugas: Tugas):
        db_tambah_tugas(tugas)

    def daftar_tugas(self, filter_status: str = "Semua"):
        semua = get_semua_tugas()
        if filter_status == "Semua":
            return semua
        return [t for t in semua if t["status"] == filter_status]

    def hapus_tugas(self, id_tugas: int):
        db_hapus_tugas(id_tugas)

    def ubah_status(self, id_tugas: int, status_baru: str):
        update_status_tugas(id_tugas, status_baru)

    def hitung_statistik(self):
        semua = get_semua_tugas()
        total   = len(semua)
        selesai = sum(1 for t in semua if t["status"] == "Selesai")
        proses  = sum(1 for t in semua if t["status"] == "Sedang Dikerjakan")
        belum   = sum(1 for t in semua if t["status"] == "Belum Selesai")
        pct     = round((selesai / total) * 100) if total else 0
        return {"total": total, "selesai": selesai, "proses": proses, "belum": belum, "pct": pct}