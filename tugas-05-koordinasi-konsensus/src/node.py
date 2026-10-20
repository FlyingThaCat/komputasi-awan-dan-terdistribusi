"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) harus kalian lengkapi sendiri.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        self.ok_received = threading.Event()

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (LENGKAPI BAGIAN INI) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        if msg_type == "ELECTION":
            if self.node_id > sender_id:
                sender_port = self.peers.get(sender_id)
                if sender_port is None:
                    print(f"[Node {self.node_id}] Peer node {sender_id} tidak dikenal")
                    return

                self.send_message(sender_port, "OK")
                self.start_election()
            return

        if msg_type == "OK":
            self.ok_received.set()
            print(f"[Node {self.node_id}] Menerima OK dari node {sender_id}")
            return

        if msg_type == "COORDINATOR":
            with self.lock:
                self.leader_id = sender_id
            print(f"[Node {self.node_id}] Leader baru: node {sender_id}")
            return

        if msg_type == "PING":
            return

        print(f"[Node {self.node_id}] Pesan tidak dikenal '{msg_type}' dari node {sender_id}")

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
        self.ok_received.clear()
        print(f"[Node {self.node_id}] Memulai election ke peer lebih tinggi: {higher_peers}")

        for peer_id, peer_port in higher_peers.items():
            if self.send_message(peer_port, "ELECTION"):
                print(f"[Node {self.node_id}] ELECTION terkirim ke node {peer_id}")
            else:
                print(f"[Node {self.node_id}] Node {peer_id} tidak merespons")

        if self.ok_received.wait(ELECTION_TIMEOUT):
            print(f"[Node {self.node_id}] Menerima OK; menunggu COORDINATOR")
            return

        self.declare_leader()

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] Menjadi leader; broadcast COORDINATOR")

        for peer_id, peer_port in self.peers.items():
            if self.send_message(peer_port, "COORDINATOR"):
                print(f"[Node {self.node_id}] COORDINATOR terkirim ke node {peer_id}")
            else:
                print(f"[Node {self.node_id}] Node {peer_id} tidak merespons")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            with self.lock:
                leader_id = self.leader_id

            if leader_id is None or leader_id == self.node_id:
                continue

            leader_port = self.peers.get(leader_id)
            if leader_port is not None and self.send_message(leader_port, "PING"):
                continue

            with self.lock:
                if self.leader_id == leader_id:
                    self.leader_id = None

            print(f"[Node {self.node_id}] Leader node {leader_id} tidak merespons")
            self.start_election()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    # Asumsi konvensi port: id N selalu di port 5000+N (lihat contoh perintah di README).
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  # beri waktu semua node lain start dulu sebelum election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
