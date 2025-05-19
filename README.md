# Time Server and Client (Multithreaded TCP-based)

## 📋 Deskripsi
Proyek ini merupakan implementasi **File Protocol Stress Test** berbasis TCP socket yang berjalan pada port `13337`. Program ini dirancang untuk menguji ketahanan dan performa server file protocol dalam menangani banyak koneksi secara bersamaan (**concurrent**) menggunakan konsep **multithreading** dan/atau **multiprocessing**. Dalam pengujian ini, setiap client secara paralel dapat melakukan operasi listing file, download file, upload file untuk mensimulasikan beban tinggi pada server.

## 🧩 Fitur
- Server membuka port `13337` menggunakan protokol **TCP**.
- Setiap client yang terhubung akan dilayani dalam thread tersendiri.
- Perintah yang dikenali oleh server:
  - `LIST`: Mengembalikan semua file yang ada di server.
  - `GET`: Melakukan aksi download file pada server.
  - `ADD`: Melakukan aksi uploads file ke server.
  - Perintah lainnya akan menghasilkan respon error.



## 🚀 Cara Menjalankan Program

### 1. Jalankan Server

Buka terminal dan jalankan file `FileServer.py`:

```bash
python3 FileServerMultithreading.py <jumlah-worker>
```

Output akan menampilkan log setiap kali ada client yang terhubung dan permintaan yang diterima.

### 2. Jalankan Client

Buka terminal baru dan jalankan `FileCLientSressTest.py`:

```bash
python FileCLientSressTest.py
```


## 🔒 Catatan Keamanan
Untuk keperluan produksi, pastikan port yang digunakan tidak terbuka untuk publik jika tidak diperlukan. Gunakan autentikasi dan enkripsi jika ingin mengembangkan lebih lanjut.

## 🧑‍💻 Author
- Nama: Muhammad Bimatara Indianto
- Tugas: Pembuatan File protocol Client Server
- Mata Kuliah: Pemrograman Jaringan 