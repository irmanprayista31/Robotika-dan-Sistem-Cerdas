// Mengimpor VecDeque dari koleksi standar untuk implementasi antrian (queue)
use std::collections::VecDeque;

// Fungsi untuk merencanakan jalur dari start ke goal pada grid
fn plan_path(grid: &Vec<Vec<i32>>, start: (usize, usize), goal: (usize, usize)) -> Option<Vec<(usize, usize)>> {
    // Definisi arah pergerakan: kanan, bawah, kiri, atas
    let directions = [(0, 1), (1, 0), (0, -1), (-1, 0)];
    
    // Matriks untuk mencatat apakah titik sudah dikunjungi
    let mut visited = vec![vec![false; grid[0].len()]; grid.len()];
    
    // Antrian (queue) untuk BFS
    let mut queue = VecDeque::new();
    
    // Matriks untuk melacak jalur
    let mut path = vec![vec![None; grid[0].len()]; grid.len()];

    // Memulai dengan titik start dan menandainya sebagai sudah dikunjungi
    queue.push_back(start);
    visited[start.0][start.1] = true;

    // Proses BFS
    while let Some((x, y)) = queue.pop_front() {
        // Jika titik saat ini adalah tujuan (goal), kembalikan jalur yang ditemukan
        if (x, y) == goal {
            let mut current = goal;
            let mut result = vec![current];
            
            // Menelusuri jalur mundur dari goal ke start
            while let Some(prev) = path[current.0][current.1] {
                current = prev;
                result.push(current);
            }
            
            // Membalikkan jalur untuk mendapatkan urutan dari start ke goal
            result.reverse();
            return Some(result);
        }

        // Mengeksplorasi arah-arah yang memungkinkan
        for &(dx, dy) in &directions {
            // Menentukan koordinat baru setelah bergerak
            let nx = x as isize + dx;
            let ny = y as isize + dy;

            // Mengecek apakah koordinat baru valid (dalam batas grid)
            if nx >= 0 && ny >= 0 && (nx as usize) < grid.len() && (ny as usize) < grid[0].len() {
                let (nx, ny) = (nx as usize, ny as usize);
                
                // Mengecek apakah titik tersebut belum dikunjungi dan bukan rintangan (nilai 0 artinya bisa dilalui)
                if !visited[nx][ny] && grid[nx][ny] == 0 {
                    visited[nx][ny] = true;   // Tandai titik tersebut sebagai sudah dikunjungi
                    queue.push_back((nx, ny)); // Masukkan titik baru ke antrian
                    path[nx][ny] = Some((x, y)); // Catat titik sebelumnya sebagai titik asal untuk jalur
                }
            }
        }
    }

    // Jika tidak ditemukan jalur, kembalikan None
    None
}

fn main() {
    // Definisikan grid, 0 untuk jalur yang bisa dilalui dan 1 untuk rintangan
    let grid = vec![
        vec![0, 0, 1, 0, 0],
        vec![1, 0, 1, 0, 1],
        vec![0, 0, 0, 0, 0],
        vec![1, 1, 1, 1, 0],
        vec![0, 0, 0, 0, 0],
    ];

    // Titik start dan goal
    let start = (0, 0);
    let goal = (4, 4);

    // Memanggil fungsi plan_path dan mencetak hasilnya
    match plan_path(&grid, start, goal) {
        Some(path) => println!("Path: {:?}", path), // Jika jalur ditemukan, cetak jalurnya
        None => println!("No path found."), // Jika tidak ditemukan jalur
    }
}
