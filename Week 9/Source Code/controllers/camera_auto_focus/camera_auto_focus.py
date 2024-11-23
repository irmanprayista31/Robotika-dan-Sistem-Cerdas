from controller import Robot

# Membuat kelas Controller yang merupakan turunan dari kelas Robot
class Controller(Robot):
    def __init__(self):
        # Memanggil konstruktor kelas Robot
        super(Controller, self).__init__()
        
        # Mendefinisikan timeStep untuk mengatur interval waktu dalam simulasi
        self.timeStep = 32
        
        # Mendapatkan perangkat kamera dari robot dan mengaktifkannya
        self.camera = self.getDevice('camera')
        self.camera.enable(self.timeStep)
        
        # Mendapatkan perangkat sensor jarak dan mengaktifkannya
        self.distance_sensor = self.getDevice('distance sensor')
        self.distance_sensor.enable(self.timeStep)
        
        # Mendapatkan perangkat motor untuk roda kiri dan kanan
        self.left_motor = self.getDevice('left wheel motor')
        self.right_motor = self.getDevice('right wheel motor')
        
        # Mengatur posisi motor menjadi tak terbatas agar motor bisa berputar terus-menerus
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        
        # Mengatur kecepatan awal motor: roda kiri bergerak mundur, roda kanan maju
        self.left_motor.setVelocity(-1)
        self.right_motor.setVelocity(1)

    # Fungsi utama untuk menjalankan logika robot
    def run(self):
        # Loop utama yang dijalankan selama simulasi berjalan
        while self.step(self.timeStep) != -1:
            # Membaca nilai jarak dari sensor jarak dan mengonversinya ke meter
            object_distance = self.distance_sensor.getValue() / 1000
            
            # Mengatur jarak fokus kamera berdasarkan jarak objek yang terdeteksi
            self.camera.setFocalDistance(object_distance)

# Membuat objek dari kelas Controller dan menjalankan fungsi run
controller = Controller()
controller.run()
