# Jurnal Proses — Tugas 2

## Selasa, 20 Oktober 2026
- Opsi arsitektur yang dipertimbangkan: SOA dan Publish-Subscribe
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Karena FoodGo membutuhkan sistem yang setiap layanannya tidak terlalu bergantung satu sama lain dan bisa saling bertukar informasi melalui message broker
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Memisahkan alur komunikasi langsung dan melalui message broker agar hubungan antarlayanan lebih mudah dipahami

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20 Oktober 2026 | ChatGPT | Apa bedanya SOA dan Publish-Subscribe? | SOA memisahkan layanan, sedangkan Publish-Subscribe mengatur komunikasi melalui message broker. | Memahami perbedaan keduanya untuk menentukan arsitektur FoodGo. |
| 20 Oktober 2026 | ChatGPT | Bagaimana cara membuat diagram arsitektur FoodGo? | Diagram perlu menunjukkan layanan yang digunakan dan hubungan komunikasinya. | Menyesuaikan diagram dengan alur pemesanan FoodGo. |
| 20 Oktober 2026 | ChatGPT | Kenapa SOA dan Publish-Subscribe cocok untuk FoodGo? | Keduanya membantu mengurangi ketergantungan antarlayanan, tetapi memiliki kekurangan seperti debugging yang lebih sulit. | Menggunakan penjelasan tersebut untuk menyusun analisis sesuai studi kasus FoodGo. |
| 20 Oktober 2026 | ChatGPT | Bagaimana alur komunikasi saat pelanggan memesan makanan di FoodGo? | Validasi menu menggunakan komunikasi langsung, sedangkan pembaruan status dan notifikasi menggunakan message broker. | Menyesuaikan alur komunikasi dengan diagram proses pemesanan. |
