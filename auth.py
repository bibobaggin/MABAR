# auth.py
import csv
import os
from logger import log_activity
from utils import (
    USER_DB, print_header, print_error, print_success,
    styled_input, print_warning, get_display_name,clear_screen # Added get_display_name
)

def register():
    clear_screen() # Added
    print_header("Registrasi Pengguna Baru")
    username = styled_input("Username baru:").strip()
    display_name = styled_input("Nama lengkap:").strip()
    password = styled_input("Password baru:").strip() # Consider using getpass for passwords
    role = styled_input("Role (user/teller/admin):").strip().lower()

    if not username or not display_name or not password:
        print_warning("Semua field harus diisi.")
        return

    if role not in ["user", "teller", "admin"]:
        print_error("Role tidak valid. Harap pilih user, teller, atau admin.")
        return

    # Check if username already exists
    if os.path.exists(USER_DB):
        with open(USER_DB, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username:
                    print_warning(f"Username '{username}' sudah terdaftar.")
                    return

    # Simpan ke CSV
    try:
        with open(USER_DB, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, display_name, role])
        log_activity(username, role, "Registrasi", f"Role={role}")
        print_success("Registrasi berhasil!")
    except IOError:
        print_error("Gagal menyimpan data pengguna.")


def login_auth():
    clear_screen() # Added
    print_header("Login Pengguna")
    username = styled_input("Username:").strip()
    password = styled_input("Password:").strip() # Consider getpass

    if not os.path.exists(USER_DB):
        print_error(f"Database pengguna ({USER_DB}) tidak ditemukan.")
        return None

    try:
        with open(USER_DB, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and len(row) >= 4: # Ensure row has enough columns
                    db_username, db_password, db_display_name, db_role = row[0], row[1], row[2], row[3]
                    if db_username == username and db_password == password:
                        # print_success(f"Login berhasil sebagai {db_display_name}!") # Moved to main.py
                        log_activity(username, db_role, "Login sukses")
                        return username, db_display_name, db_role
            print_error("Username atau password salah.")
            return None
    except FileNotFoundError:
        print_error(f"Database pengguna ({USER_DB}) tidak ditemukan.")
        return None
    except Exception as e:
        print_error(f"Terjadi kesalahan saat login: {e}")
        return None