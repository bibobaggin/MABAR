# main.py
from auth import register, login_auth
from features import Antrian
from logger import tampilkan_audit_log, log_activity
from utils import USER_DB, get_display_name

def user_menu(antrian, username, display_name,role):
    while True:
        print(f"\nMenu User — {display_name}:")
        print("1. Cek Antrian")
        print("2. Masuk ke Antrean")
        print("3. Keluar dari Antrean")
        print("4. Cetak Antrian")
        print("5. Logout")
        choice = input("Pilih aksi (1-5): ")

        if choice == '1':
            antrian.cek_antrian()
        elif choice == '2':
            antrian.masuk_ke_antrean(username)
        elif choice == '3':
            antrian.keluar_dari_antrean(username)
        elif choice == '4':
            antrian.cetak_antrian()
        elif choice == '5':
            log_activity(username, role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")


def teller_menu(antrian, username, display_name, role):
    while True:
        print("\nMenu Teller:")
        print("1. Lihat Antrian Saat Ini")
        print("2. Proses Pengguna yang Antre")
        print("3. Tambah Prioritas ke Pengguna Antrean")
        print("4. Keluar")
        choice = input("Pilih aksi (1-4): ")

        if choice == '1':
            antrian.cek_antrian()
        elif choice == '2':
            if antrian.antrian.is_empty():
                print("Tidak ada pengguna dalam antrean.")
            else:
                nama = antrian.antrian.dequeue()
                print(f"Pengguna {nama} telah diproses dan dikeluarkan dari antrean.")
                antrian.save_antrian()
                log_activity(nama, get_display_name(nama), "Diproses oleh teller")
        elif choice == '3':
            if antrian.antrian.is_empty():
                print("Tidak ada pengguna dalam antrean.")
            else:
                nama = input("Masukkan nama pengguna yang akan diberi prioritas: ")
                current = antrian.antrian.front
                found = False
                while current:
                    if current.data == nama:
                        found = True
                        break
                    current = current.next
                if found:
                    antrian.keluar_dari_antrean(nama)
                    antrian.masuk_prioritas(nama)
                else:
                    print(f"{nama} tidak ditemukan dalam antrean.")
        elif choice == '4':
            log_activity(username, role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")

def admin_menu(antrian,admin_username,admin_display_name,role):
    while True:
        print("\nMenu Admin:")
        print("1. Lihat/Cetak Antrian")
        print("2. Modifikasi Antrean")
        print("3. Import Antrean")
        print("4. Export Antrean")
        print("5. Cari Nama Orang yang Antre")
        print("6. Update Antrean (Tukar Urutan)")
        print("7. Keluar")
        print("8. Tampilkan Audit Log")
        choice = input("Pilih aksi (1-7): ")

        if choice == '1':
            antrian.cetak_antrian()
        elif choice == '2':
            try:
                index = int(input("Masukkan index antrean yang ingin dihapus: ")) - 1
                antrian.modifikasi_antrean(index,admin_username,admin_display_name)
            except ValueError:
                print("Masukkan harus berupa angka!")
        elif choice == '3':
            data = input("Masukkan data antrean (pisahkan dengan koma): ").split(",")
            cleaned_data = [x.strip() for x in data]
            antrian.import_antrean(cleaned_data)
        elif choice == '4':
            antrian.export_antrean()
        elif choice == '5':
            nama = input("Masukkan nama yang dicari: ")
            antrian.cari_nama_orang_antre(nama)
        elif choice == '6':
            # 1) Ambil string input dulu
            s1 = input("Masukkan index pertama: ")
            s2 = input("Masukkan index kedua: ")
            # 2) Coba parsing angka saja
            try:
                idx1 = int(s1) - 1
                idx2 = int(s2) - 1
            except ValueError:
                print("Masukkan harus berupa angka!")
                continue   # langsung kembali ke menu, tanpa update_antrean
            # 3) Parsing sukses, tinggal swap
            antrian.update_antrean(idx1, idx2, admin_username, admin_display_name)

        elif choice == '7':
            log_activity(admin_username, role, "Logout")

            break
        elif choice == '8':
            tampilkan_audit_log()


        else:
            print("Pilihan tidak valid!")


def main():
    file_choice = input("Pilih format file antrean (1 = TXT, 2 = CSV): ")
    antrian = Antrian("antrian.txt") if file_choice == '1' else Antrian("antrian.csv")

    while True:
        print("\n=== Selamat Datang di Sistem Manajemen Antrian Bank ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        menu = input("Pilih menu: ")

        if menu == '1':
            result = login_auth()
            if result:
                username, display_name, role = result
                if role == "user":
                    user_menu(antrian, username, display_name,role)
                elif role == "teller":
                    teller_menu(antrian, username, display_name, role)
                elif role == "admin":
                    admin_menu(antrian, username, display_name,role)

        elif menu == '2':
            register()
        elif menu == '3':
            log_activity(username, role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
