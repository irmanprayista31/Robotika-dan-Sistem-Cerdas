fn main() {
    // Mendefinisikan sebuah vektor yang berisi probabilitas untuk berbagai jalur
    let probabilities = vec![0.8, 0.6, 0.4, 0.9];
    
    // Vektor yang akan menyimpan indeks-indeks jalur dengan probabilitas lebih besar dari 0.7
    let mut best_path = vec![];

    // Iterasi melalui setiap elemen dalam vektor probabilities
    for (i, &prob) in probabilities.iter().enumerate() {
        // Jika probabilitas lebih besar dari 0.7, tambahkan indeks ke vektor best_path
        if prob > 0.7 {
            best_path.push(i);
        }
    }

    // Menampilkan hasil indeks-indeks jalur yang memiliki probabilitas lebih besar dari 0.7
    println!("Best path indices: {:?}", best_path);
}
