// Mengimpor BinaryHeap dari pustaka standard
use std::collections::BinaryHeap;

// Mendefinisikan struktur Task untuk merepresentasikan sebuah tugas
#[derive(Eq, PartialEq)] // Memungkinkan untuk membandingkan dua tugas dengan menggunakan equality
struct Task {
    priority: i32,         // Menyimpan nilai prioritas tugas
    description: String,   // Menyimpan deskripsi tugas
}

// Implementasi trait Ord untuk Task agar bisa dibandingkan dan disusun dalam BinaryHeap
impl Ord for Task {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // Membandingkan tugas berdasarkan prioritas secara menurun (prioritas lebih besar lebih dulu)
        other.priority.cmp(&self.priority)
    }
}

// Implementasi PartialOrd untuk Task untuk memberikan kemampuan perbandingan parsial
impl PartialOrd for Task {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        // Menggunakan cmp untuk membandingkan tugas secara lengkap
        Some(self.cmp(other))
    }
}

fn main() {
    // Membuat BinaryHeap untuk menampung tugas-tugas yang diurutkan berdasarkan prioritas
    let mut tasks = BinaryHeap::new();

    // Menambahkan beberapa tugas ke dalam BinaryHeap
    tasks.push(Task { priority: 1, description: "Clean room".to_string() });
    tasks.push(Task { priority: 3, description: "Deliver package".to_string() });
    tasks.push(Task { priority: 2, description: "Charge battery".to_string() });

    // Menyelesaikan tugas dengan prioritas tertinggi terlebih dahulu
    while let Some(task) = tasks.pop() {
        // Menampilkan tugas yang sedang dieksekusi beserta prioritasnya
        println!("Executing task: {} with priority {}", task.description, task.priority);
    }
}
