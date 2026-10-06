# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 3

| Nama | NIM | Kontribusi |
|---|---|---|
| I Made Sudiarte | 103072400044 | [pitfall/bagian yang dikerjakan] |
| John Tjandra Utomo | 103072400023 | [pitfall/bagian yang dikerjakan] |
| Ivan Radithya Tanaya Ardianto | 103072430005 | [pitfall/bagian yang dikerjakan] |
| Lilo Wahyu Rachmadani | 103072400126 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: "network is always reliable" — ditulis oleh John Tjandra Utomo

**Bukti di skenario:** [Kutipan](https://github.com/FlyingThaCat/komputasi-awan-dan-terdistribusi/tree/main/tugas-01-identifikasi-masalah-pitfall#studi-kasus-foodgo) Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service "modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu".

**Kenapa ini keliru:** di sistem cloud / distributed, setiap server pasti melewati jaringan yang dapat kehilangan paket meskipun di hosting sekelas aws dan cloudflare kita dapat melihat berita akhir-akhir ini yang membicarakan tentang down / tumbangnya cloudflare dan beberapa infrastruktur aws terkena serangan militer [aws health](https://health.aws.amazon.com/health/status) [berita](https://www.cnbc.com/2026/09/15/aws-cant-restore-service-to-bahrain-uae-6-months-after-iran-strikes.html) dari sini kita dapat menyimpulkan bahwa cloud solution belum tentu aman dan reliable dan kebanyakan website menggunakan dns yang dimana dns sendiri dapat menjadi point of failure seperti yang terjadi pada facebook pada beberapa tahun terakhir [berita](https://blog.cloudflare.com/october-2021-facebook-outage/#meet-bgp)

**Dampak ke FoodGo:** saat jam makan siang, panggilan ke modul pembayaran yang gagal sementara, langsung dianggap gagal pesan, karena tidak ada retry. Pelanggan hanya melihat error. Pesanan dibatalkan atau hilang dan pelanggan mengulang pemesanan secara manual, yang menambah beban.

**Solusi desain awal:** tambahkan retry terbatas (maksimal 2-3 kali) dengan jeda yang bertambah agar client tidak melakukan retry secara serentak dan lebih terasa random. dan ada baiknya setiap request memiliki id pesanan sehingga pembayaran yang sama tidak diproses dua kali

**Trade-off:** retry bisa memperparah overload karena kita membuat 3x request yang dapat meledak. latensi pun juga dapat bertambah karena setiap retry request yang gagal kita menambah random delay. dan tidak selalu cocok untuk segala masalah (saldo tidak cukup / data tidak valid)

---

## Pitfall 2: Latency is Zero — ditulis oleh Lilo Wahyu Rachmadani

**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout." dan "... tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)."


**Kenapa ini keliru**: Asumsi bahwa latency is zero merupakan analisa yang keliru, karena komunikasi melalui jaringan tidak pernah terjadi secara instan (0 milidetik). Pengiriman data selalu membutuhkan waktu untuk melalui jaringan (seperti kabel dan router), serta sangat bergantung pada kecepatan pemrosesan dan kondisi server tujuan. 

**Dampak ke FoodGo**: Ketiadaan timeout membuat thread di modul pesanan terhenti (mengalami blocking) karena terus menunggu respon dari modul pembayaran tanpa batas waktu. Saat jam makan siang, penumpukkan thread yang menggantung ini dapat menghabiskan kapasitas pemrosesan server (thread exhaustion), sehingga aplikasi berjalan dengan sangat lambat. pesanan baru bertumpuk, dan proses server akhirnya mengalami crash secara menyeluruh.  

**Solusi desain awal:** 
1. Memasang timeout (batas waktu) sehingga saat tidak ada respons dalam kurun waktu tertentu, sistem akan langsung memutus koneksi secara sepihak dan membebaskan thread server.
2. Jika terjadi kegagalan berturut-turut pada pemanggilan modul pembayaran, maka request pemanggilan berikutnya akan ditolak dengan cepat tanpa membebani server.


**Trade-off:** FoodGo mengorbankan potensi pendapatan dari pengguna dan waktu atau kenyamanan pengguna saat terjadi gangguan demi mencegah server mati total (crash). Sistem lebih memilih menolak sebagian transaksi dengan cepat (fail-fast) daripada membiarkan seluruh aplikasi lumpuh untuk semua pengguna.

---

## Pitfall 3: Single Point of Failure dan Skalabilitas Buruk — ditulis oleh Ivan Radithya Tanaya Ardianto

**Bukti di skenario:** Dari [kutipan](https://github.com/FlyingThaCat/komputasi-awan-dan-terdistribusi/tree/main/tugas-01-identifikasi-masalah-pitfall#studi-kasus-foodgo) ini "satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.". Saat traffic padat, ditemukan satu server yang menangani banyak modul yang berjalan dalam satu proses monolik yang sama.


**Kenapa ini keliru:** Hal tersebut tentu saja melanggar tujuan dari skalabilitas, di mana jika suatu modul sedang padat, modul tersebut boleh hanya diperbesar. Tetapi juga harus meningkatkan seluruh spesifikasi server (_vertical scaling_) atau dengan menduplikasi seluruh aplikasi beserta modul-modul yang sedang sepi. Dengan satu proses bisa diartikan juga satu failure domain, yang dapat berakibat pada kerusakan system. Termasuk bug, kebocoran memori, atau lonjakan beban akibat satu modul menjatuhkan semuanya. Skala juga tidak diatur per modul, kenyataannya kebutuhan pada setiap modul berbeda.

**Dampak ke FoodGo:** Saat melakukan pembayaran atau transaksi bisa terjadi macet atau _crash_, diikuti dengan modul notifikasi kurir yang ikut mati. Pesanan yang sudah dibayar tidak sampai ke kurir, menjadikan masalah yang makin meluas dari pembayaran ke seluruh operasional (seperti upgrade server). Karena hanya ada satu server, tidak ada instance cadangan yang dapat mengambil alih, sehingga restart manual harus dilakukan.

**Solusi desain awal:**
- Jalankan beberapa instance di balik _load balancer_ dengan _health check_ (skala horizontal), sehingga saat satu instance mati, tidak akan mematikan layanan atau modul lain. 
- Pisahkan modul secara bertahap, mulai dari yang paling beresiko sepeerti pembayaran dan notifikasi yang dijadikan service terpisah. Tidak perlu langsung memecah semuanya menjadi microservice.
- Jadikan notifikasi kurir secara asinkron lewat _message queque_, agar pesanan tidak menunggu notifikasi dan lonjakan beban yang bisa diserap oleh antrean.

**Trade-off:** Setelah modul dipisahkan, interaksi antar modul berubah dari pemanggilan fungsi lokal menjadi _network call_. FoodGo jutru makin terdampak Fallacies yang sama (seperti latensi dan kegagalan parsial) dan beban operasional yang naik (seperti deployment, monitoring, dan debugging terdistribusi). Itu sebabnya disarankan pemisahan bertahap, bukan langsung microservice penuh.

---

## Pitfall 4: Asumsi kapasitas tak terbatas (tidak ada backpressure dan load shedding) — ditulis oleh I Made Sudiarte

**Bukti di skenario:** "Saat jam makan siang, banyak orang memesan makanan secara bersamaan contoh (100000 orang)". System API pesanan akan langsung meneruskan dan memproses seluruh request pesanan tersebut dari pengguna ke database secara real-time tanpa ada Batasan untuk jumlah requestnya.

**Kenapa ini keliru:** Sistem dibangun dengan asumsi bahwa database mereka kuat memproses 100000 request secara bersamaan, padahal pada umumnya database hanya bisa memproses 10000 request jika requestnya dikirim secara bersamaan.

**Dampak ke FoodGo:** Permintaan pesanan akan menumpuk, database akan mengalami error "connection timeout", server aplikasi akan kehabisan memori akibat permintaan pesanan melebihi batas normal proses pada database. serta latency aplikasi mengalami kenaikan secara drastis yang menyebabkan sistem aplikasi mengalami crash.

**Solusi desain awal:** Terapkan ratte limmiting di API Gateway, agar jika kapasitas permintaan penuh sistem akan melakukan load shedding dimana API Gateway akan langsung menolak pesanan baru yang masuk. dan terapkan sistem queue (message queue), setiap pesanan yang masuk akan ditaruh diantian dulu sebelum diproses lalu database akan langsung memprosesnya satu-satu.

**Trade-off:** karena menggunakan sistem antrian, pesanan tidak lagi langsung diproses/instan serta sistem akan menjadi lebih rumit dan mahal karena menambah komponen baru di server, pesanan akan mengalami sedikit keterlambatan, saat sistem melakukan load shedding ada kemungkinan pelanggan yang tadinya ingin memesan makanan dan pesanannya ditolak karena kapasitas permintaan penuh memutuskan tidak jadi memesan.

---


## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
