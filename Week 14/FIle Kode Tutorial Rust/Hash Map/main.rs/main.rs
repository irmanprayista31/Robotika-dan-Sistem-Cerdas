fn main() {
    // Perintah 'use' digunakan untuk membawa definisi HashMap dari bagian 'collections' pada pustaka standar Rust.
    use std::collections::HashMap;

    // Membuat hash map kosong menggunakan metode HashMap::new().
    // HashMap di sini menggunakan tipe data key dan value berupa String.
    let mut items: HashMap<String, String> = HashMap::new();

    // Menambahkan elemen ke dalam hash map menggunakan metode .insert(<key>, <value>).
    items.insert(String::from("One"), String::from("Book")); // Menambahkan pasangan key-value ("One", "Book").
    items.insert(String::from("Two"), String::from("Keyboard")); // Menambahkan pasangan key-value ("Two", "Keyboard").
    items.insert(String::from("Three"), String::from("Sunglasses")); // Menambahkan pasangan key-value ("Three", "Sunglasses").

    // Mengambil nilai tertentu dari hash map berdasarkan key menggunakan metode .get(<key>).
    // Metode ini mengembalikan nilai bertipe Option<&V> (dapat berupa Some(value) atau None).
    let keyboard = items.get("Two"); // Mengambil nilai untuk key "Two".
    println!("{:?}", keyboard); // Mencetak hasil (Some("Keyboard")).

    // Menghapus entri dari hash map menggunakan metode .remove(<key>).
    // Jika key dihapus, mencoba mengambil nilai dengan key tersebut akan mengembalikan 'None'.
    items.remove("Three"); // Menghapus entri dengan key "Three".
    
    // Mencoba mengambil nilai untuk key "Three" setelah dihapus.
    println!("{:?}", items.get("Three")); // Hasilnya adalah None.
}
