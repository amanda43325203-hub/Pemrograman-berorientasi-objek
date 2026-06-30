import streamlit as st
from datetime import date, datetime

from database      import setup_database
from manajer_tugas import ManajerTugas
from model         import Tugas
from konfigurasi   import PRIORITAS_LIST, STATUS_LIST

setup_database()
manajer = ManajerTugas()

st.set_page_config(
    page_title="TaskMate — Manajemen Tugas",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SELEKSI DAN REFORMASI STYLE (MOCKUP PREMIUM DESIGN) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght=300;400;500;600&family=Space+Grotesk:wght=500;600;700&display=swap');

:root {
    /* Background utama diubah menjadi pink soft sesuai request */
    --bg: #fcedf2; 
    --surface: #ffffff; 
    --surface2: #fff0f3; 
    --surface3: #ffe3e8;
    --border: #f5d6dc; 
    --border2: #ffccd5;
    --text: #4a3538; 
    --text2: #8a686d; 
    --text3: #b08d93;
    --accent: #ff85a2; 
    --accent2: #ff5c8a; 
    --accent-bg: #fff0f3;
    --green: #49a078; 
    --green-bg: #e8f5e9;
    --amber: #e09f3e; 
    --amber-bg: #fff3e0;
    --radius: 14px; 
    --radius-lg: 18px;
    --shadow: 0 6px 18px rgba(234, 182, 197, 0.4);
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1100px; }

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem !important; }
section[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; flex-direction: column !important; }

section[data-testid="stSidebar"] .stRadio label p {
    color: var(--text) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    display: flex !important; align-items: center !important; gap: 10px !important;
    padding: 10px 14px !important; border-radius: 10px !important; cursor: pointer !important;
    color: var(--text) !important; font-size: 14px !important; font-weight: 500 !important;
    border: 1px solid transparent !important; transition: all 0.18s !important; background: transparent !important;
}
section[data-testid="stSidebar"] .stRadio label:hover { background: var(--surface2) !important; }
section[data-testid="stSidebar"] .stRadio label:hover p { color: var(--accent2) !important; }
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }

h1 { font-family: 'Space Grotesk', sans-serif !important; font-size: 26px !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.5px !important; }
h2 { font-family: 'Space Grotesk', sans-serif !important; font-size: 18px !important; font-weight: 600 !important; color: var(--text) !important; margin-bottom: 0.8rem !important; margin-top: 1.5rem !important; }

/* Kotak Form & Input diubah menjadi Putih Bersih Kontras dengan Shadow */
div[data-testid="stForm"] {
    background: var(--surface) !important;
    border: none !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem !important;
    box-shadow: var(--shadow) !important;
}

input[type="text"], input[type="number"], input[type="date"], textarea,
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
    background: #fafafa !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 14px !important;
    padding: 10px 14px !important;
}
input:focus, textarea:focus { border-color: var(--accent) !important; background: var(--surface) !important; box-shadow: 0 0 0 3px rgba(255,133,162,0.15) !important; }

.stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label, .stNumberInput label {
    font-size: 12px !important; font-weight: 600 !important; color: var(--text2) !important;
    text-transform: uppercase !important; letter-spacing: 0.8px !important; margin-bottom: 6px !important;
}

.stSelectbox > div > div {
    background: #fafafa !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; color: var(--text) !important; font-size: 14px !important;
}
.stSelectbox svg { fill: var(--text2) !important; }

/* Buttons styling */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important; font-size: 14px !important;
    font-weight: 600 !important; border-radius: var(--radius) !important;
    padding: 0.6rem 1.5rem !important; transition: all 0.2s !important; border: none !important;
}
.stButton > button[kind="primary"], .stButton > button:not([kind]) {
    background: var(--accent) !important; color: #fff !important;
}
.stButton > button[kind="primary"]:hover, .stButton > button:not([kind]):hover {
    background: var(--accent2) !important; transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,92,138,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface) !important; color: var(--text2) !important; border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important; color: var(--accent) !important; background: var(--surface2) !important;
}

/* Metrik Kotak-Kotak Putih Melayang */
[data-testid="stMetric"] {
    background: var(--surface) !important; 
    border: none !important;
    border-radius: var(--radius-lg) !important; 
    padding: 1.2rem 1.5rem !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stMetric"] label { font-size: 12px !important; font-weight: 600 !important; color: var(--text3) !important; text-transform: uppercase !important; letter-spacing: 0.8px !important; }
[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif !important; font-size: 30px !important; font-weight: 700 !important; color: var(--text) !important; }

.stSuccess { background: var(--green-bg) !important; border: 1px solid #c8e6c9 !important; border-radius: var(--radius) !important; color: var(--green) !important; }
.stError   { background: #ffe5ec !important; border: 1px solid #ffccd5 !important; border-radius: var(--radius) !important; color: #d90429 !important; }
.stWarning { background: var(--amber-bg) !important; border: 1px solid #ffe0b2 !important; border-radius: var(--radius) !important; color: var(--amber) !important; }

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; opacity: 0.5; }

/* Custom Badge Tags */
.tag { display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 6px; }
.tag-tinggi  { background:#ffe5ec; color:#d90429; }
.tag-sedang  { background:#fff3e0; color:#e09f3e; }
.tag-rendah  { background:#e8f5e9; color:#49a078; }
.tag-selesai { background:#e8f5e9; color:#49a078; }
.tag-proses  { background:#e3f2fd; color:#4a90e2; }
.tag-belum   { background:#fff0f3; color:#b08d93; }
.tag-matkul  { background:#fff0f3; color:#ff5c8a; border:1px solid #ffccd5; }

/* Task Card Putih Premium dengan Shadow */
.task-card { background:#ffffff; border: none; border-radius:16px; padding:1.5rem; margin-bottom:14px; box-shadow: var(--shadow); }
.task-card.done { opacity:0.65; background:#fafafa; box-shadow: none; border: 1px dashed var(--border); }
.task-title { font-size:16px; font-weight:600; color:#4a3538; margin-bottom:4px; }
.task-card.done .task-title { text-decoration:line-through; color:#b08d93; }
.task-meta { display:flex; gap:8px; flex-wrap:wrap; align-items:center; margin-top:8px; }
.deadline { font-size:12px; color:#8a686d; font-weight:500; }
.deadline.overdue { color:#d90429; font-weight:600; }
.task-desc { font-size:13px; color:#8a686d; margin-top:10px; padding-top:8px; border-top:1px dashed #f5d6dc; }

/* Sidebar Component Styling */
.sb-logo { display:flex; align-items:center; gap:12px; padding:0 4px 1.5rem; border-bottom:1px solid #f5d6dc; margin-bottom:1.5rem; }
.sb-logo-icon { width:38px; height:38px; background:#fff0f3; border:1px solid #ffccd5; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; }
.sb-logo-text { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:16px; color:#4a3538; }
.sb-logo-sub { font-size:11px; color:#8a686d; }

.sb-stats { background:#ffffff; border:none; border-radius:14px; padding:1.2rem; margin-top:2rem; margin-bottom:1.5rem; box-shadow: 0 4px 12px rgba(234, 182, 197, 0.25); }
.sb-stats-title { font-size:11px; color:#b08d93; text-transform:uppercase; letter-spacing:1px; font-weight:600; margin-bottom:10px; }
.sb-stat-row { display:flex; justify-content:space-between; margin-bottom:6px; font-size:13px; }
.sb-stat-lbl { color:#8a686d; }
.sb-stat-val { font-family:'Space Grotesk',sans-serif; font-weight:600; }
.v-green { color:#49a078; } .v-amber { color:#e09f3e; } .v-red { color:#d90429; }

.prog-wrap { background:#ffe3e8; border-radius:4px; height:6px; overflow:hidden; margin-top:8px; }
.prog-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#ff85a2,#ff5c8a); }

.page-sub { font-size:14px; color:#8a686d; margin-top:-0.5rem; margin-bottom:1.5rem; }
.empty-state { text-align:center; padding:3rem 1rem; color:#b08d93; font-size:14px; }

/* CSS Banner Ungu Gradasi Premium Sesuai Contoh Gambar Screenshot */
.premium-header-banner {
    background: linear-gradient(135deg, #a87ffb 0%, #ca86ef 50%, #f693cb 100%);
    border-radius: 20px;
    padding: 2.5rem 2.5rem;
    color: white !important;
    margin-bottom: 2rem;
    position: relative;
    box-shadow: 0 10px 30px rgba(168, 127, 251, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.banner-text-side {
    display: flex;
    flex-direction: column;
}
.banner-date {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(255, 255, 255, 0.85);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.banner-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    color: white !important;
    line-height: 1.2 !important;
}
.banner-subtitle {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.9);
    margin-top: 8px;
    font-weight: 400;
}
.banner-badge-btn {
    background: #ffffff;
    color: #a87ffb;
    font-weight: 600;
    font-size: 13px;
    padding: 10px 22px;
    border-radius: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 6px;
}
</style>
""", unsafe_allow_html=True)


def badge_prioritas(p):
    cls = {"Tinggi":"tag-tinggi","Sedang":"tag-sedang","Rendah":"tag-rendah"}.get(p,"tag-rendah")
    return f'<span class="tag {cls}">{p}</span>'

def badge_status(s):
    cls = {"Selesai":"tag-selesai","Sedang Dikerjakan":"tag-proses","Belum Selesai":"tag-belum"}.get(s,"tag-belum")
    return f'<span class="tag {cls}">{s}</span>'

def badge_matkul(m):
    return f'<span class="tag tag-matkul">{m}</span>'


# Helper untuk mendapatkan format tanggal Indonesia di banner
def dapatkan_hari_ini():
    hari_ini = datetime.now().strftime("%A, %d %B %Y").upper()
    for eng, ind in [("MONDAY","SENIN"),("TUESDAY","SELASA"),("WEDNESDAY","RABU"),("THURSDAY","KAMIS"),("FRIDAY","JUMAT"),("SATURDAY","SABTU"),("SUNDAY","MINGGU")]:
        hari_ini = hari_ini.replace(eng, ind)
    return hari_ini


# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">📋</div>
        <div>
            <div class="sb-logo-text">TaskMate</div>
            <div class="sb-logo-sub">Manajemen Tugas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["📚   Tambah Mata Kuliah", "➕   Tambah Tugas", "📋   Daftar Tugas"],
        label_visibility="collapsed",
    )

    stat = manajer.hitung_statistik()
    pct  = stat["pct"]
    st.markdown(f"""
    <div class="sb-stats">
        <div class="sb-stats-title">Ringkasan</div>
        <div class="sb-stat-row"><span class="sb-stat-lbl">Total Tugas</span><span class="sb-stat-val" style="color:#4a3538">{stat['total']}</span></div>
        <div class="sb-stat-row"><span class="sb-stat-lbl">Selesai</span><span class="sb-stat-val v-green">{stat['selesai']}</span></div>
        <div class="sb-stat-row"><span class="sb-stat-lbl">Sedang Dikerjakan</span><span class="sb-stat-val v-amber">{stat['proses']}</span></div>
        <div class="sb-stat-row"><span class="sb-stat-lbl">Belum Selesai</span><span class="sb-stat-val v-red">{stat['belum']}</span></div>
        <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
        <div style="font-size:11px;color:#8a686d;margin-top:5px;text-align:right">{pct}% selesai</div>
    </div>
    """, unsafe_allow_html=True)

    # TOMBOL CLEAR CACHE AMAN & TETAP BERTAHAN DI BAWAH SIDEBAR
    if st.button("🔄 Clear Cache & Refresh Data", use_container_width=True, type="secondary"):
        st.cache_data.clear()
        st.rerun()


# ── HALAMAN: Tambah Mata Kuliah (SEKARANG DENGAN BANNER GRADASI PREMIUM) ──
if menu == "📚   Tambah Mata Kuliah":
    # Menambahkan Banner Ungu Gradasi Premium Sesuai Request
    st.markdown(f"""
    <div class="premium-header-banner">
        <div class="banner-text-side">
            <div class="banner-date">✨ {dapatkan_hari_ini()}</div>
            <div class="banner-title">Mata Kuliah<br>Semester Dua 📖</div>
            <div class="banner-subtitle">Susun daftar mata kuliahmu di sini agar manajemen tugas menjadi lebih rapi dan terstruktur 🌸</div>
        </div>
        <div class="banner-badge-btn">
            <span>📚</span> Kuliah
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_matkul", clear_on_submit=True):
        st.markdown("## Tambah Baru")
        nama = st.text_input("Nama Mata Kuliah", placeholder="Contoh: Pemrograman Berorientasi Objek")
        submitted = st.form_submit_button("➕ Tambah Mata Kuliah", use_container_width=True)
        if submitted:
            if not nama.strip():
                st.error("⚠️   Nama mata kuliah tidak boleh kosong!")
            else:
                ok = manajer.tambah_mata_kuliah(nama)
                if ok:
                    st.success(f"✅ '{nama}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning(f"⚠️   '{nama}' sudah terdaftar.")

    st.markdown("## Daftar Mata Kuliah")
    daftar = manajer.daftar_mata_kuliah()
    if not daftar:
        st.markdown('<div class="empty-state">📭 Belum ada mata kuliah. Tambahkan dulu!</div>', unsafe_allow_html=True)
    else:
        for mk in daftar:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(
                    f'<div style="background:#ffffff; border:none; box-shadow: 0 4px 12px rgba(234, 182, 197, 0.25); border-radius:10px;'
                    f'padding:14px 18px; display:flex; align-items:center; gap:10px;">'
                    f'<span style="color:#ff5c8a; font-size:16px">📖</span>'
                    f'<span style="font-size:14px; font-weight:500; color:#4a3538">{mk["nama_matkul"]}</span>'
                    f'</div>', unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_mk_{mk['id_matkul']}", help="Hapus", use_container_width=True):
                    manajer.hapus_mata_kuliah(mk["id_matkul"])
                    st.rerun()


# ── HALAMAN: Tambah Tugas ────────────────────────────────────
elif menu == "➕   Tambah Tugas":
    st.markdown(f"""
    <div class="premium-header-banner">
        <div class="banner-text-side">
            <div class="banner-date">✨ {dapatkan_hari_ini()}</div>
            <div class="banner-title">Dashboard Tugas<br>Kuliah Ku 🌸</div>
            <div class="banner-subtitle">Konsisten itu kunci. Sedikit demi sedikit, lama-lama menjadi bukit 🌷</div>
        </div>
        <div class="banner-badge-btn">
            <span>+</span> Tambah Tugas
        </div>
    </div>
    """, unsafe_allow_html=True)

    daftar_mk = manajer.daftar_mata_kuliah()
    nama_mk   = ["-- Pilih Mata Kuliah --"] + [mk["nama_matkul"] for mk in daftar_mk]

    if len(nama_mk) <= 1:
        st.warning("⚠️   Belum ada mata kuliah. Silakan tambahkan mata kuliah terlebih dahulu!")
    else:
        with st.form("form_tugas", clear_on_submit=True):
            judul     = st.text_input("Judul Tugas", placeholder="Masukkan judul tugas...")
            deskripsi = st.text_area("Deskripsi", placeholder="Deskripsi tugas (opsional)...", height=100)
            col1, col2 = st.columns(2)
            with col1:
                deadline  = st.date_input("Deadline", value=date.today())
                prioritas = st.selectbox("Prioritas", PRIORITAS_LIST, index=1)
            with col2:
                status = st.selectbox("Status", STATUS_LIST)
                matkul = st.selectbox("Mata Kuliah", nama_mk, index=0)

            submitted = st.form_submit_button("✅ Tambah Tugas", use_container_width=True)
            if submitted:
                if not judul.strip():
                    st.error("⚠️   Judul tugas tidak boleh kosong!")
                elif matkul == "-- Pilih Mata Kuliah --":
                    st.error("⚠️   Silakan pilih Mata Kuliah yang valid!")
                else:
                    tugas = Tugas(
                        judul=judul.strip(), deskripsi=deskripsi.strip(),
                        deadline=deadline, prioritas=prioritas,
                        status=status, nama_matkul=matkul,
                    )
                    manajer.tambah_tugas(tugas)
                    st.success("✅ Tugas berhasil ditambahkan!")
                    st.rerun()


# ── HALAMAN: Daftar Tugas ────────────────────────────────────
elif menu == "📋   Daftar Tugas":
    st.markdown("# 📋 Daftar Tugas")
    st.markdown('<p class="page-sub">Semua tugasmu dalam satu tempat</p>', unsafe_allow_html=True)

    stat = manajer.hitung_statistik()
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📦 Total Tugas", stat["total"])
    with c2: st.metric("✅ Selesai", stat["selesai"])
    with c3: st.metric("⏳ Pending", stat["proses"])
    with c4: st.metric("❌ Belum Selesai", stat["belum"])

    st.markdown("---")

    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        filter_status = st.selectbox("Filter Status", ["Semua"] + STATUS_LIST, label_visibility="collapsed")
    with col_f2:
        filter_prio = st.selectbox("Filter Prioritas", ["Semua Prioritas"] + PRIORITAS_LIST, label_visibility="collapsed")
    with col_f3:
        filter_mk_list = ["Semua Matkul"] + [mk["nama_matkul"] for mk in manajer.daftar_mata_kuliah()]
        filter_mk = st.selectbox("Filter Matkul", filter_mk_list, label_visibility="collapsed")

    semua_tugas = manajer.daftar_tugas(filter_status)
    if filter_prio != "Semua Prioritas":
        semua_tugas = [t for t in semua_tugas if t["prioritas"] == filter_prio]
    if filter_mk != "Semua Matkul":
        semua_tugas = [t for t in semua_tugas if t["nama_matkul"] == filter_mk]

    urut = {"Tinggi": 0, "Sedang": 1, "Rendah": 2}
    semua_tugas.sort(key=lambda x: urut.get(x["prioritas"], 9))

    st.markdown(f'<p class="page-sub">{len(semua_tugas)} tugas ditemukan</p>', unsafe_allow_html=True)

    if not semua_tugas:
        st.markdown('<div class="empty-state">📭 Tidak ada tugas yang sesuai filter.</div>', unsafe_allow_html=True)
    else:
        for t in semua_tugas:
            done_class = "done" if t["status"] == "Selesai" else ""
            dl_html = ""
            if t["deadline"]:
                try:
                    dl_date = datetime.strptime(str(t["deadline"]), "%Y-%m-%d").date()
                    diff    = (dl_date - date.today()).days
                    dl_str  = dl_date.strftime("%d %b %Y")
                    oc  = "overdue" if diff < 0 else ""
                    pfx = "⚠️ Lewat: " if diff < 0 else "📅 "
                    dl_html = f'<span class="deadline {oc}">{pfx}{dl_str}</span>'
                except Exception:
                    pass

            desc_html = f'<div class="task-desc">{t["deskripsi"]}</div>' if t.get("deskripsi") else ""

            st.markdown(f"""
            <div class="task-card {done_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="task-title">📌 {t['judul']}</div>
                    <div>{dl_html}</div>
                </div>
                <div class="task-meta">
                    {badge_matkul(t['nama_matkul'])}
                    {badge_prioritas(t['prioritas'])}
                    {badge_status(t['status'])}
                </div>
                {desc_html}
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_b:
                if st.button("🔄 Ubah Status", key=f"ubah_{t['id_tugas']}", use_container_width=True):
                    idx = STATUS_LIST.index(t["status"])
                    manajer.ubah_status(t["id_tugas"], STATUS_LIST[(idx + 1) % len(STATUS_LIST)])
                    st.rerun()
            with col_c:
                if st.button("🗑️ Hapus", key=f"hapus_{t['id_tugas']}", use_container_width=True):
                    manajer.hapus_tugas(t["id_tugas"])
                    st.rerun()