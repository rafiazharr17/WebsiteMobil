from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data dummy untuk daftar mobil
cars = [
    {"id": 1, "nama": "PEUGEOT", "harga": 50000, "gambar": "car1.jpg"},
    {"id": 2, "nama": "LAMBORGHINI", "harga": 60000, "gambar": "car2.jpeg"},
    # Tambahkan data mobil lainnya
]

# Data dummy untuk menyimpan informasi pembelian
purchases = []

@app.route('/')
def index():
    return render_template('home.html', cars=cars)

@app.route('/proses-pembelian', methods=['POST'])
def proses_pembelian():
    nama = request.form.get('nama')
    alamat = request.form.get('alamat')
    telepon = request.form.get('telepon')
    mobil_id = int(request.form.get('mobil_id'))

    # Temukan mobil yang dipilih
    mobil_terpilih = next((mobil for mobil in cars if mobil['id'] == mobil_id), None)

    if mobil_terpilih:
        # Hitung total harga
        total_harga = mobil_terpilih['harga']

        # Simpan informasi pembelian
        pembelian = {
            'nama_pelanggan': nama,
            'alamat_pelanggan': alamat,
            'telepon_pelanggan': telepon,
            'nama_mobil': mobil_terpilih['nama'],
            'gambar_mobil': mobil_terpilih['gambar'],
            'total_harga': total_harga
        }

        purchases.append(pembelian)

        # Redirect ke halaman invoice
        return redirect(url_for('invoice', purchase_id=len(purchases)))

    return "Error: Mobil tidak ditemukan."

@app.route('/invoice/<int:purchase_id>')
def invoice(purchase_id):
    if 1 <= purchase_id <= len(purchases):
        data_invoice = purchases[purchase_id - 1]
        return render_template('invoice.html', **data_invoice)
    else:
        return "Error: Invoice tidak ditemukan."

if __name__ == '__main__':
    app.run(debug=True)
