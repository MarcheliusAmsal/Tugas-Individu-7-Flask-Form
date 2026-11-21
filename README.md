# Tugas Individu 7 - Flask Forms & WTForms

Aplikasi Web Pemesanan Kuliner Nusantara (**WarungOnline**) berbasis Python Flask, WTForms, CSRF Protection, dan Bootstrap 5.

## 🚀 Fitur Utama
- **Katalog & Keranjang Belanja Interaktif (`/keranjang`)**: Penyesuaian jumlah pesanan (+ / −), hapus item, dan perhitungan otomatis subtotal, ongkir, pajak, diskon.
- **Form Checkout & Validasi Data (`/`)**: Input lengkap customer details dan shipping details dengan validasi ketat (nama, email, nomor HP Indonesia, kode pos 5 digit, pilihan metode pembayaran) menggunakan Flask-WTF.
- **Dashboard Admin Real-time (`/admin`)**:
  - Penambahan menu baru dengan validasi tipe data numerik dan foto otomatis.
  - Rekap pesanan masuk secara real-time.
  - Manajemen daftar menu aktif.
- **Keamanan**: Dilengkapi dengan Token CSRF (`form.hidden_tag()`) pada seluruh form.

## 🛠️ Instalasi & Menjalankan Proyek

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/MarcheliusAmsal/Tugas-Individu-7-Flask-Form.git
   cd Tugas-Individu-7-Flask-Form
   ```

2. **Buat & aktifkan virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi Flask:**
   ```bash
   python app.py
   ```

5. **Akses melalui browser:**
   - Halaman Pemesanan / Checkout: `http://127.0.0.1:5000/`
   - Keranjang Belanja: `http://127.0.0.1:5000/keranjang`
   - Dashboard Admin: `http://127.0.0.1:5000/admin`
