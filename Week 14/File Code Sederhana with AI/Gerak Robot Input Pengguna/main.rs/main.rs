// Mengimpor pustaka input/output dari standar pustaka untuk membaca input dari pengguna
use std::io;

fn main() {
    // Menetapkan posisi awal sebagai tuple (0, 0)
    let mut position = (0, 0);

    // Mulai loop yang akan terus berjalan sampai pengguna memilih untuk keluar
    loop {
        // Menampilkan posisi saat ini
        println!("Current position: {:?}", position);

        // Meminta pengguna untuk memasukkan pergerakan atau 'q' untuk keluar
        println!("Enter movement (format: x y, or 'q' to quit):");

        // Membaca input pengguna sebagai string
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        // Jika input adalah 'q', keluar dari loop
        if input.trim() == "q" {
            break;
        }

        // Memisahkan input berdasarkan spasi dan mencoba mengonversinya menjadi integer
        let parts: Vec<i32> = input
            .trim() // Menghapus spasi kosong di awal dan akhir input
            .split_whitespace() // Memisahkan string input berdasarkan spasi
            .filter_map(|x| x.parse().ok()) // Mengonversi setiap bagian menjadi integer, jika gagal mengabaikan bagian tersebut
            .collect();

        // Jika ada dua angka yang valid (x dan y), perbarui posisi
        if parts.len() == 2 {
            position.0 += parts[0]; // Menambahkan x ke posisi horizontal
            position.1 += parts[1]; // Menambahkan y ke posisi vertikal
        } else {
            // Jika input tidak terdiri dari dua angka, beri tahu pengguna bahwa inputnya tidak valid
            println!("Invalid input, please enter two integers.");
        }
    }
}
