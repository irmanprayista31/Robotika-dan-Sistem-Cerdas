#include <stdio.h>
#include <webots/camera.h>
#include <webots/camera_recognition_object.h>
#include <webots/motor.h>
#include <webots/robot.h>

// Mendefinisikan kecepatan motor dan langkah waktu simulasi
#define SPEED 1.5
#define TIME_STEP 64

int main() {
  // Deklarasi tag perangkat untuk kamera, motor kiri, dan motor kanan
  WbDeviceTag camera, left_motor, right_motor;
  int i, j; // Variabel untuk iterasi

  // Inisialisasi robot
  wb_robot_init();

  /* Mengambil perangkat kamera, mengaktifkan kamera, dan mengaktifkan fitur pengenalan objek */
  camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, TIME_STEP);
  wb_camera_recognition_enable(camera, TIME_STEP);

  /* Mengambil handler untuk motor kiri dan kanan, 
     serta mengatur posisi target motor ke infinity (kontrol kecepatan) */
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
    /* Mendapatkan jumlah objek yang dikenali oleh kamera */
    int number_of_objects = wb_camera_recognition_get_number_of_objects(camera);
    printf("\nRecognized %d objects.\n", number_of_objects);

    /* Mengambil informasi objek yang dikenali dan menampilkannya */
    const WbCameraRecognitionObject *objects = wb_camera_recognition_get_objects(camera);
    for (i = 0; i < number_of_objects; ++i) {
      // Menampilkan model objek
      printf("Model of object %d: %s\n", i, objects[i].model);
      
      // Menampilkan ID objek
      printf("Id of object %d: %d\n", i, objects[i].id);
      
      // Menampilkan posisi relatif objek
      printf("Relative position of object %d: %lf %lf %lf\n", i, objects[i].position[0], objects[i].position[1],
             objects[i].position[2]);
      
      // Menampilkan orientasi relatif objek
      printf("Relative orientation of object %d: %lf %lf %lf %lf\n", i, objects[i].orientation[0], objects[i].orientation[1],
             objects[i].orientation[2], objects[i].orientation[3]);
      
      // Menampilkan ukuran objek
      printf("Size of object %d: %lf %lf\n", i, objects[i].size[0], objects[i].size[1]);
      
      // Menampilkan posisi objek pada gambar kamera
      printf("Position of the object %d on the camera image: %d %d\n", i, objects[i].position_on_image[0],
             objects[i].position_on_image[1]);
      
      // Menampilkan ukuran objek pada gambar kamera
      printf("Size of the object %d on the camera image: %d %d\n", i, objects[i].size_on_image[0], objects[i].size_on_image[1]);
      
      // Menampilkan warna-warna yang dikenali pada objek
      for (j = 0; j < objects[i].number_of_colors; ++j)
        printf("- Color %d/%d: %lf %lf %lf\n", j + 1, objects[i].number_of_colors, objects[i].colors[3 * j],
               objects[i].colors[3 * j + 1], objects[i].colors[3 * j + 2]);
    }
  }

  // Membersihkan alokasi sumber daya robot setelah simulasi selesai
  wb_robot_cleanup();

  return 0;
}
