# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): ...
- Cara memperbaikinya: ...

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|24/11/2026|Gemini|bagaimana konsep umum consistent hashing/Chord|Consistent Hashing adalah teknik distribusi data di sistem terdistribusi yang memetakan node (server) dan key (data) ke dalam ruang alamat berbentuk lingkaran (hash ring) agar perubahan jumlah server tidak memicu perpindahan data besar-besaran. Chord adalah protokol Peer-to-Peer (P2P) berbasis Distributed Hash Table (DHT) yang mengimplementasikan consistent hashing sekaligus menambahkan mekanisme routing cepat agar setiap node bisa menemukan lokasi data secara efisien tanpa server pusat.|Memahami konsep dari consistent hash/chord|
|24/112026| Gemini | berikan contoh implementasi dari bagaimana konsep umum consistent hashing/Chord | Berikut adalah implementasi sederhana Consistent Hashing dan Chord menggunakan Python. Simulasi ini menggunakan ruang cincin berukuran $m = 4$ (ID $0$ sampai $15$) agar struktur Finger Table dan jejak lompatan (hops) saat lookup mudah diamati. | memahami alur code dan menyesuaikannya |
