# features.py
import csv
import os
from datetime import datetime
from linked_queue import LinkedListQueue # type: ignore
from logger import log_activity
from utils import (
    USER_DB, get_display_name, print_success, print_error,
    print_warning, print_info, AnsiColors, print_table_header, print_table_row,clear_screen
)

class Antrian:
    def __init__(self, file_name="antrian.txt"):
        self.file_name = file_name
        self.antrian = LinkedListQueue()
        self.load_antrian()

    def masuk_prioritas(self, nama, actor_username=None, actor_role=None):
        result = self.antrian.enqueue_prioritas(nama) # enqueue_prioritas should return status
        if result == "exists": # Assuming queue.py's enqueue methods return status
             # Warning already printed by queue.py
            pass
        elif result == "success":
            display_name = get_display_name(nama)
            print_success(f"{display_name} ({nama}) berhasil dimasukkan sebagai prioritas.")
            self.save_antrian()
            if actor_username and actor_role:
                log_activity(actor_username, actor_role, "Memberi prioritas", f"Pengguna: {nama} ({display_name})")
            else:
                log_activity(nama, "system", "Diberi prioritas (aktor tidak diketahui)")
        # else: nothing happens / queue was empty, handled by enqueue_prioritas

    def load_antrian(self):
        loaded_count = 0
        if not os.path.exists(self.file_name):
            # print_info(f"File antrian {self.file_name} tidak ditemukan. Memulai dengan antrian kosong.")
            return # No file to load

        try:
            if self.file_name.endswith(".txt"):
                with open(self.file_name, "r", encoding="utf-8") as f:
                    for line in f:
                        username = line.strip()
                        if username: # Ensure not an empty line
                            self.antrian.enqueue(username) 
                            loaded_count +=1
            elif self.file_name.endswith(".csv"):
                with open(self.file_name, mode="r", newline='', encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0]: # Ensure row and first element exist
                            self.antrian.enqueue(row[0])
                            loaded_count +=1
            # if loaded_count > 0:
            # print_info(f"{loaded_count} pengguna dimuat dari {self.file_name}.")
        except Exception as e:
            print_error(f"Gagal memuat antrian dari {self.file_name}: {e}")


    def save_antrian(self):
        try:
            with open(self.file_name, mode="w", newline='', encoding="utf-8") as f:
                current = self.antrian.front
                if self.file_name.endswith(".txt"):
                    while current:
                        f.write(current.data[0] + "\n")
                        current = current.next
                elif self.file_name.endswith(".csv"):
                    writer = csv.writer(f)
                    while current:
                        writer.writerow([current.data[0]])
                        current = current.next
        except IOError:
            print_error(f"Gagal menyimpan antrian ke {self.file_name}.")


    def cek_antrian(self):
        self.antrian.display() # display method in queue.py will be styled

    def masuk_ke_antrean(self, username, actor_username=None, actor_role=None):
        result = self.antrian.enqueue(username) # enqueue should return status
        if result == "exists":
            # Warning already printed by queue.py
            pass
        elif result == "success":
            display_name = get_display_name(username)
            print_success(f"{display_name} ({username}) berhasil masuk ke antrean.")
            self.save_antrian()
            if actor_username and actor_role:
                log_activity(actor_username, actor_role, "Masuk antrean", f"Pengguna: {username} ({display_name})")
            else:
                log_activity(username, "user", "Masuk antrean (self, aktor tidak diketahui)")

    def keluar_dari_antrean(self, username_to_remove, actor_username=None, actor_role=None):
        display_name = get_display_name(username_to_remove)
        if self.antrian.remove_item(username_to_remove):
            print_success(f"Pengguna {display_name} ({username_to_remove}) berhasil keluar dari antrean.")
            self.save_antrian()
            if actor_username and actor_role:
                log_activity(actor_username, actor_role, "Keluar dari antrean", f"Pengguna: {username_to_remove} ({display_name})")
            else:
                log_activity(username_to_remove, "user", "Keluar dari antrean (self, aktor tidak diketahui)")
            return True
        else:
            print_error(f"Pengguna {display_name} ({username_to_remove}) tidak ditemukan dalam antrean.")
            return False

    def proses_antrean_berikutnya(self, actor_username, actor_role):
        if self.antrian.is_empty():
            print_info("Antrean kosong, tidak ada yang bisa diproses.")
            return None

        data_tuple = self.antrian.dequeue()
        if data_tuple:
            removed_user_username, removed_user_join_time = data_tuple
            display_name = get_display_name(removed_user_username)
            
            print_info(f"Memproses: {AnsiColors.BOLD}{display_name} ({removed_user_username}){AnsiColors.ENDC}")
            time_str = "N/A"
            if isinstance(removed_user_join_time, datetime):
                time_str = removed_user_join_time.strftime("%Y-%m-%d %H:%M:%S")
            print_info(f"Bergabung pada: {time_str}")
            
            self.save_antrian()
            log_activity(actor_username, actor_role, "Memproses pengguna", f"Pengguna: {removed_user_username} ({display_name})")
            return removed_user_username
        return None

    def cetak_antrian(self, current_username_actor): # <<< Parameter added here
        if self.antrian.is_empty():
            print_info("\n📭 Antrean kosong! Tidak ada laporan untuk dicetak.\n")
            return

        report_file_name = "laporan_antrian.txt"
        print_info(f"\n📄 Mencetak Laporan Antrian ke Konsol dan File ({report_file_name})...")
        
        columns = ["No.", "Nama", "Username", "Waktu Masuk"]
        widths = [5, 25, 20, 20]
        
        print("") 
        print_table_header(columns, widths)

        user_position = -1
        total_in_queue = 0

        try:
            with open(report_file_name, "w", encoding="utf-8") as f:
                f.write("Laporan Antrian Bank MABSkuy\n")
                f.write(f"Dicetak pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                header_line = ""
                for col, w in zip(columns, widths): header_line += f"{col:<{w}} "
                f.write(header_line.strip() + "\n")
                f.write(f"{'-' * (sum(widths) + len(widths) -1)}\n")

                current_node = self.antrian.front
                idx = 1
                while current_node:
                    username_in_queue, join_time = current_node.data
                    display_name_val = get_display_name(username_in_queue)
                    time_str = "N/A"
                    if isinstance(join_time, datetime):
                        time_str = join_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    row_values = [idx, display_name_val, username_in_queue, time_str]
                    
                    # Highlight user's row in console and find position
                    row_display_color = ""
                    if username_in_queue == current_username_actor:
                        user_position = idx
                        row_display_color = AnsiColors.BOLD + AnsiColors.ORANGE 
                    
                    print_table_row(row_values, widths, row_color=row_display_color) 
                    
                    file_row_str = ""
                    for val, w in zip(row_values, widths): file_row_str += f"{str(val):<{w}} "
                    f.write(file_row_str.strip() + "\n")
                    
                    current_node = current_node.next
                    idx += 1
                
                total_in_queue = idx - 1 
                
                footer_line_console = f"{AnsiColors.BLUE}{'-' * (sum(widths) + len(widths) -1)}{AnsiColors.ENDC}"
                footer_line_file = f"{'-' * (sum(widths) + len(widths) -1)}"
                print(footer_line_console)
                f.write(footer_line_file + "\n")

            print_success(f"\n✅ Laporan berhasil disimpan ke {report_file_name}")

            # Print and append the special message for the logged-in user
            special_message_console = ""
            special_message_file = ""

            if user_position != -1:
                special_message_console = f"ANDA DI POSISI {AnsiColors.BOLD}{user_position}{AnsiColors.ENDC} DARI {AnsiColors.BOLD}{total_in_queue}{AnsiColors.ENDC} ORANG!"
                special_message_file = f"ANDA DI POSISI {user_position} DARI {total_in_queue} ORANG!"
                print_success(special_message_console)
            else:
                actor_display_name = get_display_name(current_username_actor)
                special_message_console = f"Anda ({AnsiColors.BOLD}{actor_display_name}{AnsiColors.ENDC}) saat ini tidak berada dalam antrean."
                special_message_file = f"Anda ({actor_display_name}) saat ini tidak berada dalam antrean."
                print_info(special_message_console)
            
            with open(report_file_name, "a", encoding="utf-8") as f_append:
                f_append.write("\n\nCatatan Pribadi Pengguna:\n")
                f_append.write(special_message_file + "\n")
            print("") # Extra newline for console

        except IOError:
            print_error(f"\n❌ Gagal menulis laporan ke file {report_file_name}.\n")


    def cari_nama_orang_antre(self, nama_username_to_find):
        current = self.antrian.front
        posisi = 1
        found = False
        while current:
            username_in_queue, join_time = current.data
            if username_in_queue == nama_username_to_find:
                display_name = get_display_name(username_in_queue)
                time_str = "N/A"
                if isinstance(join_time, datetime): time_str = join_time.strftime('%Y-%m-%d %H:%M:%S')
                print_success(f"Pengguna {AnsiColors.BOLD}{display_name} ({username_in_queue}){AnsiColors.ENDC} ditemukan pada antrean nomor {AnsiColors.BOLD}{posisi}{AnsiColors.ENDC}.")
                print_info(f"Bergabung pada: {time_str}")
                found = True
                break # Found, no need to continue
            current = current.next
            posisi += 1
        if not found:
            print_error(f"Pengguna {nama_username_to_find} tidak ditemukan dalam antrean.")

    def update_antrean(self, index1, index2, actor_username, actor_role):
        all_data_tuples = self.antrian.get_all_items_with_timestamps()

        if not (0 <= index1 < len(all_data_tuples) and 0 <= index2 < len(all_data_tuples)):
            print_error("Indeks tidak valid! Harap masukkan nomor antrian yang benar.")
            return
        
        if index1 == index2:
            print_warning("Indeks tidak boleh sama.")
            return

        user1_tuple = all_data_tuples[index1]
        user2_tuple = all_data_tuples[index2]

        all_data_tuples[index1], all_data_tuples[index2] = all_data_tuples[index2], all_data_tuples[index1]

        self.antrian = LinkedListQueue()
        for item_tuple in all_data_tuples:
            self.antrian.enqueue(item_tuple[0], timestamp=item_tuple[1])

        user1_display = get_display_name(user1_tuple[0])
        user2_display = get_display_name(user2_tuple[0])
        print_success(f"Urutan antrean {AnsiColors.BOLD}{user1_display}{AnsiColors.ENDC} dan {AnsiColors.BOLD}{user2_display}{AnsiColors.ENDC} berhasil ditukar.")
        self.save_antrian()
        log_activity(actor_username, actor_role, "Tukar posisi antrean", f"Antara '{user1_tuple[0]}' (pos {index1+1}) dan '{user2_tuple[0]}' (pos {index2+1})")