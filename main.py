# main.py
from auth import register, login_auth
from features import Antrian
from logger import tampilkan_audit_log, log_activity
from utils import (
    get_display_name, init_colors, clear_screen, print_header,
    print_error, print_success, print_warning, styled_input,
    print_option, print_farewell, print_info
)

# Initialize colors once at the start
init_colors()

# USER MENU
def user_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        clear_screen()
        print_header(f"Menu User — {current_display_name}")
        print_option("1", "Cek Antrian")
        print_option("2", "Masuk ke Antrean")
        print_option("3", "Keluar dari Antrean")
        print_option("4", "Cetak Antrian")
        print_option("5", "Logout")
        choice = styled_input("Pilih aksi (1-5):")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (user)")
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '2':
            antrian_instance.masuk_ke_antrean(current_username, actor_username=current_username, actor_role=current_role)
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '3':
            antrian_instance.keluar_dari_antrean(current_username, actor_username=current_username, actor_role=current_role)
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '4':
            antrian_instance.cetak_antrian(current_username) # <<< Parameter added here
            log_activity(current_username, current_role, "Mencetak laporan antrian")
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '5':
            log_activity(current_username, current_role, "Logout")
            print_success(f"Logout berhasil. Sampai jumpa, {current_display_name}!")
            break
        else:
            print_error("Pilihan tidak valid!")
            styled_input("Tekan Enter untuk kembali...")

# TELLER MENU
def teller_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        clear_screen()
        print_header(f"Menu Teller — {current_display_name}")
        print_option("1", "Lihat Antrian Saat Ini")
        print_option("2", "Proses Pengguna yang Antre")
        print_option("3", "Tambah Prioritas ke Pengguna Antre")
        print_option("4", "Cari Pengguna")
        print_option("5", "Logout")
        choice = styled_input("Pilih aksi (1-5):")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (teller)")
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '2':
            antrian_instance.proses_antrean_berikutnya(actor_username=current_username, actor_role=current_role)
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '3':
            user_to_prioritize = styled_input("Masukkan username pengguna yang ingin diberi prioritas:").strip()
            if user_to_prioritize:
                antrian_instance.masuk_prioritas(user_to_prioritize, actor_username=current_username, actor_role=current_role)
            else:
                print_warning("Username tidak boleh kosong.")
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '4':
            user_to_find = styled_input("Masukkan username pengguna yang ingin dicari:").strip()
            if user_to_find:
                antrian_instance.cari_nama_orang_antre(user_to_find)
                log_activity(current_username, current_role, "Mencari pengguna", f"Target pencarian: {user_to_find}")
            else:
                print_warning("Username tidak boleh kosong.")
            styled_input("Tekan Enter untuk kembali...")
        elif choice == '5':
            log_activity(current_username, current_role, "Logout")
            print_success(f"Logout berhasil. Sampai jumpa, {current_display_name}!")
            break
        else:
            print_error("Pilihan tidak valid!")
            styled_input("Tekan Enter untuk kembali...")

# ADMIN MENU
def admin_menu(antrian_instance, current_username, current_display_name, current_role):
    while True:
        clear_screen()
        print_header(f"Menu Admin — {current_display_name}")
        print_option("1", "Lihat Antrian Saat Ini")
        print_option("2", "Tambah Pengguna ke Antrean (Manual)")
        print_option("3", "Hapus Pengguna dari Antrean (Manual)")
        print_option("4", "Proses Antrean Berikutnya")
        print_option("5", "Tukar Posisi Antrean")
        print_option("6", "Tambah Prioritas ke Pengguna Antre")
        print_option("7", "Tampilkan Audit Log")
        print_option("8", "Logout")

        choice = styled_input("Pilih aksi (1-8):")

        if choice == '1':
            antrian_instance.cek_antrian()
            log_activity(current_username, current_role, "Melihat antrian (admin)")
        elif choice == '2':
            user_to_add = styled_input("Masukkan username pengguna yang ingin ditambahkan ke antrean:").strip()
            if user_to_add:
                antrian_instance.masuk_ke_antrean(user_to_add, actor_username=current_username, actor_role=current_role)
            else:
                print_warning("Username tidak boleh kosong.")
        elif choice == '3':
            user_to_remove = styled_input("Masukkan username pengguna yang ingin dihapus dari antrean:").strip()
            if user_to_remove:
                antrian_instance.keluar_dari_antrean(user_to_remove, actor_username=current_username, actor_role=current_role)
            else:
                print_warning("Username tidak boleh kosong.")
        elif choice == '4':
            antrian_instance.proses_antrean_berikutnya(actor_username=current_username, actor_role=current_role)
        elif choice == '5':
            try:
                idx1_str = styled_input("Masukkan indeks pengguna pertama (mulai dari 0):").strip()
                idx2_str = styled_input("Masukkan indeks pengguna kedua (mulai dari 0):").strip()
                if not idx1_str or not idx2_str:
                    print_warning("Indeks tidak boleh kosong.")
                else:
                    idx1 = int(idx1_str)
                    idx2 = int(idx2_str)
                    antrian_instance.update_antrean(idx1, idx2, actor_username=current_username, actor_role=current_role)
            except ValueError:
                print_error("Indeks harus berupa angka.")
            except Exception as e:
                print_error(f"Terjadi kesalahan saat menukar posisi: {e}")
        elif choice == '6':
            user_to_prioritize = styled_input("Masukkan username pengguna yang ingin diberi prioritas:").strip()
            if user_to_prioritize:
                antrian_instance.masuk_prioritas(user_to_prioritize, actor_username=current_username, actor_role=current_role)
            else:
                print_warning("Username tidak boleh kosong.")
        elif choice == '7':
            clear_screen()
            print_header("Audit Log Sistem")
            tampilkan_audit_log()
            log_activity(current_username, current_role, "Menampilkan audit log")
        elif choice == '8':
            log_activity(current_username, current_role, "Logout")
            print_success(f"Logout berhasil. Sampai jumpa, {current_display_name}!")
            break
        else:
            print_error("Pilihan tidak valid!")
        
        if choice != '8': # Don't pause on logout
             styled_input("Tekan Enter untuk kembali...")


def main():
    clear_screen()
    print_header("Sistem Manajemen Antrian Bank - MABSkuy", char="*", width=70)
    
    file_choice = styled_input("Pilih format file antrean (1 = TXT, 2 = CSV):")
    while file_choice not in ['1', '2']:
        print_error("Pilihan format file tidak valid.")
        file_choice = styled_input("Pilih format file antrean (1 = TXT, 2 = CSV):")

    queue_system = Antrian("antrian.txt") if file_choice == '1' else Antrian("antrian.csv")

    while True:
        clear_screen()
        print_header("Selamat Datang di MABSkuy")
        print_option("1", "Login")
        print_option("2", "Registrasi")
        print_option("3", "Keluar")
        menu_choice = styled_input("Pilih menu:")

        if menu_choice == '1':
            login_result = login_auth()
            if login_result:
                logged_username, logged_display_name, logged_role = login_result
                print_success(f"Login berhasil sebagai {logged_display_name}!")
                styled_input("Tekan Enter untuk melanjutkan...")
                if logged_role == "user":
                    user_menu(queue_system, logged_username, logged_display_name, logged_role)
                elif logged_role == "teller":
                    teller_menu(queue_system, logged_username, logged_display_name, logged_role)
                elif logged_role == "admin":
                    admin_menu(queue_system, logged_username, logged_display_name, logged_role)
            else: # Login failed
                styled_input("Tekan Enter untuk kembali...")

        elif menu_choice == '2':
            register()
            styled_input("Tekan Enter untuk kembali...")
        elif menu_choice == '3':
            log_activity("system", "N/A", "Aplikasi ditutup dari menu utama")
            clear_screen()
            print_farewell()
            break
        else:
            print_error("Pilihan tidak valid!")
            styled_input("Tekan Enter untuk kembali...")

if __name__ == "__main__":
    main()