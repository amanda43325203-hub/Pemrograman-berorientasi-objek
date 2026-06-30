import sqlite3
from konfigurasi import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mata_kuliah (
            id_matkul   INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_matkul TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id_tugas    INTEGER PRIMARY KEY AUTOINCREMENT,
            judul       TEXT    NOT NULL,
            deskripsi   TEXT,
            deadline    DATE    NOT NULL,
            prioritas   TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'Belum Selesai',
            nama_matkul TEXT    NOT NULL,
            FOREIGN KEY (nama_matkul) REFERENCES mata_kuliah(nama_matkul)
        )
    """)

    # Bagian insert otomatis matkul_default sudah dihapus total 
    # agar database kosong dan bisa kamu input mandiri lewat dashboard.

    conn.commit()
    conn.close()


def tambah_matkul(nama: str):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO mata_kuliah (nama_matkul) VALUES (?)", (nama,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_semua_matkul():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM mata_kuliah ORDER BY nama_matkul").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def hapus_matkul(id_matkul: int):
    conn = get_connection()
    conn.execute("DELETE FROM mata_kuliah WHERE id_matkul = ?", (id_matkul,))
    conn.commit()
    conn.close()


def tambah_tugas(t):
    conn = get_connection()
    conn.execute(
        """INSERT INTO tugas (judul, deskripsi, deadline, prioritas, status, nama_matkul)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (t.judul, t.deskripsi, str(t.deadline), t.prioritas, t.status, t.nama_matkul)
    )
    conn.commit()
    conn.close()


def get_semua_tugas():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tugas ORDER BY deadline ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def hapus_tugas(id_tugas: int):
    conn = get_connection()
    conn.execute("DELETE FROM tugas WHERE id_tugas = ?", (id_tugas,))
    conn.commit()
    conn.close()


def update_status_tugas(id_tugas: int, status_baru: str):
    conn = get_connection()
    conn.execute("UPDATE tugas SET status = ? WHERE id_tugas = ?", (status_baru, id_tugas))
    conn.commit()
    conn.close()