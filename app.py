from flask import Flask, render_template, redirect, url_for, flash, request
from forms import PemesananForm, TambahProdukForm
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "warung-online-token-secret-2026"

# Database simulasi pesanan masuk (tercatat di Dashboard Admin)
PESANAN_DB = []

# Database simulasi keranjang belanja & menu aktif
KERANJANG_DB = [
    {
        "id": 1,
        "nama": "Nasi Goreng Spesial Box",
        "kategori": "Paket Box",
        "deskripsi": "Nasi goreng spesial disajikan dalam box higienis dengan telur mata sapi, ayam suwir, acar, dan kerupuk gurih",
        "harga": 20000,
        "qty": 1,
        "gambar": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=500&q=80"
    },
    {
        "id": 2,
        "nama": "Mie Goreng Spesial Box",
        "kategori": "Paket Box",
        "deskripsi": "Mie goreng kecap manis khas nusantara lengkap dengan potongan bakso, telur, sayuran segar, dan taburan bawang goreng",
        "harga": 18000,
        "qty": 2,
        "gambar": "https://images.unsplash.com/photo-1612927601601-6638404737ce?auto=format&fit=crop&w=500&q=80"
    }
]

def hitung_ringkasan():
    """Menghitung ringkasan biaya secara aman dengan tipe data numerik."""
    if not KERANJANG_DB:
        return 0, 0, 0, 0, 0

    subtotal = sum(int(item["harga"]) * int(item["qty"]) for item in KERANJANG_DB)
    ongkir = 8000
    pajak = 2000
    diskon = 5000 if subtotal >= 20000 else 0
    total = max(0, subtotal + ongkir + pajak - diskon)
    return subtotal, ongkir, pajak, diskon, total

@app.context_processor
def inject_cart_count():
    """Menyediakan jumlah total porsi item keranjang ke seluruh template."""
    total_qty = sum(int(item["qty"]) for item in KERANJANG_DB)
    return {
        "total_cart_items": total_qty,
        "total_pesanan_masuk": len(PESANAN_DB)
    }

@app.route("/", methods=["GET", "POST"])
def pemesanan():
    form = PemesananForm()
    subtotal, ongkir, pajak, diskon, total = hitung_ringkasan()

    if form.validate_on_submit():
        if not KERANJANG_DB:
            flash("Keranjang belanja masih kosong. Silakan pilih menu terlebih dahulu sebelum melakukan checkout.", "warning")
            return redirect(url_for("keranjang"))

        # 1. Catat nama menu yang dipesan beserta porsi dan rincian harga
        daftar_menu_pesanan = []
        for item in KERANJANG_DB:
            daftar_menu_pesanan.append({
                "nama": item["nama"],
                "qty": item["qty"],
                "harga": int(item["harga"]),
                "subtotal": int(item["harga"]) * int(item["qty"])
            })

        rincian_teks = ", ".join([f"{item['nama']} ({item['qty']}x)" for item in KERANJANG_DB])
        waktu_sekarang = datetime.now().strftime("%d %b %Y, %H:%M WIB")

        # 2. Rekam seluruh data pemesan & menu yang dipesan ke Dashboard Admin (PESANAN_DB)
        pesanan_baru = {
            "id": f"ORD-{len(PESANAN_DB) + 1001}",
            "waktu": waktu_sekarang,
            "nama": f"{form.nama_depan.data.strip()} {form.nama_belakang.data.strip()}",
            "email": form.email.data.strip(),
            "no_hp": form.no_hp.data.strip(),
            "alamat": f"{form.alamat.data.strip()}, {form.kota.data.strip()} (Kode Pos: {form.kode_pos.data.strip()})",
            "pembayaran": form.metode_pembayaran.data,
            "items": rincian_teks,
            "daftar_menu": daftar_menu_pesanan,
            "total_bayar": total,
            "status": "Tercatat di Admin"
        }
        
        # Simpan pesanan baru di urutan paling atas
        PESANAN_DB.insert(0, pesanan_baru)

        flash(
            f"Pesanan atas nama {pesanan_baru['nama']} berhasil dibuat. Data formulir dan menu yang dipesan ({rincian_teks}) telah dikirim dan dicatat di Dashboard Admin.",
            "success"
        )
        return redirect(url_for("admin_produk"))

    return render_template(
        "pemesanan.html",
        form=form,
        menu=KERANJANG_DB,
        subtotal=subtotal,
        ongkir=ongkir,
        pajak=pajak,
        diskon=diskon,
        total=total
    )

@app.route("/keranjang")
def keranjang():
    subtotal, ongkir, pajak, diskon, total = hitung_ringkasan()
    return render_template(
        "keranjang.html",
        menu=KERANJANG_DB,
        subtotal=subtotal,
        ongkir=ongkir,
        pajak=pajak,
        diskon=diskon,
        total=total
    )

@app.route("/keranjang/tambah/<int:item_id>")
def tambah_qty(item_id):
    for item in KERANJANG_DB:
        if item["id"] == item_id:
            item["qty"] += 1
            flash(f"Porsi '{item['nama']}' ditambah menjadi {item['qty']}x.", "info")
            break
    referrer = request.referrer
    if referrer and "keranjang" in referrer:
        return redirect(url_for("keranjang"))
    return redirect(url_for("pemesanan"))

@app.route("/keranjang/kurang/<int:item_id>")
def kurang_qty(item_id):
    for item in list(KERANJANG_DB):
        if item["id"] == item_id:
            if item["qty"] > 1:
                item["qty"] -= 1
                flash(f"Porsi '{item['nama']}' dikurangi menjadi {item['qty']}x.", "info")
            else:
                KERANJANG_DB.remove(item)
                flash(f"Menu '{item['nama']}' telah dihapus dari keranjang.", "warning")
            break
    referrer = request.referrer
    if referrer and "keranjang" in referrer:
        return redirect(url_for("keranjang"))
    return redirect(url_for("pemesanan"))

@app.route("/keranjang/hapus/<int:item_id>")
def hapus_item(item_id):
    for item in list(KERANJANG_DB):
        if item["id"] == item_id:
            KERANJANG_DB.remove(item)
            flash(f"Menu '{item['nama']}' berhasil dihapus dari keranjang.", "warning")
            break
    referrer = request.referrer
    if referrer and "keranjang" in referrer:
        return redirect(url_for("keranjang"))
    return redirect(url_for("pemesanan"))

@app.route("/admin", methods=["GET", "POST"])
def admin_produk():
    form = TambahProdukForm()
    if form.validate_on_submit():
        gambar_input = form.gambar.data.strip() if form.gambar.data and form.gambar.data.strip() else ""
        if not gambar_input:
            if form.kategori.data == "Minuman":
                gambar_input = "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=80"
            elif form.kategori.data == "Paket Box":
                gambar_input = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80"
            else:
                gambar_input = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80"

        next_id = max([item["id"] for item in KERANJANG_DB], default=0) + 1
        harga_int = int(form.harga.data)

        menu_baru = {
            "id": next_id,
            "nama": form.nama.data.strip(),
            "kategori": form.kategori.data,
            "deskripsi": f"Menu {form.kategori.data.lower()} lezat yang disiapkan spesial untuk pelanggan setia.",
            "harga": harga_int,
            "qty": 1,
            "gambar": gambar_input
        }
        KERANJANG_DB.append(menu_baru)
        flash(f"Menu baru '{form.nama.data}' (Rp {harga_int:,.0f}) berhasil dicatat dan masuk ke sistem.", "success")
        return redirect(url_for("admin_produk"))

    return render_template(
        "admin_produk.html",
        form=form,
        pesanan=PESANAN_DB,
        menu=KERANJANG_DB
    )

@app.route("/admin/hapus-menu/<int:item_id>")
def admin_hapus_menu(item_id):
    for item in list(KERANJANG_DB):
        if item["id"] == item_id:
            KERANJANG_DB.remove(item)
            flash(f"Menu '{item['nama']}' berhasil dihapus dari sistem.", "info")
            break
    return redirect(url_for("admin_produk"))

if __name__ == "__main__":
    app.run(debug=True)
