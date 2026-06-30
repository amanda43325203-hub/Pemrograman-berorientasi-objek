from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class MataKuliah:
    nama_matkul: str
    id_matkul:   Optional[int] = field(default=None)


@dataclass
class Tugas:
    judul:       str
    deskripsi:   str
    deadline:    date
    prioritas:   str
    status:      str
    nama_matkul: str
    id_tugas:    Optional[int] = field(default=None)