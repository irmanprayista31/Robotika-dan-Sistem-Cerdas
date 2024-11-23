#include <webots/camera.h>
#include <webots/display.h>
#include <webots/motor.h>
#include <webots/robot.h>

#define SPEED 1.5
#define TIME_STEP 64

int main() {
  WbDeviceTag camera, display, left_motor, right_motor;
  WbImageRef segmented_image; // Referensi untuk menyimpan gambar segmentasi

  wb_robot_init();

  /* Mengambil perangkat kamera, mengaktifkan kamera, pengenalan, dan segmentasi */
  camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, TIME_STEP); // Mengaktifkan kamera dengan langkah waktu tertentu
  wb_camera_recognition_enable(camera, TIME_STEP); // Mengaktifkan fitur pengenalan objek
  wb_camera_recognition_enable_segmentation(camera); // Mengaktifkan segmentasi gambar
  const int width = wb_camera_get_width(camera); // Lebar gambar kamera
  const int height = wb_camera_get_height(camera); // Tinggi gambar kamera

  /* Mengambil perangkat display untuk menampilkan gambar segmentasi */
  display = wb_robot_get_device("segmented image display");

  /* Mendapatkan perangkat motor dan mengatur posisi target ke infinity untuk kontrol kecepatan */
  left_motor = wb_robot_get_device("left wheel motor");
  right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY); // Menjadikan kontrol kecepatan
  wb_motor_set_position(right_motor, INFINITY);

  /* Mengatur kecepatan awal motor */
  wb_motor_set_velocity(left_motor, -SPEED); // Motor kiri bergerak mundur
  wb_motor_set_velocity(right_motor, SPEED); // Motor kanan bergerak maju

  /* Loop utama */
  while (wb_robot_step(TIME_STEP) != -1) {
    // Memastikan segmentasi dan pengenalan kamera telah diaktifkan
    if (wb_camera_recognition_is_segmentation_enabled(camera) && 
        wb_camera_recognition_get_sampling_period(camera) > 0) {
      
      /* Mendapatkan gambar segmentasi dan menampilkannya di perangkat Display */
      const unsigned char *data = wb_camera_recognition_get_segmentation_image(camera); // Mengambil data gambar segmentasi
      if (data) {
        // Membuat gambar baru untuk ditampilkan
        segmented_image = wb_display_image_new(display, width, height, data, WB_IMAGE_BGRA);
        
        // Menempelkan gambar pada display
        wb_display_image_paste(display, segmented_image, 0, 0, false);
        
        // Menghapus gambar dari memori setelah ditampilkan
        wb_display_image_delete(display, segmented_image);
      }
    }
  }

  wb_robot_cleanup(); // Membersihkan sumber daya sebelum keluar dari simulasi

  return 0;
}
