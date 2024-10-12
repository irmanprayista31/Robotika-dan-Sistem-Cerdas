from controller import Robot

TIME_STEP = 64 # waktu untuk menjalankan satu langkah simulasi
MAX_SPEED = 6.28 # set kecepatan maksimal robot
robot = Robot()

# motor roda kiri dan kanan
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

# mengatur posisi motor agar berjalan tanpa batas (mode kecepatan)
leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

# mengatur kecepatan awal = 0.0
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Mendefinisikan sensor proximity
# Karena robot memiliki 8 sensor proximity yang dinamakan ps[0] - ps[7]
# loop 8 kali (sebanyak jumlah sensor proximity)
# lalu disimpan di list proximity_sensor
proximity_sensors = []
for i in range(8):
    print("Sensor Proximity Aktif")
    sensor = robot.getDevice(f'ps{i}')
    sensor.enable(TIME_STEP)
    proximity_sensors.append(sensor)

# Fungsi untuk menghentikan robot
def stop_robot():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def move_forward(speed):
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)
    
# Loop untuk menggerakkan robot
while robot.step(TIME_STEP) != -1:
   
    # Robot dengan Sensor Proximity
    # [0] sensor kiri depan dan [7] sensor kanan depan
    front_left_value = proximity_sensors[0].getValue()
    front_right_value = proximity_sensors[7].getValue()
    print("Nilai sensor proximity depan kiri: ", front_left_value)
    print("Nilai sensor proximity depan kanan: ", front_right_value)

    # Jika ada objek di depan maka berhenti, selain itu jalan terus 
    if front_left_value > 80 or front_right_value > 80:
        print("Objek terdeteksi, robot berhenti")
        stop_robot()  
    else:
        move_forward(5) 
