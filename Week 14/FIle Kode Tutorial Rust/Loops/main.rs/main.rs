fn main() {
    // Menggunakan pernyataan `break` untuk menghentikan loop.
    // Dengan `break`, kita bisa menghentikan loop dan juga mengembalikan nilai pada titik henti.
    let mut counter = 1; // Mendeklarasikan variabel counter dengan nilai awal 1
    let loop_stop = loop {
        counter *= 4; // Melipatgandakan nilai counter dengan 4 di setiap iterasi
        if counter > 100 {
            break counter; // Menghentikan loop dan mengembalikan nilai counter
        }
    };

    println!("Break the loop at counter = {}", loop_stop); // Mencetak nilai counter pada titik henti

    // While loop: Menggunakan ekspresi kondisi untuk menentukan kapan loop berhenti.
    // Loop akan terus berjalan selama ekspresi kondisi bernilai true.
    let mut num = 0; // Inisialisasi variabel num dengan nilai awal 0
    while num < 10 {
        println!("Hello there!"); // Mencetak pesan selama kondisi terpenuhi
        num = num + 1; // Menambahkan 1 ke variabel num pada setiap iterasi
    }

    // For loop: Menggunakan iterator untuk memproses koleksi item.
    let shopping_list = ["milk", "cheese", "bread", "apples"]; // Daftar belanja sebagai array

    // Nilai dari iterator diambil menggunakan metode `iter()`.
    for item in shopping_list.iter() {
        println!("The next item on my shopping is {}", item); // Mencetak setiap item dalam daftar belanja
    }

    // Membuat iterator dengan notasi rentang (range) a..b
    // Iterator dimulai dari nilai `a` dan berhenti pada nilai sebelum `b` (nilai `b` tidak termasuk).
    for number in 0..10 {
        println!("Number {}", number); // Mencetak angka dari 0 hingga 9
    }
}
