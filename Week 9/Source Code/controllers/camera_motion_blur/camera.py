from controller import Robot, Camera, AnsiCodes
import os

# Jika sistem operasi adalah Windows, import library tambahan untuk pengolahan path
if os.name == 'nt':
    from ctypes import create_unicode_buffer, windll

class Controller(Robot):
    def __init__(self):
        super(Controller, self).__init__()
        self.timeStep = int(self.getBasicTimeStep())
        self.camera = self.getDevice('camera')
        self.camera.enable(self.timeStep)
        self.left_motor = self.getDevice('left wheel motor')
        self.right_motor = self.getDevice('right wheel motor')
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def run(self):
        speed = 4
        pause_counter = 0
        left_speed = 0
        right_speed = 0
        red = 0
        green = 0
        blue = 0
        width = self.camera.getWidth()
        height = self.camera.getHeight()
        color_names = ['merah', 'hijau', 'biru']
        ansi_colors = [AnsiCodes.RED_FOREGROUND, AnsiCodes.GREEN_FOREGROUND, AnsiCodes.BLUE_FOREGROUND]

        while self.step(self.timeStep) != -1:
            image = self.camera.getImage()
            if pause_counter > 0:
                pause_counter -= 1
            
            # Kasus 1: Blob ditemukan baru-baru ini, robot menunggu hingga pause_counter berkurang
            if pause_counter > 640 / self.timeStep:
                left_speed = 0
                right_speed = 0
            # Kasus 2: Blob ditemukan cukup baru, robot mulai berputar tanpa menganalisis gambar untuk sementara waktu
            elif pause_counter > 0:
                left_speed = -speed
                right_speed = speed
            # Kasus 3: Robot berputar dan menganalisis gambar kamera untuk menemukan blob warna baru
            elif not image:
                left_speed = 0
                right_speed = 0
            else:
                # Di sini kita menganalisis gambar dari kamera untuk mendeteksi blob warna
                red = 0
                green = 0
                blue = 0
                for i in range(int(width / 3), int(2 * width / 3)):
                    for j in range(int(height / 2), int(3 * height / 4)):
                        red += Camera.imageGetRed(image, width, i, j)
                        green += Camera.imageGetGreen(image, width, i, j)
                        blue += Camera.imageGetBlue(image, width, i, j)
                
                # Jika satu komponen lebih dominan dari yang lainnya, ditemukan blob
                if red > 3 * green and red > 3 * blue:
                    current_blob = 0  # merah
                elif green > 3 * red and green > 3 * blue:
                    current_blob = 1  # hijau
                elif blue > 3 * red and blue > 3 * green:
                    current_blob = 2  # biru
                else:
                    current_blob = None
                
                # Kasus 3a: Tidak ada blob yang ditemukan, robot terus berputar
                if current_blob is None:
                    left_speed = -speed
                    right_speed = speed
                # Kasus 3b: Blob ditemukan, robot berhenti dan menyimpan gambar
                else:
                    left_speed = 0
                    right_speed = 0
                    print('Sepertinya saya menemukan sebuah ' + ansi_colors[current_blob] +
                          color_names[current_blob] + AnsiCodes.RESET + ' blob.')
                    # Hitung path file di direktori pengguna
                    if os.name == 'nt':
                        user_directory = os.environ['USERPROFILE']
                        # kami membutuhkan path DOS 8.3 untuk mendukung karakter non-ASCII dalam nama pengguna
                        BUFFER_SIZE = 1024
                        buffer = create_unicode_buffer(BUFFER_SIZE)
                        windll.kernel32.GetShortPathNameW(user_directory, buffer, BUFFER_SIZE)
                        user_directory = buffer.value
                    else:
                        user_directory = os.environ['HOME']
                    filename = os.path.join(user_directory, color_names[current_blob] + '_blob.png')
                    self.camera.saveImage(filename, 100)
                    pause_counter = 1280 / self.timeStep
            
            # Setel kecepatan motor.
            self.left_motor.setVelocity(left_speed)
            self.right_motor.setVelocity(right_speed)

# Inisialisasi dan jalankan controller
controller = Controller()
controller.run()
