# README – Petunjuk Penggunaan Program

## Sistem Antrean Pelayanan Akademik

Program ini merupakan simulasi sistem antrean pelayanan akademik yang membandingkan algoritma **First Come First Serve (FCFS)** dan **Priority Scheduling**.

## Cara Menjalankan Program

1. Pastikan Python 3 telah terpasang pada komputer.
2. Buka Terminal atau Command Prompt.
3. Masuk ke folder tempat file program berada.
4. Jalankan program dengan perintah:

```bash
python nama_file.py
```

---

# Menu Program

Saat program dijalankan akan muncul menu berikut:

```
=== Sistem Antrean Akademik ===

1. Tambah mahasiswa
2. Tampilkan antrean
3. Proses satu mahasiswa
4. Proses semua antrean
5. Generate antrean otomatis
6. Hapus antrean
7. Keluar
```

---

## 1. Tambah Mahasiswa

Digunakan untuk menambahkan data mahasiswa secara manual ke dalam antrean.

Data yang dimasukkan:

* NIM
* Nama
* Jenis layanan
* Waktu proses (menit)

Setelah data dimasukkan, mahasiswa akan otomatis masuk ke antrean FCFS dan Priority Scheduling.

---

## 2. Tampilkan Antrean

Menampilkan isi antrean yang sedang tersimpan.

Terdapat dua pilihan:

* **Antrean Prioritas**

  * Ditampilkan berdasarkan prioritas layanan.
* **Antrean FCFS**

  * Ditampilkan berdasarkan urutan kedatangan mahasiswa.

---

## 3. Proses Satu Mahasiswa

Memproses satu mahasiswa dari masing-masing algoritma.

Program akan menampilkan:

* Mahasiswa yang diproses menggunakan FCFS.
* Mahasiswa yang diproses menggunakan Priority Scheduling.

---

## 4. Proses Semua Antrean

Menjalankan simulasi seluruh data antrean menggunakan kedua algoritma.

Output yang ditampilkan meliputi:

* Jumlah antrean yang diproses.
* Waktu komputasi (real-time) FCFS.
* Waktu komputasi (real-time) Priority Scheduling.
* Rata-rata, minimum, dan maksimum:

  * Waktu tunggu (Waiting Time)
  * Waktu proses (Processing Time)
  * Turnaround Time

Menu ini digunakan untuk membandingkan performa kedua algoritma.

---

## 5. Generate Antrean Otomatis

Membuat data mahasiswa secara otomatis.

Pilihan jumlah data:

* 50 mahasiswa
* 100 mahasiswa
* 500 mahasiswa
* 1000 mahasiswa

Data yang dihasilkan bersifat acak dan langsung dimasukkan ke dalam kedua antrean.

---

## 6. Hapus Antrean

Menghapus seluruh data antrean pada:

* FCFS Queue
* Priority Queue

Gunakan menu ini sebelum melakukan pengujian baru agar data sebelumnya tidak tercampur.

---

## 7. Keluar

Menutup program dan mengakhiri proses simulasi.

---

# Alur Penggunaan yang Disarankan

1. Jalankan program.
2. Tambahkan data mahasiswa secara manual **atau** gunakan menu **Generate Antrean Otomatis**.
3. Pilih **Tampilkan Antrean** untuk melihat isi antrean.
4. Pilih **Proses Semua Antrean** untuk membandingkan algoritma FCFS dan Priority Scheduling.
5. Amati hasil statistik dan waktu komputasi yang ditampilkan.
6. Jika ingin melakukan pengujian baru, gunakan **Hapus Antrean**, kemudian ulangi langkah 2–5.
7. Pilih **Keluar** untuk mengakhiri program.

---

# Keterangan Prioritas Layanan

| Layanan     | Prioritas |
| ----------- | :-------: |
| Cuti        |     1     |
| Surat Aktif |     2     |
| Legalisasi  |     3     |
| Konsultasi  |     4     |

**Catatan:** Semakin kecil nilai prioritas, semakin dahulu mahasiswa akan diproses pada algoritma Priority Scheduling.
