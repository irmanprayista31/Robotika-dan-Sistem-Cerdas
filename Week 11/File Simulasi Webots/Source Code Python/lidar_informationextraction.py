from controller import Robot

# Konstanta waktu langkah
TIME_STEP = 32

# Indeks untuk sensor kiri dan kanan
LEFT = 0
RIGHT = 1

# Inisialisasi robot
robot = Robot()

# Inisialisasi perangkat LIDAR
lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)
lidar.enablePointCloud()

# Inisialisasi sensor ultrasonik
us = [robot.getDevice("us0"), robot.getDevice("us1")]
for sensor in us:
    sensor.enable(TIME_STEP)

# Inisialisasi motor
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))  # Mode kecepatan
right_motor.setPosition(float('inf'))  # Mode kecepatan
left_motor.setVelocity(0.0)  # Set awal kecepatan motor
right_motor.setVelocity(0.0)

# Koefisien penghitungan kecepatan
coefficients = [[12.0, -6.0], [-10.0, 8.0]]
base_speed = 6.0

# Fungsi untuk mengambil data dari LIDAR
def extract_lidar_data():
    lidar_data = lidar.getRangeImage()
    print(f"Lidar Data: {lidar_data[10]}...")
    return lidar_data

# Fungsi untuk membaca nilai sensor jarak
def read_distance_sensor():
    distances = [sensor.getValue() for sensor in us]
    print(f"Distance Sensor Reading: Left={distances[LEFT]:.2f}, Right={distances[RIGHT]:.2f}")
    return distances

# Fungsi untuk menghitung kecepatan motor berdasarkan sensor jarak
def compute_speed(us_values):
    speed = [0.0, 0.0]
    for i in range(2):  # Iterasi untuk motor kiri dan kanan
        for k in range(2):  # Iterasi untuk setiap sensor jarak
            speed[i] += us_values[k] * coefficients[i][k]
    return speed

# Loop utama untuk kontrol robot
while robot.step(TIME_STEP) != -1:
    # Ambil data dari LIDAR
    lidar_data = extract_lidar_data()
    
    # Ambil data dari sensor jarak
    us_values = read_distance_sensor()
    
    # Hitung kecepatan motor berdasarkan data sensor
    speeds = compute_speed(us_values)
    
    # Atur kecepatan motor
    left_motor.setVelocity(base_speed + speeds[LEFT])
    right_motor.setVelocity(base_speed + speeds[RIGHT])

# membersihkan memori
robot.cleanup()