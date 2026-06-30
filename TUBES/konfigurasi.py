import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'tugas_kuliah.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

PRIORITAS_LIST = ["Rendah", "Sedang", "Tinggi"]
STATUS_LIST    = ["Belum Selesai", "Sedang Dikerjakan", "Selesai"]