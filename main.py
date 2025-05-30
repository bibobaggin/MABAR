# main.py
from auth import register, login_auth
from features import Antrian # Antrian class from features.py
from logger import tampilkan_audit_log, log_activity
from utils import get_display_name

# USER MENU
def user_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        print(f"\nMenu User — {current_display_name}:")
        print("1. Cek Antrian")
        print("2. Masuk ke Antrean")
        print("3. Keluar dari Antrean")
        print("4. Cetak Antrian")
        print("5. Logout")
        choice = input("Pilih aksi (1-5): ")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (user)")
        elif choice == '2':
            # current_username wants to enter the queue themselves
            antrian_instance.masuk_ke_antrean(current_username, actor_username=current_username, actor_role=current_role)
        elif choice == '3':
            antrian_instance.keluar_dari_antrean(current_username, actor_username=current_username, actor_role=current_role)
        elif choice == '4':
            antrian_instance.cetak_antrian()
            # Logging for this action can be added if desired, e.g.:
            log_activity(current_username, current_role, "Mencetak laporan antrian")
        elif choice == '5':
            log_activity(current_username, current_role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")

# TELLER MENU
def teller_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        print("\nMenu Teller:")
        print("1. Lihat Antrian Saat Ini")
        print("2. Proses Pengguna yang Antre")
        print("3. Tambah Prioritas ke Pengguna Antre")
        print("4. Cari Pengguna")
        print("5. Logout")
        choice = input("Pilih aksi (1-5): ")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (teller)")
        elif choice == '2':
            antrian_instance.proses_antrean_berikutnya(actor_username=current_username, actor_role=current_role)
        elif choice == '3':
            user_to_prioritize = input("Masukkan username pengguna yang ingin diberi prioritas: ").strip()
            if user_to_prioritize:
                antrian_instance.masuk_prioritas(user_to_prioritize, actor_username=current_username, actor_role=current_role)
            else:
                print("Username tidak boleh kosong.")
        elif choice == '4':
            user_to_find = input("Masukkan username pengguna yang ingin dicari: ").strip()
            if user_to_find:
                antrian_instance.cari_nama_orang_antre(user_to_find)
                # Logging for search action
                log_activity(current_username, current_role, "Mencari pengguna", f"Target pencarian: {user_to_find}")
            else:
                print("Username tidak boleh kosong.")
        elif choice == '5':
            log_activity(current_username, current_role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")

# ADMIN MENU
def admin_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        print(f"\nMenu Admin — {current_display_name}:")
        print("1. Lihat Antrian Saat Ini")
        print("2. Tambah Pengguna ke Antrean (Manual)")
        print("3. Hapus Pengguna dari Antrean (Manual)")
        print("4. Proses Antrean Berikutnya")
        print("5. Tukar Posisi Antrean")
        print("6. Tambah Prioritas ke Pengguna Antre")
        print("7. Tampilkan Audit Log")
        print("8. Logout")

        choice = input("Pilih aksi (1-8): ")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (admin)")
        elif choice == '2':
            user_to_add = input("Masukkan username pengguna yang ingin ditambahkan ke antrean: ").strip()
            if user_to_add:
                antrian_instance.masuk_ke_antrean(user_to_add, actor_username=current_username, actor_role=current_role)
            else:
                print("Username tidak boleh kosong.")
        elif choice == '3':
            user_to_remove = input("Masukkan username pengguna yang ingin dihapus dari antrean: ").strip()
            if user_to_remove:
                antrian_instance.keluar_dari_antrean(user_to_remove, actor_username=current_username, actor_role=current_role)
            else:
                print("Username tidak boleh kosong.")
        elif choice == '4':
            antrian_instance.proses_antrean_berikutnya(actor_username=current_username, actor_role=current_role)
        elif choice == '5':
            try:
                idx1_str = input("Masukkan indeks pengguna pertama (mulai dari 0): ").strip()
                idx2_str = input("Masukkan indeks pengguna kedua (mulai dari 0): ").strip()
                if not idx1_str or not idx2_str:
                    print("Indeks tidak boleh kosong.")
                else:
                    idx1 = int(idx1_str)
                    idx2 = int(idx2_str)
                    antrian_instance.update_antrean(idx1, idx2, actor_username=current_username, actor_role=current_role)
            except ValueError:
                print("Indeks harus berupa angka.")
            except Exception as e:
                print(f"Terjadi kesalahan saat menukar posisi: {e}")
        elif choice == '6':
            user_to_prioritize = input("Masukkan username pengguna yang ingin diberi prioritas: ").strip()
            if user_to_prioritize:
                antrian_instance.masuk_prioritas(user_to_prioritize, actor_username=current_username, actor_role=current_role)
            else:
                print("Username tidak boleh kosong.")
        elif choice == '7':
            tampilkan_audit_log()
            # Log this action as well
            log_activity(current_username, current_role, "Menampilkan audit log")
        elif choice == '8':
            log_activity(current_username, current_role, "Logout")
            break
        else:
            print("Pilihan tidak valid!")


def main():
    file_choice = input("Pilih format file antrean (1 = TXT, 2 = CSV): ")
    queue_system = Antrian("antrian.txt") if file_choice == '1' else Antrian("antrian.csv")

    while True:
        print("\n=== Selamat Datang di Sistem Manajemen Antrian Bank ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        menu_choice = input("Pilih menu: ")

        if menu_choice == '1':
            login_result = login_auth()
            if login_result:
                logged_username, logged_display_name, logged_role = login_result
                if logged_role == "user":
                    user_menu(queue_system, logged_username, logged_display_name, logged_role)
                elif logged_role == "teller":
                    teller_menu(queue_system, logged_username, logged_display_name, logged_role)
                elif logged_role == "admin":
                    admin_menu(queue_system, logged_username, logged_display_name, logged_role)
        elif menu_choice == '2':
            register()
        elif menu_choice == '3':
            # FIX APPLIED HERE: Log a generic system exit.
            log_activity("system", "N/A", "Aplikasi ditutup dari menu utama")
            print("Terima kasih telah menggunakan sistem kami.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()