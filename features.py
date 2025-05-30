import csv, os
from queue import Node, LinkedListQueue # type: ignore
from logger import log_activity
from utils import USER_DB, get_display_name


class Antrian:
    def __init__(self, file_name="antrian.txt"):
        self.file_name = file_name
        self.antrian = LinkedListQueue()
        self.load_antrian()

    def masuk_prioritas(self, nama):
        self.antrian.enqueue_prioritas(nama)
        print(f"{nama} berhasil dimasukkan sebagai prioritas ke depan antrean.")
        self.save_antrian()
        log_activity(nama, get_display_name(nama), "Diberi prioritas")

    def load_antrian(self):
        if self.file_name.endswith(".txt"):
            if os.path.exists(self.file_name):
                with open(self.file_name, "r") as f:
                    for line in f:
                        self.antrian.enqueue(line.strip())
        elif self.file_name.endswith(".csv"):
            if os.path.exists(self.file_name):
                with open(self.file_name, mode="r", newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:
                            self.antrian.enqueue(row[0])

    def save_antrian(self):
        if self.file_name.endswith(".txt"):
            with open(self.file_name, "w") as f:
                current = self.antrian.front
                while current:
                    f.write(f"{current.data}\n")
                    current = current.next
        elif self.file_name.endswith(".csv"):
            with open(self.file_name, mode="w", newline='') as f:
                writer = csv.writer(f)
                current = self.antrian.front
                while current:
                    writer.writerow([current.data])
                    current = current.next

    def cek_antrian(self):
        if self.antrian.is_empty():
            print("Antrian kosong.")
        else:
            print("Status Antrian saat ini:")
            self.save_antrian()
            self.antrian.display()

    def masuk_ke_antrean(self, nama):
        if self.antrian.exists(nama):
            print(f"{nama} sudah ada dalam antrean.")
            return
        self.antrian.enqueue(nama)
        print(f"{nama} berhasil masuk ke antrean.")
        self.save_antrian()
        log_activity(nama, get_display_name(nama), "Masuk ke antrean")

    def keluar_dari_antrean(self, nama):
        temp_antrian = LinkedListQueue()
        found = False
        while not self.antrian.is_empty():
            current = self.antrian.dequeue()
            if current == nama:
                found = True
            else:
                temp_antrian.enqueue(current)
        self.antrian = temp_antrian
        if found:
            print(f"{nama} keluar dari antrean.")
            self.save_antrian()
            log_activity(nama, get_display_name(nama), "Keluar dari antrean")
        else:
            print(f"{nama} tidak ditemukan dalam antrean.")

    def cetak_antrian(self):
        print("Menampilkan antrian untuk dicetak...")
        self.save_antrian
        self.cek_antrian()

    def modifikasi_antrean(self, index, admin_username, admin_display_name):
        current = self.antrian.front
        counter = 0
        temp_antrian = LinkedListQueue()
        removed = None

        while current:
            if counter == index:
                removed = current.data   # catat yang dihapus
            else:
                temp_antrian.enqueue(current.data)
            current = current.next
            counter += 1

        self.antrian = temp_antrian
        self.save_antrian()

        if removed:
            # tampilkan konfirmasi
            print(f"{get_display_name(removed)} ({removed}) berhasil dihapus dari antrean.")
            # catat di log
            action = f"Hapus antrean di posisi {index+1}"
            details = f"{get_display_name(removed)} ({removed})"
            log_activity(admin_username, admin_display_name, action, details)
        else:
            print("Index tidak valid!")


    def import_antrean(self, data):
        for nama in data:
            self.antrian.enqueue(nama.strip())
        print("Data antrean berhasil diimpor.")
        self.save_antrian()

    def export_antrean(self):
        print("Data antrean untuk diekspor:")
        self.cek_antrian()

    def cari_nama_orang_antre(self, nama):
        current = self.antrian.front
        while current:
            if current.data == nama:
                print(f"{nama} sedang dalam antrean.")
                return
            current = current.next
        print(f"{nama} tidak ditemukan dalam antrean.")

    def update_antrean(self, index1, index2, actor_username, actor_display_name):
        # kumpulkan semua data antrean
        all_data = []
        current = self.antrian.front
        while current:
            all_data.append(current.data)
            current = current.next

        # validasi index
        if 0 <= index1 < len(all_data) and 0 <= index2 < len(all_data):
            # nama user yang dipertukarkan
            user1 = all_data[index1]
            user2 = all_data[index2]

            # swap data
            all_data[index1], all_data[index2] = user2, user1

            # rebuild antrean
            self.antrian = LinkedListQueue()
            for data in all_data:
                self.antrian.enqueue(data)

            print(f"Urutan antrean {user1} dan {user2} berhasil ditukar.")
            self.save_antrian()

            # catat ke audit log
            aksi = f"Tukar urutan: {get_display_name(user1)} ({user1}) <-> {get_display_name(user2)} ({user2})"

            log_activity(actor_username, actor_display_name, aksi)

        else:
            print("Index tidak valid!")