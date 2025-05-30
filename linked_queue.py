# queue.py
from utils import get_display_name, print_info, print_warning, AnsiColors, print_table_header, print_table_row
from datetime import datetime

class Node:
    def __init__(self, data_tuple): # data_tuple will be (item, timestamp)
        self.data = data_tuple
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def exists(self, item_to_check):
        current = self.front
        while current:
            if current.data[0] == item_to_check:
                return True
            current = current.next
        return False

    def enqueue(self, item, timestamp=None):
        if self.exists(item):
            display_name = get_display_name(item)
            print_warning(f"Pengguna {display_name} ({item}) sudah ada dalam antrean.")
            return "exists" # Return status

        join_time = timestamp if timestamp is not None else datetime.now()
        new_node = Node((item, join_time))

        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        return "success" # Return status

    def enqueue_prioritas(self, item, timestamp=None):
        if self.exists(item):
            display_name = get_display_name(item)
            print_warning(f"Pengguna {display_name} ({item}) sudah ada dalam antrean (prioritas tidak ditambahkan).")
            return "exists"

        join_time = timestamp if timestamp is not None else datetime.now()
        new_node = Node((item, join_time))

        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front = new_node
        return "success"

    def dequeue(self):
        if self.is_empty():
            # Caller (features.py) will handle printing "Antrean kosong"
            return None
        removed_data_tuple = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return removed_data_tuple

    def display(self):
        if self.is_empty():
            print_info("\n📭 Antrean kosong!\n")
            return

        print_info("\n🧾 Daftar Antrean Saat Ini")
        columns = ["No.", "Nama", "Username", "Waktu Masuk"]
        widths = [5, 25, 20, 20]
        print_table_header(columns, widths)

        idx = 1
        current = self.front
        while current:
            username, join_time = current.data
            display_name_val = get_display_name(username)
            time_str = "N/A"
            if isinstance(join_time, datetime):
                time_str = join_time.strftime("%Y-%m-%d %H:%M:%S")
            
            row_values = [idx, display_name_val, username, time_str]
            # Alternate row colors slightly for readability if desired, e.g.
            # row_color = AnsiColors.CYAN if idx % 2 == 0 else "" 
            print_table_row(row_values, widths) #, row_color=row_color) 
            
            current = current.next
            idx += 1
        print(f"{AnsiColors.BLUE}{'-' * (sum(widths) + len(widths) -1)}{AnsiColors.ENDC}")
        print("") # Newline at the end


    def remove_item(self, item_to_remove):
        if self.is_empty():
            return False

        if self.front.data[0] == item_to_remove:
            self.dequeue()
            return True

        current = self.front
        while current.next:
            if current.next.data[0] == item_to_remove:
                current.next = current.next.next
                if current.next is None:
                    self.rear = current
                return True
            current = current.next
        return False

    def get_all_items_with_timestamps(self):
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items

    def get_item_data_at_index(self, index): # index is 0-based
        current = self.front
        count = 0
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next
        return None