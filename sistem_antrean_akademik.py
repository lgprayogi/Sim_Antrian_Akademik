# -*- coding: utf-8 -*-
"""
Sistem Antrean Pelayanan Akademik – Versi Ringkas
Implemen­tasikan dua penjadwal:
  • FCFS   – antrian FIFO
  • Prior  – antrian prioritas (min‑heap)
"""

import copy
import heapq
import random
import time
from collections import deque

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
class Mahasiswa:
    """Data for a single request."""
    def __init__(self, nim, nama, layanan, proses, priority, tiba):
        self.nim = nim
        self.nama = nama
        self.layanan = layanan
        self.proses = proses          # menit (simulasi)
        self.prio = priority          # angka lebih kecil = lebih tinggi
        self.tiba = tiba              # urutan kedatangan
        self.mulai = None
        self.selesai = None
        self.tunggu = None

    def __repr__(self):
        return f"{self.nim} {self.nama[:10]:<10} {self.layanan:<12}"


# ----------------------------------------------------------------------
# Queues
# ----------------------------------------------------------------------
class FCFSQueue:
    def __init__(self):
        self.q = deque()

    def enqueue(self, obj):
        self.q.append(obj)

    def dequeue(self):
        return self.q.popleft() if self.q else None

    def __len__(self):
        return len(self.q)


class PriorityQueue:
    def __init__(self):
        self.heap = []   # (priority, arrival, obj)

    def enqueue(self, obj):
        heapq.heappush(self.heap, (obj.prio, obj.tiba, obj))

    def dequeue(self):
        return heapq.heappop(self.heap)[2] if self.heap else None

    def __len__(self):
        return len(self.heap)


# ----------------------------------------------------------------------
# Helper – generate random dataset
# ----------------------------------------------------------------------
SERVICE_PRIORITY = {
    "Legalisasi": 3,
    "Surat Aktif": 2,
    "Konsultasi": 4,
    "Cuti": 1,
}
SERVICE_LIST = list(SERVICE_PRIORITY.keys())


def generate_dataset(n, seed):
    random.seed(seed)
    data = []
    for i in range(1, n + 1):
        layanan = random.choice(SERVICE_LIST)
        mahasiswa = Mahasiswa(
            nim=f"{i:06d}",
            nama=f"Mhs{i}",
            layanan=layanan,
            proses=random.randint(1, 10),          # menit
            priority=SERVICE_PRIORITY[layanan],
            tiba=i,
        )
        data.append(mahasiswa)
    return data


# ----------------------------------------------------------------------
# Simulators
# ----------------------------------------------------------------------
def simulate_fcfs(dataset):
    time_now = 0
    for m in dataset:
        start = max(time_now, m.tiba)
        m.mulai = start
        m.tunggu = start - m.tiba
        time_now = start + m.proses
        m.selesai = time_now
    return dataset


def simulate_priority(dataset):
    # Build heap from dataset (priority + arrival order)
    heap = [(m.prio, m.tiba, m) for m in dataset]
    heapq.heapify(heap)
    time_now = 0
    result = []
    while heap:
        _, _, m = heapq.heappop(heap)
        start = max(time_now, m.tiba)
        m.mulai = start
        m.tunggu = start - m.tiba
        time_now = start + m.proses
        m.selesai = time_now
        result.append(m)
    return result


# ----------------------------------------------------------------------
# Minimal interactive menu
# ----------------------------------------------------------------------
def main():
    fcfs_q = FCFSQueue()
    prio_q = PriorityQueue()
    
    while True:
        print("\n=== Sistem Antrean Akademik (Ringkas) ===")
        print("1. Tambah mahasiswa (manual)")
        print("2. Tampilkan antrean")
        print("3. Proses satu mahasiswa")
        print("4. Proses semua antrean (dengan statistik)")
        print("5. Generate antrean otomatis")
        print("6. Hapus antrean")
        print("7. Keluar")
        choice = input("Pilihan (1‑7): ").strip()
        if choice == "1":
            nim = input("NIM: ").strip()
            nama = input("Nama: ").strip()
            print("Layanan:")
            for idx, layanan_item in enumerate(SERVICE_LIST, start=1):
                print(f"  {idx}. {layanan_item}")
            layanan_choice = input(f"Pilih layanan (1-{len(SERVICE_LIST)}): ").strip()
            if not layanan_choice.isdigit() or not (1 <= int(layanan_choice) <= len(SERVICE_LIST)):
                print("Pilihan layanan tidak valid.")
                continue
            layanan = SERVICE_LIST[int(layanan_choice) - 1]
            proses = int(input("Waktu proses (menit): ").strip())
            m = Mahasiswa(
                nim=nim,
                nama=nama,
                layanan=layanan,
                proses=proses,
                priority=SERVICE_PRIORITY[layanan],
                tiba=len(fcfs_q) + 1,
            )
            fcfs_q.enqueue(m)
            prio_q.enqueue(m)
            print("Mahasiswa ditambahkan.")
        elif choice == "2":
            print("\nTampilkan antrean")
            print("1. Antrean Prioritas")
            print("2. Antrean FCFS")
            submenu = input("Pilih antrean (1-2): ").strip()
            if submenu == "1":
                print("\n--- Antrean Prioritas ---")
                sorted_prio = sorted(prio_q.heap, key=lambda x: (x[0], x[1]))
                for i, (_, _, m) in enumerate(sorted_prio, 1):
                    print(f"{i}. {m} (prio={m.prio})")
            elif submenu == "2":
                print("\n--- Antrean FCFS ---")
                for i, m in enumerate(fcfs_q.q, 1):
                    print(f"{i}. {m} (prio={m.prio})")
            else:
                print("Pilihan tidak valid.")
                continue
        elif choice == "3":
            if len(fcfs_q) == 0:
                print("Antrean kosong.")
                continue
            m_fcfs = fcfs_q.dequeue()
            m_prio = prio_q.dequeue()
            print("\nDilayani (FCFS):", m_fcfs)
            print("Dilayani (Prioritas):", m_prio)
        elif choice == "4":
            if len(fcfs_q) == 0:
                print("Antrean kosong.")
                continue
            
            print("\n=== Memproses dan Membandingkan FCFS & Prioritas ===")
            
            # Copy data agar antrean asli tidak hilang
            dataset_fcfs = [copy.deepcopy(m) for m in fcfs_q.q]
            dataset_prio = [copy.deepcopy(m) for m in fcfs_q.q]
            
            # Jalankan simulasi & hitung waktu komputasi
            t0 = time.perf_counter()
            res_fcfs = simulate_fcfs(dataset_fcfs)
            t_fcfs_ms = (time.perf_counter() - t0) * 1000

            t0 = time.perf_counter()
            res_prio = simulate_priority(dataset_prio)
            t_prio_ms = (time.perf_counter() - t0) * 1000
            
            # Hitung statistik
            w_t_fcfs = [m.tunggu for m in res_fcfs]
            w_p_fcfs = [m.proses for m in res_fcfs]
            t_a_fcfs = [(m.selesai - m.tiba) for m in res_fcfs]
            
            w_t_prio = [m.tunggu for m in res_prio]
            w_p_prio = [m.proses for m in res_prio]
            t_a_prio = [(m.selesai - m.tiba) for m in res_prio]

            w_t_fcfs_avg = sum(w_t_fcfs) / len(w_t_fcfs)
            w_p_fcfs_avg = sum(w_p_fcfs) / len(w_p_fcfs)
            t_a_fcfs_avg = sum(t_a_fcfs) / len(t_a_fcfs)
            
            w_t_prio_avg = sum(w_t_prio) / len(w_t_prio)
            w_p_prio_avg = sum(w_p_prio) / len(w_p_prio)
            t_a_prio_avg = sum(t_a_prio) / len(t_a_prio)

            print(f"\nTotal Antrean Diproses: {len(res_fcfs)} mahasiswa")
            print(f"Waktu Komputasi Real-time -> FCFS: {t_fcfs_ms:.4f} ms | Prioritas: {t_prio_ms:.4f} ms\n")

            print(f"{'Indikator (menit)':<17} | {'FCFS':<35} | {'Prioritas':<35}")
            print("-" * 93)
            
            def fmt(avg, mn, mx): 
                return f"Avg: {avg:.2f} | Min: {mn} | Max: {mx}"
            
            print(f"{'Waktu Tunggu':<17} | {fmt(w_t_fcfs_avg, min(w_t_fcfs), max(w_t_fcfs)):<35} | {fmt(w_t_prio_avg, min(w_t_prio), max(w_t_prio)):<35}")
            print(f"{'Waktu Proses':<17} | {fmt(w_p_fcfs_avg, min(w_p_fcfs), max(w_p_fcfs)):<35} | {fmt(w_p_prio_avg, min(w_p_prio), max(w_p_prio)):<35}")
            print(f"{'Turnaround Time':<17} | {fmt(t_a_fcfs_avg, min(t_a_fcfs), max(t_a_fcfs)):<35} | {fmt(t_a_prio_avg, min(t_a_prio), max(t_a_prio)):<35}")
            print("-" * 93)

        elif choice == "5":
            print("\nPilih jumlah antrean yang ingin ditambahkan (Otomatis):")
            print("1. 50")
            print("2. 100")
            print("3. 500")
            print("4. 1000")
            pilihan_skenario = input("Pilihan (1-4): ").strip()
            
            if pilihan_skenario == "1":
                n = 50
            elif pilihan_skenario == "2":
                n = 100
            elif pilihan_skenario == "3":
                n = 500
            elif pilihan_skenario == "4":
                n = 1000
            else:
                print("Pilihan tidak valid, membatalkan.")
                continue
                
            data_baru = generate_dataset(n, seed=len(fcfs_q) + int(time.time()))
            for m in data_baru:
                m.tiba = len(fcfs_q) + 1
                fcfs_q.enqueue(m)
                prio_q.enqueue(m)
            print(f"{n} antrean berhasil ditambahkan secara otomatis!")
        elif choice == "6":
            fcfs_q.q.clear()
            prio_q.heap.clear()
            print("\nSeluruh antrean telah dikosongkan.")
        elif choice == "7":
            print("Terima kasih, selesai.")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()