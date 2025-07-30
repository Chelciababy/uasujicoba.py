import streamlit as st

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

if 'data_barang' not in st.session_state:
    st.session_state.data_barang = []

def hitung_total():
    total = sum(b.harga * b.jumlah for b in st.session_state.data_barang)
    return f"Rp{total:,}"

st.markdown("<h1 style='color:#ff69b4;'>🛒 Aplikasi Daftar Belanja Sederhana</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h3 style='color:#ff8acb;'>📋 Menu:</h3>", unsafe_allow_html=True)
with col2:
    st.metric("Total Belanja", hitung_total())

st.markdown("**1. Lihat Daftar Barang**")
st.markdown("**2. Tambah Barang**")
st.markdown("**3. Tandai Barang Sudah Dibeli**")
st.markdown("**4. Edit Barang**")
st.markdown("**5. Hapus Barang**")

menu = st.text_input("Masukkan angka menu (1-5):")

if menu == "1":
    st.markdown("<h4 style='color:#ff8acb;'>📄 Daftar Barang</h4>", unsafe_allow_html=True)
    if st.session_state.data_barang:
        for i, barang in enumerate(st.session_state.data_barang):
            st.write(f"{i+1}. {barang}")
    else:
        st.info("Belum ada barang dalam daftar.")
        
elif menu == "2":
    st.markdown("<h4 style='color:#ff8acb;'>➕ Tambah Barang</h4>", unsafe_allow_html=True)
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

elif menu == "3":
    st.markdown("<h4 style='color:#ff8acb;'>✔ Tandai Barang Sudah Dibeli</h4>", unsafe_allow_html=True)
    if st.session_state.data_barang:
        for i, barang in enumerate(st.session_state.data_barang):
            if st.checkbox(f"{barang}", key=f"beli_{i}"):
                st.session_state.data_barang[i].is_beli = True
            else:
                st.session_state.data_barang[i].is_beli = False
        st.success("Perubahan status berhasil disimpan.")
    else:
        st.info("Belum ada barang dalam daftar.")

elif menu == "4":
    st.markdown("<h4 style='color:#ff8acb;'>✏ Edit Barang</h4>", unsafe_allow_html=True)
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
                st.markdown("**Data Barang Saat Ini:**")
                st.write(barang)
                st.markdown("**Masukkan Data Baru:**")
                
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

elif menu == "5":
    st.markdown("<h4 style='color:#ff8acb;'>🗑 Hapus Barang</h4>", unsafe_allow_html=True)
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

elif menu != "":
    st.warning("Masukkan angka 1 - 5 sesuai menu.")
