# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal diskusi 1]
- Peserta: 
    - John Tjandra Utomo | 103072400023 
    - Lilo Wahyu Rachmadani | 103072400126 
    - Ivan Radithya Tanaya Ardianto | 103072430005
    -  I Made Sudiarte | 103072400044
<br>
- Poin diskusi: Diskusi berfokus pada analisis penyebab dari startup aplikasi FoodGo mengalami kegagalan sistem di mana aplikasi menjadi lambat, dan server backend yang mengalami crash, mengidentifikasi pitfall utama yang dialami FoodGo,  menganalisis asumsi dari pitfall, dampak yang ditimbulkan akibat asumsi yang keliru, setelah itu mencari solusi untuk permasalah tersebut dan menentukan komponen apa yang akan dikorbankan untuk menerapkan solusi yang dikasih.
- Perbedaan pendapat (jika ada): -

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 October 2026 | claude | apakah network reliable selalu benar? | Jaringan memang sering berhasil, bahkan 99,9% dari waktu. Tapi kegagalan tetap pasti terjadi suatu saat, dan sistem terdistribusi yang dipakai banyak orang pasti mengalaminya. Penyebabnya antara lain: 1.Paket hilang atau terlambat. 2.Koneksi putus, atau DNS gagal resolve. 3.Switch atau router bermasalah. 4.Service tujuan restart atau overload, sehingga dari sisi pemanggil terlihat sama seperti jaringan gagal. | memberikan study case dan bukti pada masalah yang pernah terjadi pada perusahaan besar |
