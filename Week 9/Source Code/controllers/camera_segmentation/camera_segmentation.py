from controller import Robot, Display

class Controller(Robot):
    def __init__(self):
        super(Controller, self).__init__()
        self.timeStep = 64

        # Mengambil perangkat kamera dan mengaktifkan fitur kamera, pengenalan, serta segmentasi
        self.camera = self.getDevice('camera')
        self.camera.enable(self.timeStep)  # Mengaktifkan kamera dengan timestep tertentu
        self.camera.recognitionEnable(self.timeStep)  # Mengaktifkan fitur pengenalan objek
        self.camera.enableRecognitionSegmentation()  # Mengaktifkan segmentasi pengenalan objek

        # Mengambil perangkat display untuk menampilkan gambar hasil segmentasi
        self.display = self.getDevice('segmented image display')

        # Mengambil perangkat motor dan mengatur kecepatan awal
        self.left_motor = self.getDevice('left wheel motor')
        self.right_motor = self.getDevice('right wheel motor')
        self.left_motor.setPosition(float('inf'))  # Mengatur kontrol kecepatan
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(-1.5)  # Motor kiri bergerak mundur
        self.right_motor.setVelocity(1.5)  # Motor kanan bergerak maju

    def run(self):
        # Mendapatkan dimensi kamera
        width = self.camera.getWidth()
        height = self.camera.getHeight()

        # Loop utama untuk menjalankan simulasi
        while self.step(self.timeStep) != -1:
            # Memastikan segmentasi pengenalan telah diaktifkan
            if self.camera.isRecognitionSegmentationEnabled() and self.camera.getRecognitionSamplingPeriod() > 0:
                # Mengambil data gambar segmentasi
                data = self.camera.getRecognitionSegmentationImage()
                if data:
                    # Membuat dan menampilkan gambar segmentasi di perangkat Display
                    segmented_image = self.display.imageNew(data, Display.BGRA, width, height)
                    self.display.imagePaste(segmented_image, 0, 0, False)  # Menempelkan gambar pada Display
                    self.display.imageDelete(segmented_image)  # Menghapus gambar dari memori setelah ditampilkan


# Inisialisasi dan menjalankan Controller
controller = Controller()
controller.run()
