// Mengimpor pustaka untuk mengelola saluran (mpsc), thread, dan pengaturan durasi waktu
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    // Membuat saluran (channel) yang digunakan untuk komunikasi antar thread
    // tx adalah pengirim (sender), dan rx adalah penerima (receiver)
    let (tx, rx) = mpsc::channel();

    // Membuat thread baru untuk mensimulasikan pengiriman event secara periodik
    thread::spawn(move || {
        // Mendefinisikan beberapa event yang akan dikirim
        let events = vec!["Obstacle detected", "Goal changed"];
        
        // Mengirim setiap event melalui saluran
        for event in events {
            tx.send(event).unwrap(); // Mengirim event melalui tx
            thread::sleep(Duration::from_secs(2)); // Menunggu selama 2 detik sebelum mengirim event berikutnya
        }
    });

    // Menerima dan menampilkan event yang diterima dari saluran
    while let Ok(event) = rx.recv() {
        // Mencetak event yang diterima ke layar
        println!("Event received: {}", event);
    }
}
