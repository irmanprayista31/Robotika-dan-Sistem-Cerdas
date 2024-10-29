def get_neighbors(node, grid):
    neighbors = []
    # Arah: atas, bawah, kiri, kanan
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for d in directions:
        neighbor = (node[0] + d[0], node[1] + d[1])
        # Pastikan tetangga berada dalam batas grid dan bukan halangan (nilai 0)
        if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
            neighbors.append(neighbor)
    return neighbors

def a_star(start, goal, grid):
    # Daftar node yang perlu diperiksa
    open_list = {start}
    # Set node yang sudah diperiksa
    closed_list = set()
    # Menyimpan jarak dari start ke node saat ini
    g = {start: 0}
    # Menyimpan nilai f (biaya + heuristik)
    f = {start: heuristic(start, goal)}
    # Melacak jalur
    came_from = {}
    
    while open_list:
        # Ambil node dengan nilai f terendah
        current = min(open_list, key=lambda x: f[x])
        
        # Jika mencapai tujuan, bangun jalur
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Kembalikan jalur terbalik
        
        # Pindahkan node saat ini dari open_list ke closed_list
        open_list.remove(current)
        closed_list.add(current)
        
        # Periksa setiap tetangga dari node saat ini
        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_list:
                continue
            
            # Hitung biaya g baru
            tentative_g = g[current] + 1
            
            # Jika tetangga belum ada di open_list atau biaya g lebih rendah
            if neighbor not in open_list:
                open_list.add(neighbor)
            elif tentative_g >= g.get(neighbor, float('inf')):
                continue
            
            # Simpan informasi terbaik untuk mencapai tetangga
            came_from[neighbor] = current
            g[neighbor] = tentative_g
            f[neighbor] = g[neighbor] + heuristic(neighbor, goal)
    
    return None  # Kembalikan None jika tidak ada jalur ditemukan

def heuristic(a, b):
    # Menggunakan heuristik Manhattan (jarak x + jarak y)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Contoh grid (0 adalah jalan bebas, 1 adalah halangan)
grid = [
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 0]
]

# Mulai dan tujuan
start = (0, 0)
goal = (3, 3)

# Jalankan algoritma A*
path = a_star(start, goal, grid)
print("Jalur:", path)
