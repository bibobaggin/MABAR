# auth.py
import csv, os
from logger import log_activity
from utils import USER_DB

def register():
    print("\n== Registrasi Pengguna Baru ==")
    username = input("Username baru: ").strip()
    display_name = input("Nama lengkap: ").strip()
    password = input("Password baru: ").strip()
    role = input("Role (user/teller/admin): ").strip().lower()
    if role not in ["user","teller","admin"]:
        print("Role tidak valid."); return

    log_activity(username, role, "Registrasi", f"Role={role}")
    # simpan ke CSV
    with open(USER_DB, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, password, display_name, role])
    print("Registrasi berhasil!")

def login_auth():
    import csv
    print("\n== Login ==")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if os.path.exists(USER_DB):
        with open(USER_DB, "r", newline="") as f:
            for row in csv.reader(f):
                if row and row[0]==username and row[1]==password:
                    display_name, role = row[2], row[3]
                    print(f"Login berhasil sebagai {display_name}!")
                    log_activity(username, role, "Login sukses")
                    return username, display_name, role
    print("Login gagal!")
    log_activity(username, "-", "Login gagal")
    return None
