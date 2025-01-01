fn main() {
    // Arrays: Koleksi elemen dengan tipe data yang sama yang disimpan secara berurutan di memori
    // Mendeklarasikan array, menginisialisasi semua nilainya, dan membiarkan compiler menentukan panjangnya
    let working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    
    // Mendeklarasikan array, menginisialisasi semua nilai dengan 0, dan menentukan panjangnya (5 elemen)
    let working_days_num = [0; 5];
    
    // Mengakses elemen array menggunakan indeks
    println!("First working day: {}", working_days[0]); // Mengakses elemen pertama (indeks 0)

    // Vectors: Koleksi elemen dengan tipe data yang sama, namun lebih fleksibel dibandingkan array
    // Mendeklarasikan vector dan menginisialisasi semua nilainya
    let nephews_age = vec![14, 9, 0];
    println!("Nephews' ages: {:?}", nephews_age); // Mencetak semua elemen vector
    
    // Mendeklarasikan vector, menginisialisasi semua elemen dengan 0, dan menentukan panjangnya (5 elemen)
    let zeroes = vec![0; 5];
    println!("Zeroes vector: {:?}", zeroes); // Mencetak vector yang berisi nilai nol
    
    // Menambahkan atau menghapus elemen dalam vector menggunakan metode `push` atau `pop`
    let mut names = Vec::new(); // Membuat vector kosong yang dapat diubah

    names.push("Will");  // Menambahkan elemen ke dalam vector
    names.push("Isaac"); // Menambahkan elemen lain
    names.push("Sam");   // Menambahkan elemen ketiga
    println!("Names: {:?}", names); // Mencetak semua elemen vector

    names.pop(); // Menghapus elemen terakhir dari vector
    println!("Names after pop: {:?}", names); // Mencetak elemen vector setelah penghapusan

    // Mengakses elemen dalam vector berdasarkan indeks
    let mut fruit = vec!["Apple", "Melon", "Orange"]; // Membuat vector dengan beberapa elemen
    let orange = fruit[2]; // Menyimpan elemen pada indeks ke-2 (Orange) ke variabel `orange`
    fruit[0] = "Strawberry"; // Mengganti elemen pertama (indeks 0) dengan "Strawberry"
    println!("Fruits: {:?}, Orange = {}", fruit, orange); // Mencetak vector dan elemen Orange
}