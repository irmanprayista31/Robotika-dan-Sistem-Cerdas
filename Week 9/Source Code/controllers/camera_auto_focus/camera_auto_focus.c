#include <webots/camera.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>
#include <webots/robot.h>

// Mendefinisikan kecepatan motor dan langkah waktu simulasi
#define SPEED 1
#define TIME_STEP 32

int main() {
  // Deklarasi tag perangkat untuk kamera, sensor jarak, dan motor
  WbDeviceTag camera, distance_sensor, left_motor, right_motor;

  // Inisialisasi robot
  wb_robot_init();

  /* Mengambil perangkat kamera dan mengaktifkannya */
  camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, TIME_STEP);

  /* Mengambil perangkat sensor jarak dan mengaktifkannya */
  distance_sensor = wb_robot_get_device("distance sensor");
  wb_distance_sensor_enable(distance_sensor, TIME_STEP);

  /* Mengambil handler untuk motor kiri dan kanan, serta mengatur posisi target ke infinity (mode kontrol kecepatan) */
  left_motor = wb_robot_get_device("left wheel motor");
  right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);

  /* Mengatur kecepatan awal motor:
     - Motor kiri bergerak mundur dengan kecepatan -SPEED
     - Motor kanan bergerak maju dengan kecepatan SPEED */
  wb_motor_set_velocity(left_motor, -SPEED);
  wb_motor_set_velocity(right_motor, SPEED);

  /* Loop utama simulasi */
  while (wb_robot_step(TIME_STEP) != -1) {
    // Membaca nilai jarak dari sensor jarak dan mengonversinya ke meter
    const double object_distance = wb_distance_sensor_get_value(distance_sensor) / 1000;
    
    // Mengatur jarak fokus kamera berdasarkan jarak objek yang terdeteksi
    wb_camera_set_focal_distance(camera, object_distance);
  }

  // Membersihkan sumber daya robot setelah simulasi selesai
  wb_robot_cleanup();

  return 0;
}
