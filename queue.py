# queue.py
from utils import get_display_name

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def exists(self, data):
        current = self.front
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def enqueue(self, data):
        if self.exists(data):
            return
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def enqueue_prioritas(self, data):
        if self.exists(data):
            return
        new_node = Node(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front = new_node

    def dequeue(self):
        if self.is_empty():
            print("Antrean kosong!")
            return None
        removed = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return removed

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
            uname = current.data
            dname = get_display_name(uname)
            nomor = f"{idx:02d}"
            print(f"{nomor:<5} {dname:<20} {uname:<15}")
            current = current.next
            idx += 1

        print("=" * 42)
        print("🔚 Antrian Selesai\n")
 # type: ignore