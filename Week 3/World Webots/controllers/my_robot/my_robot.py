"""
# SIMULASI GERAKAN MAJU DENGAN OPEN-LOOP CONTROL
from controller import Robot

TIME_STEP = 64
MAX_SPEED = 6.28 
robot = Robot()

leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

timestep = int(robot.getBasicTimeStep())

while robot.step(TIME_STEP) != -1:
    leftMotor.setVelocity(5.0)
    rightMotor.setVelocity(5.0)
"""



"""
# SIMULASI GERAKAN MELINGKAR
from controller import Robot

TIME_STEP = 64 
MAX_SPEED = 6.28
robot = Robot()

leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

timestep = int(robot.getBasicTimeStep())

while robot.step(TIME_STEP) != -1:
    leftMotor.setVelocity(0.5*MAX_SPEED)
    rightMotor.setVelocity(MAX_SPEED)
"""



"""
# SIMULASI PENGHENTIAN ROBOT DENGAN SENSOR PROXIMITY
from controller import Robot

TIME_STEP = 64
MAX_SPEED = 6.28 
robot = Robot()

leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))

leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

proximity_sensors = []
for i in range(8):
    print("Sensor Proximity Aktif")
    sensor = robot.getDevice(f'ps{i}')
    sensor.enable(TIME_STEP)
    proximity_sensors.append(sensor)

def stop_robot():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def move_forward(speed):
    leftMotor.setVelocity(speed)
    rightMotor.setVelocity(speed)
    
while robot.step(TIME_STEP) != -1:
    front_left_value = proximity_sensors[0].getValue()
    front_right_value = proximity_sensors[7].getValue()
    print("Nilai sensor proximity depan kiri: ", front_left_value)
    print("Nilai sensor proximity depan kanan: ", front_right_value)
    if front_left_value > 80 or front_right_value > 80:
        print("Objek terdeteksi, robot berhenti")
        stop_robot()  
    else:
        move_forward(5)
 """
