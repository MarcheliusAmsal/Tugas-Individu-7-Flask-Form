from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange, Optional

class PemesananForm(FlaskForm):
    # Customer Details
    nama_depan = StringField("Nama Depan (First Name) *", validators=[
        DataRequired(message="Nama depan wajib diisi"),
        Length(min=2, max=50, message="Nama depan minimal 2 karakter")
    ])
    nama_belakang = StringField("Nama Belakang (Last Name) *", validators=[
        DataRequired(message="Nama belakang wajib diisi"),
        Length(min=2, max=50, message="Nama belakang minimal 2 karakter")
    ])
    email = StringField("Email *", validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid (contoh: user@gmail.com)")
    ])
    no_hp = StringField("Nomor HP (Phone Number) *", validators=[
        DataRequired(message="Nomor HP wajib diisi"),
        Regexp(r"^(08|\+628)\d{8,12}$", message="Nomor HP harus diawali 08 atau +628 (10–14 digit angka)")
    ])
    
    # Shipping Details
    alamat = StringField("Alamat Pengiriman (Street Address) *", validators=[
        DataRequired(message="Alamat pengiriman wajib diisi"),
        Length(min=8, max=255, message="Alamat pengiriman harus jelas dan lengkap (minimal 8 karakter)")
    ])
    kode_pos = StringField("Kode Pos (Postal Code) *", validators=[
        DataRequired(message="Kode pos wajib diisi"),
        Regexp(r"^\d{5}$", message="Kode pos harus 5 digit angka")
    ])
    kota = StringField("Kota (City) *", validators=[
        DataRequired(message="Nama kota wajib diisi"),
        Length(min=3, max=50, message="Nama kota minimal 3 karakter")
    ])
    
    # Payment Method
    metode_pembayaran = SelectField("Metode Pembayaran *", choices=[
        ("COD", "Bayar di Tempat (COD)"),
        ("Transfer Bank", "Transfer Bank (BCA / Mandiri / BRI)"),
        ("E-Wallet", "E-Wallet (Dana / GoPay / ShopeePay)")
    ])
    
    submit = SubmitField("Kirim Pesanan (Check Out)")


# Form 2: Dashboard Admin (Tambah Menu Baru)
class TambahProdukForm(FlaskForm):
    nama = StringField("Nama Menu *", validators=[
        DataRequired(message="Nama menu wajib diisi"),
        Length(min=3, max=80, message="Nama menu minimal 3 karakter")
    ])
    kategori = SelectField("Kategori *", choices=[
        ("Makanan", "Makanan"),
        ("Minuman", "Minuman"),
        ("Paket Box", "Paket Box")
    ])
    harga = IntegerField("Harga Satuan (Rp) *", validators=[
        DataRequired(message="Harga wajib diisi dengan nominal angka"),
        NumberRange(min=1000, message="Harga minimal Rp 1.000")
    ])
    gambar = StringField("URL Gambar Menu (Opsional)", validators=[
        Optional(),
        Length(max=500, message="URL gambar maksimal 500 karakter")
    ])
    submit = SubmitField("Simpan Menu Baru")
