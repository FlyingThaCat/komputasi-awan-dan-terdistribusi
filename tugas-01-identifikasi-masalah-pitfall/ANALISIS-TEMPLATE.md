# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 3

| Nama | NIM | Kontribusi |
|---|---|---|
| I Made Sudiarte | [nim] | [pitfall/bagian yang dikerjakan] |
| John Tjandra Utomo | 103072400023 | [pitfall/bagian yang dikerjakan] |
| Ivan  | [nim] | [pitfall/bagian yang dikerjakan] |
| Lilo Wahyu Rachmadani | 103072400126 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: "network is always reliable" — ditulis oleh John Tjandra Utomo

**Bukti di skenario:** [Kutipan](https://github.com/FlyingThaCat/komputasi-awan-dan-terdistribusi/tree/main/tugas-01-identifikasi-masalah-pitfall#studi-kasus-foodgo) Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service "modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu".

**Kenapa ini keliru:** di sistem cloud / distributed, setiap server pasti melewati jaringan yang dapat kehilangan paket meskipun di hosting sekelas aws dan cloudflare kita dapat melihat berita akhir-akhir ini yang membicarakan tentang down / tumbangnya cloudflare dan beberapa infrastruktur aws terkena serangan militer [aws health](https://health.aws.amazon.com/health/status) [berita](https://www.cnbc.com/2026/09/15/aws-cant-restore-service-to-bahrain-uae-6-months-after-iran-strikes.html) dari sini kita dapat menyimpulkan bahwa cloud solution belum tentu aman dan reliable dan kebanyakan website menggunakan dns yang dimana dns sendiri dapat menjadi point of failure seperti yang terjadi pada facebook pada beberapa tahun terakhir [berita](https://blog.cloudflare.com/october-2021-facebook-outage/#meet-bgp)

**Dampak ke FoodGo:** saat jam makan siang, panggilan ke modul pembayaran yang gagal sementara, langsung dianggap gagal pesan, karena tidak ada retry. Pelanggan hanya melihat error. Pesanan dibatalkan atau hilang dan pelanggan mengulang pemesanan secara manual, yang menambah beban.

**Solusi desain awal:** tambahkan retry terbatas (maksimal 2-3 kali) dengan jeda yang bertambah agar client tidak melakukan retry secara serentak dan lebih terasa random. dan ada baiknya setiap request memiliki id pesanan sehingga pembayaran yang sama tidak diproses dua kali

**Trade-off:** retry bisa memperparah overload karena kita membuat 3x request yang dapat meledak. latensi pun juga dapat bertambah karena setiap retry request yang gagal kita menambah random delay. dan tidak selalu cocok untuk segala masalah (saldo tidak cukup / data tidak valid)

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 4: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---


## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
