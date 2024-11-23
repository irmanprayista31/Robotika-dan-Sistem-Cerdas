from controller import Robot

class Controller(Robot):
    def __init__(self):
        # Memanggil konstruktor kelas induk Robot
        super(Controller, self).__init__()
        
        # Mendefinisikan langkah waktu untuk simulasi
        self.timeStep = 64
        
        # Mengambil perangkat kamera dan mengaktifkannya
        self.camera = self.getDevice('camera')
        self.camera.enable(self.timeStep)
        
        # Mengaktifkan fitur pengenalan objek pada kamera
        self.camera.recognitionEnable(self.timeStep)
        
        # Mengambil perangkat motor kiri dan kanan
        self.left_motor = self.getDevice('left wheel motor')
        self.right_motor = self.getDevice('right wheel motor')
        
        # Mengatur posisi motor ke infinity untuk kontrol kecepatan
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        
        # Mengatur kecepatan awal motor
        # Motor kiri bergerak mundur (-1.5), motor kanan bergerak maju (1.5)
        self.left_motor.setVelocity(-1.5)
        self.right_motor.setVelocity(1.5)

    def run(self):
        # Loop utama untuk menjalankan simulasi
        while self.step(self.timeStep) != -1:
            # Mendapatkan jumlah objek yang dikenali oleh kamera
            number_of_objects = self.camera.getRecognitionNumberOfObjects()
            print(f'Recognized {number_of_objects} objects.')
            print(' ')
            
            # Mengambil informasi semua objek yang dikenali
            objects = self.camera.getRecognitionObjects()
            counter = 1  # Inisialisasi penghitung objek
            
            for object in objects:
                # Mendapatkan atribut objek: posisi, orientasi, ukuran, dll.
                position = object.getPosition()  # Posisi relatif objek
                orientation = object.getOrientation()  # Orientasi relatif objek
                size = object.getSize()  # Ukuran objek
                position_on_image = object.getPositionOnImage()  # Posisi pada gambar kamera
                size_on_image = object.getSizeOnImage()  # Ukuran pada gambar kamera
                number_of_colors = object.getNumberOfColors()  # Jumlah warna yang dikenali
                colors = object.getColors()  # Warna objek
                
                # Menampilkan informasi lengkap tentang objek
                print(f' Object {counter}/{number_of_objects}: {object.getModel()} (id = {object.getId()})')
                print(f' Position: {position[0]} {position[1]} {position[2]}')
                print(f' Orientation: {orientation[0]} {orientation[1]} {orientation[2]} {orientation[3]}')
                print(f' Size: {size[0]} x {size[1]}')
                print(f' Position on camera image: {position_on_image[0]} {position_on_image[1]}')
                print(f' Size on camera image: {size_on_image[0]} x {size_on_image[1]}')
                
                # Menampilkan semua warna yang dikenali pada objek
                for j in range(number_of_colors):
                    print(f'  Color {j + 1}/{number_of_colors}: '
                          f'{colors[3 * j]} {colors[3 * j + 1]} {colors[3 * j + 2]}')
                print(' ')
                
                # Meningkatkan penghitung objek
                counter += 1

# Membuat instance dari kelas Controller dan menjalankan simulasi
controller = Controller()
controller.run()
