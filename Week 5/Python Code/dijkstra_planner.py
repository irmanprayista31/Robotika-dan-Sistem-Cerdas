import heapq  # Mengimpor heapq untuk menggunakan antrean prioritas (min-heap)

def dijkstra(graph, start, goal):
    # Inisialisasi antrean prioritas dengan node awal, biaya 0, dan jalur kosong
    queue = [(0, start, [])]
    # Set untuk menyimpan node yang sudah diproses
    seen = set()
    # Dictionary untuk menyimpan jarak minimum ke setiap node
    min_distance = {start: 0}
    
    while queue:
        # Mengambil node dengan biaya paling rendah
        (cost, v1, path) = heapq.heappop(queue)
        
        # Jika node sudah diproses, lewati
        if v1 in seen:
            continue
        
        # Tambahkan node saat ini ke jalur
        path = path + [v1]
        
        # Jika sudah mencapai tujuan, kembalikan biaya dan jalur
        if v1 == goal:
            return cost, path
        
        # Tandai node ini sebagai sudah diproses
        seen.add(v1)
        
        # Periksa tetangga dari node saat ini
        for v2, distance in graph[v1].items():
            # Jika tetangga sudah diproses, lewati
            if v2 in seen:
                continue
            
            # Hitung biaya baru untuk mencapai tetangga
            prev = min_distance.get(v2, None)
            next_cost = cost + distance
            
            # Jika jalur ini lebih baik, perbarui jarak minimum dan tambahkan ke antrean
            if prev is None or next_cost < prev:
                min_distance[v2] = next_cost
                heapq.heappush(queue, (next_cost, v2, path))
    
    # Jika tidak ada jalur yang ditemukan, kembalikan infinity dan jalur kosong
    return float("inf"), []

# Contoh graf yang merepresentasikan ruang bebas dengan jarak antar node
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Menjalankan algoritma untuk menemukan jalur terpendek dari 'A' ke 'D'
cost, path = dijkstra(graph, 'A', 'D')
print("Biaya:", cost)
print("Jalur:", path)

