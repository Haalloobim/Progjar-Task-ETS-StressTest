# Time Server and Client (Multithreaded TCP-based)

## 📋 Deskripsi
Proyek ini merupakan implementasi **File Protocol Client Server** berbasis TCP socket yang berjalan pada port `6666`. Server ini mampu menangani beberapa koneksi client secara **concurrent** menggunakan konsep **multithreading**. Setiap client dapat melakukan listing file, download file, upload file, dan juga delete file. 

## 🧩 Fitur
- Server membuka port `6666` menggunakan protokol **TCP**.
- Setiap client yang terhubung akan dilayani dalam thread tersendiri.
- Perintah yang dikenali oleh server:
  - `LIST`: Mengembalikan semua file yang ada di server.
  - `GET`: Melakukan aksi download file pada server.
  - `ADD`: Melakukan aksi uploads file ke server.
  - `DELETE`: Melakukan aksi delete file yang ada di server.
  - Perintah lainnya akan menghasilkan respon error.



## 🚀 Cara Menjalankan Program

### 1. Jalankan Server

Buka terminal dan jalankan file `FileServer.py`:

```bash
python FileServer.py
```

Output akan menampilkan log setiap kali ada client yang terhubung dan permintaan yang diterima.

### 2. Jalankan Client

Buka terminal baru dan jalankan `FileCLientCLI.py`:

```bash
python FileCLientCLI.py
```

Kemudian kamu akan diminta untuk memasukkan perintah untuk masing-masing client yang berjalan secara paralel:

```python
print("File Transfer Client")
print("====================")
print("1. List file")
print("2. Download file")
print("3. Upload file")
print("4. Delete file")
print("5. Exit")
print("====================")
```

## 🔒 Catatan Keamanan
Untuk keperluan produksi, pastikan port yang digunakan tidak terbuka untuk publik jika tidak diperlukan. Gunakan autentikasi dan enkripsi jika ingin mengembangkan lebih lanjut.

## 🧑‍💻 Author
- Nama: Muhammad Bimatara Indianto
- Tugas: Pembuatan File protocol Client Server
- Mata Kuliah: Pemrograman Jaringan 