use std::collections::VecDeque;

// Fungsi untuk mencari jalur menggunakan algoritma BFS
fn plan_path(grid: &Vec<Vec<i32>>, start: (usize, usize), goal: (usize, usize)) -> Option<Vec<(usize, usize)>> {
    // Arah gerakan yang diizinkan (atas, bawah, kiri, kanan)
    let directions = vec![
        (-1, 0), // atas
        (1, 0),  // bawah
        (0, -1), // kiri
        (0, 1),  // kanan
    ];

    let mut queue = VecDeque::new();
    let mut visited = vec![vec![false; grid[0].len()]; grid.len()];
    let mut parent = vec![vec![None; grid[0].len()]; grid.len()];

    // Menambahkan titik mulai ke antrian
    queue.push_back(start);
    visited[start.0][start.1] = true;

    while let Some(current) = queue.pop_front() {
        // Jika kita mencapai titik tujuan, kembalikan jalur yang ditemukan
        if current == goal {
            let mut path = Vec::new();
            let mut step = current;
            while let Some(prev) = parent[step.0][step.1] {
                path.push(step);
                step = prev;
            }
            path.push(start);
            path.reverse();
            return Some(path);
        }

        // Mengeksplorasi arah yang memungkinkan
        for (dx, dy) in &directions {
            let new_x = current.0 as isize + dx;
            let new_y = current.1 as isize + dy;

            // Pastikan posisi baru valid dan belum dikunjungi
            if new_x >= 0
                && new_x < grid.len() as isize
                && new_y >= 0
                && new_y < grid[0].len() as isize
                && grid[new_x as usize][new_y as usize] == 0
                && !visited[new_x as usize][new_y as usize]
            {
                let new_pos = (new_x as usize, new_y as usize);
                visited[new_x as usize][new_y as usize] = true;
                parent[new_x as usize][new_y as usize] = Some(current);
                queue.push_back(new_pos);
            }
        }
    }

    // Jika tidak ada jalur yang ditemukan
    None
}

fn main() {
    // Definisi grid yang mewakili area pencarian jalur
    // 0 berarti jalur yang bisa dilalui, 1 berarti rintangan
    let grid = vec![
        vec![0, 0, 1, 0, 0],
        vec![1, 0, 1, 0, 1],
        vec![0, 0, 0, 0, 0],
        vec![1, 1, 1, 1, 0],
        vec![0, 0, 0, 0, 0],
    ];

    // Titik awal dan tujuan
    let start = (0, 0); // Titik mulai berada di posisi (0, 0)
    let goal = (4, 4);  // Titik tujuan berada di posisi (4, 4)

    // Memanggil fungsi `plan_path` untuk mencari jalur dari start ke goal
    match plan_path(&grid, start, goal) {
        Some(path) => {
            // Jika jalur ditemukan, iterasi dan tampilkan setiap langkah pada jalur
            for step in &path {
                println!("Step: {:?}", step); // Menampilkan setiap langkah pada jalur yang ditemukan
            }
        }
        None => println!("No path found."), // Jika tidak ditemukan jalur, beri tahu pengguna
    }
}
