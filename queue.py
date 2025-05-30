# queue.py
from utils import get_display_name
from datetime import datetime # Added for timestamping

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
            if current.data[0] == item_to_check: # Check only the item part of the tuple
                return True
            current = current.next
        return False

    def enqueue(self, item, timestamp=None):
        if self.exists(item): # Check if item (e.g., username) already exists
            print(f"Peringatan: {item} sudah ada dalam antrean.")
            return

        join_time = timestamp if timestamp is not None else datetime.now()
        new_node = Node((item, join_time)) # Store as a tuple

        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def enqueue_prioritas(self, item, timestamp=None):
        if self.exists(item):
            print(f"Peringatan: {item} sudah ada dalam antrean prioritas.")
            return

        join_time = timestamp if timestamp is not None else datetime.now()
        new_node = Node((item, join_time)) # Store as a tuple

        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front = new_node

    def dequeue(self):
        if self.is_empty():
            # print("Antrean kosong!") # Usually handled by caller
            return None
        removed_data_tuple = self.front.data # This is (item, timestamp)
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return removed_data_tuple

    def display(self):
        if self.is_empty():
            print("\n📭 Antrean kosong!\n")
            return

        print("\n🧾 Daftar Antrean Saat Ini")
        print("=" * 42)
        print(f"{'No.':<5} {'Nama':<20} {'Username':<15}")
        print("-" * 42)

        idx = 1
        current = self.front
        while current:
            username = current.data[0] # Actual item is the first element of the tuple
            display_name_val = get_display_name(username)
            print(f"{idx:<5} {display_name_val:<20} {username:<15}")
            current = current.next
            idx += 1
        print("-" * 42)

    def remove_item(self, item_to_remove):
        if self.is_empty():
            return False

        # If the item to remove is at the front
        if self.front.data[0] == item_to_remove:
            self.dequeue()
            return True

        current = self.front
        while current.next:
            if current.next.data[0] == item_to_remove:
                removed_node_ref = current.next
                current.next = current.next.next
                if current.next is None: # If the removed node was the rear
                    self.rear = current
                # del removed_node_ref # Optional: Python's GC will handle it
                return True
            current = current.next
        return False # Item not found

    def get_all_items_with_timestamps(self):
        items = []
        current = self.front
        while current:
            items.append(current.data) # Appends the (item, timestamp) tuple
            current = current.next
        return items

    def get_item_data_at_index(self, index):
        current = self.front
        count = 0
        while current:
            if count == index:
                return current.data # Returns (item, timestamp)
            count += 1
            current = current.next
        return None # Index out of bounds