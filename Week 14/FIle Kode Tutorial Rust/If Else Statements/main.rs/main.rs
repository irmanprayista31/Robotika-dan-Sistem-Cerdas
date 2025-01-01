fn main() {
    // Pernyataan if/else dasar
    // Mengecek apakah 1 sama dengan 2
    if 1 == 2 {
        println!("The numbers are equal"); // Jika kondisinya benar, cetak "The numbers are equal"
    } else {
        println!("The numbers are not equal"); // Jika kondisinya salah, cetak "The numbers are not equal"
    }

    // Mengikat nilai ke variabel menggunakan pernyataan if/else
    let sunny_day = true; // Mendeklarasikan bahwa hari cerah
    let take_jacket = if sunny_day {
        "Don't take a jacket" // Jika hari cerah, tidak perlu membawa jaket
    } else {
        "Take a jacket" // Jika tidak cerah, membawa jaket
    };

    println!("{}", take_jacket); // Mencetak pesan sesuai kondisi cuaca

    // Menggunakan beberapa pernyataan if/else untuk mengevaluasi beberapa kondisi
    let num = 100; // Mendeklarasikan variabel num dengan nilai 100
    let out_of_range: bool; // Deklarasi variabel boolean untuk menyimpan hasil kondisi

    if num < 0 {
        // Jika nilai num kurang dari 0
        out_of_range = true; // Set variabel out_of_range menjadi true
    } else if num == 0 {
        // Jika nilai num sama dengan 0
        out_of_range = true; // Set variabel out_of_range menjadi true
    } else if num > 101 {
        // Jika nilai num lebih dari 101
        out_of_range = true; // Set variabel out_of_range menjadi true
    } else {
        // Jika tidak memenuhi kondisi di atas
        out_of_range = false; // Set variabel out_of_range menjadi false
    }
    println!("{}", out_of_range); // Mencetak nilai dari out_of_range
}
