import streamlit as st

# ----------------------------- CSS STYLING -----------------------------
st.set_page_config(page_title="Aplikasi Belanja", page_icon="🛒")

st.markdown("""
    <style>
    body {
        background-color: #fff0f5;
    }
    .judul-app {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #C71585;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .menu-box {
        background: linear-gradient(to right, #ffe4ec, #fcd2e2);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #FF69B4;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    .metric-box {
        background-color: #ffe9f0;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        text-align: center;
        color: #C71585;
    }
    .box-shadow {
        background-color: #fffafc;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- Kelas Barang -----------------------------
class Barang:
    def __init__(self, nama, harga, jumlah, kategori):
        self.nama = nama
        self.harga = harga
        self.jumlah = jumlah
        self.kategori = kategori
        self.is_beli = False

    def __str__(self):
        status = "✅" if self.is_beli else "❌"
        return f"{status} {self.nama} - Harga: Rp{self.harga:,}, Jumlah: {self.jumlah}, Kategori: {self.kategori}"

# ----------------------------- State Awal -----------------------------
if 'data_barang' not in st.session_state:
    st.session_state.data_barang = []

def hitung_total():
    total = sum(b.harga * b.jumlah for b in st.session_state.data_barang)
    return f"Rp{total:,}"

# ----------------------------- Tampilan Header -----------------------------
st.markdown('<div class="judul-app">🛒 Aplikasi Daftar Belanja Sederhana</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <div class="menu-box">
        <h4>📋 Menu:</h4>
        <ol>
        <li>📄 Lihat Daftar Barang</li>
        <li>➕ Tambah Barang</li>
        <li>✔️ Tandai Barang Sudah Dibeli</li>
        <li>✏️ Edit Barang</li>
        <li>🗑️ Hapus Barang</li>
        </ol>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-box">
            💰 <strong>Total Belanja:</strong><br>{hitung_total()}
        </div>
    """, unsafe_allow_html=True)

# ----------------------------- Input Menu -----------------------------
menu = st.text_input("Masukkan angka menu (1-5):")

# ----------------------------- Menu 1 -----------------------------
if menu == "1":
    st.subheader("📦 Daftar Barang")
    if st.session_state.data_barang:
        for i, barang in enumerate(st.session_state.data_barang):
            status = "✅" if barang.is_beli else "❌"
            warna = {
                "Primer": "🔴",
                "Sekunder": "🟠",
                "Tersier": "🟢"
            }[barang.kategori]
            st.markdown(f"""
                <div class="box-shadow">
                    <strong>{i+1}. {status} {barang.nama}</strong><br>
                    Harga: Rp{barang.harga:,} | Jumlah: {barang.jumlah} | Kategori: {warna} {barang.kategori}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Belum ada barang dalam daftar.")

# ----------------------------- Menu 2 -----------------------------
elif menu == "2":
    st.subheader("➕ Tambah Barang")
    with st.form(key='tambah_barang'):
        nama = st.text_input("Nama Barang")
        col1, col2 = st.columns(2)
        with col1:
            harga = st.number_input("Harga", min_value=0, step=1000)
        with col2:
            jumlah = st.number_input("Jumlah", min_value=1)
        kategori = st.selectbox("Kategori", ["Primer", "Sekunder", "Tersier"])
        
        if st.form_submit_button("Simpan Barang"):
            if nama and harga > 0 and jumlah > 0:
                barang = Barang(nama, harga, jumlah, kategori)
                st.session_state.data_barang.append(barang)
                st.success("Barang berhasil ditambahkan!")
            else:
                st.warning("Harap isi semua kolom dengan benar!")

# ----------------------------- Menu 3 -----------------------------
elif menu == "3":
    st.subheader("✔️ Tandai Barang Sudah Dibeli")
    if st.session_state.data_barang:
        for i, barang in enumerate(st.session_state.data_barang):
            if st.checkbox(f"{barang}", key=f"beli_{i}"):
                st.session_state.data_barang[i].is_beli = True
            else:
                st.session_state.data_barang[i].is_beli = False
        st.success("Perubahan status berhasil disimpan.")
    else:
        st.info("Belum ada barang dalam daftar.")

# ----------------------------- Menu 4 -----------------------------
elif menu == "4":
    st.subheader("✏️ Edit Barang")
    if st.session_state.data_barang:
        pilihan = st.selectbox(
            "Pilih barang yang akan diedit",
            [f"{i+1}. {b.nama}" for i, b in enumerate(st.session_state.data_barang)],
            key='edit_select'
        )
        
        if pilihan:
            index = int(pilihan.split('.')[0]) - 1
            barang = st.session_state.data_barang[index]
            
            with st.form(key='edit_form'):
                st.write("### Data Barang Saat Ini:")
                st.write(barang)
                st.write("### Masukkan Data Baru:")
                
                nama_baru = st.text_input("Nama Baru", value=barang.nama)
                col1, col2 = st.columns(2)
                with col1:
                    harga_baru = st.number_input("Harga Baru", value=barang.harga, min_value=0, step=1000)
                with col2:
                    jumlah_baru = st.number_input("Jumlah Baru", value=barang.jumlah, min_value=1)
                kategori_baru = st.selectbox(
                    "Kategori Baru", 
                    ["Primer", "Sekunder", "Tersier"],
                    index=["Primer", "Sekunder", "Tersier"].index(barang.kategori)
                )
                
                if st.form_submit_button("Simpan Perubahan"):
                    st.session_state.data_barang[index].nama = nama_baru
                    st.session_state.data_barang[index].harga = harga_baru
                    st.session_state.data_barang[index].jumlah = jumlah_baru
                    st.session_state.data_barang[index].kategori = kategori_baru
                    st.success("Data barang berhasil diperbarui!")
    else:
        st.info("Belum ada barang dalam daftar.")

# ----------------------------- Menu 5 -----------------------------
elif menu == "5":
    st.subheader("🗑️ Hapus Barang")
    if st.session_state.data_barang:
        pilihan = st.multiselect(
            "Pilih barang yang akan dihapus",
            [f"{i+1}. {b.nama}" for i, b in enumerate(st.session_state.data_barang)],
            key='hapus_select'
        )
        
        if pilihan and st.button("Hapus Barang Terpilih"):
            indices_to_delete = sorted([int(item.split('.')[0])-1 for item in pilihan], reverse=True)
            for index in indices_to_delete:
                if 0 <= index < len(st.session_state.data_barang):
                    del st.session_state.data_barang[index]
            st.success(f"{len(indices_to_delete)} barang berhasil dihapus!")
    else:
        st.info("Belum ada barang dalam daftar.")

# ----------------------------- Validasi Menu -----------------------------
elif menu != "":
    st.warning("Masukkan angka 1 - 5 sesuai menu.")

# ----------------------------- Footer -----------------------------
st.markdown("---")
st.markdown("<center><span style='color:gray;'>Dibuat dengan 💖 oleh Kamu | Powered by Streamlit</span></center>", unsafe_allow_html=True)
