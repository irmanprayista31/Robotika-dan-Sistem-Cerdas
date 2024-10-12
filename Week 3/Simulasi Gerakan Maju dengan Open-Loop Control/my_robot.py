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

# Loop untuk menggerakkan robot
while robot.step(TIME_STEP) != -1:
    # Menggerakkan robot maju dengan mengatur kecepatan pada kedua roda
    leftMotor.setVelocity(5.0)
    rightMotor.setVelocity(5.0)
