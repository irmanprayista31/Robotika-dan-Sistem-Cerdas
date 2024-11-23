#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <webots/camera.h>
#include <webots/motor.h>
#include <webots/robot.h>
#include <webots/utils/system.h>

// Definisi warna ANSI untuk output teks di terminal
#define ANSI_COLOR_RED "\x1b[31m"
#define ANSI_COLOR_GREEN "\x1b[32m"
#define ANSI_COLOR_YELLOW "\x1b[33m"
#define ANSI_COLOR_BLUE "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN "\x1b[36m"
#define ANSI_COLOR_RESET "\x1b[0m"

// Kecepatan robot saat bergerak
#define SPEED 4

// Enum untuk jenis blob warna yang terdeteksi
enum BLOB_TYPE { RED, GREEN, BLUE, NONE };

int main() {
  WbDeviceTag camera, left_motor, right_motor;  // Deklarasi tag perangkat untuk kamera dan motor
  int width, height;  // Variabel untuk lebar dan tinggi gambar kamera
  int pause_counter = 0;  // Variabel untuk menghitung waktu tunggu
  int left_speed, right_speed;  // Kecepatan motor kiri dan kanan
  int i, j;  // Variabel untuk iterasi piksel gambar
  int red, blue, green;  // Variabel untuk menghitung intensitas warna RGB
  const char *color_names[3] = {"red", "green", "blue"};  // Nama warna untuk output
  const char *ansi_colors[3] = {ANSI_COLOR_RED, ANSI_COLOR_GREEN, ANSI_COLOR_BLUE};  // Warna ANSI untuk output
  const char *filenames[3] = {"red_blob.png", "green_blob.png", "blue_blob.png"};  // Nama file untuk menyimpan gambar blob
  enum BLOB_TYPE current_blob;  // Menyimpan jenis blob yang terdeteksi

  wb_robot_init();  // Inisialisasi robot

  const int time_step = wb_robot_get_basic_time_step();  // Mendapatkan langkah waktu dasar robot

  // Mendapatkan perangkat kamera, mengaktifkannya, dan menyimpan lebar dan tinggi gambar
  camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, time_step);
  width = wb_camera_get_width(camera);
  height = wb_camera_get_height(camera);

  // Mendapatkan perangkat motor dan mengatur posisi target ke tak terbatas (menggunakan kontrol kecepatan)
  left_motor = wb_robot_get_device("left wheel motor");
  right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);  // Memulai motor kiri dengan kecepatan 0
  wb_motor_set_velocity(right_motor, 0.0);  // Memulai motor kanan dengan kecepatan 0

  // Loop utama robot
  while (wb_robot_step(time_step) != -1) {
    // Mendapatkan nilai gambar terbaru dari kamera
    const unsigned char *image = wb_camera_get_image(camera);

    // Mengurangi nilai pause_counter jika lebih besar dari 0
    if (pause_counter > 0)
      pause_counter--;

    /*
     * Kasus 1: 
     * Blob ditemukan baru-baru ini
     * Robot berhenti di depan blob sampai pause_counter cukup kecil
     */
    if (pause_counter > 640 / time_step) {
      left_speed = 0;
      right_speed = 0;
    }
    /*
     * Kasus 2: 
     * Blob ditemukan baru-baru ini
     * Robot mulai berputar tapi tidak menganalisis gambar untuk sementara waktu
     */
    else if (pause_counter > 0) {
      left_speed = -SPEED;
      right_speed = SPEED;
    }
    /*
     * Kasus 3: 
     * Robot berputar dan menganalisis gambar kamera untuk menemukan blob baru
     */
    else if (!image) {  // Gambar mungkin NULL jika sinkronisasi Robot.synchronization = FALSE
      left_speed = 0;
      right_speed = 0;
    } else {  // pause_counter == 0
      // Reset jumlah warna
      red = 0;
      green = 0;
      blue = 0;

      // Menganalisis gambar dari kamera untuk mendeteksi blob dengan warna tertentu
      // Dengan cara memindai piksel di tengah gambar dan menjumlahkan komponen warna secara terpisah
      for (i = width / 3; i < 2 * width / 3; i++) {
        for (j = height / 2; j < 3 * height / 4; j++) {
          red += wb_camera_image_get_red(image, width, i, j);
          blue += wb_camera_image_get_blue(image, width, i, j);
          green += wb_camera_image_get_green(image, width, i, j);
        }
      }

      /*
       * Jika salah satu komponen warna lebih dominan daripada yang lainnya,
       * dianggap ada blob dengan warna tersebut
       */
      if ((red > 3 * green) && (red > 3 * blue))
        current_blob = RED;
      else if ((green > 3 * red) && (green > 3 * blue))
        current_blob = GREEN;
      else if ((blue > 3 * red) && (blue > 3 * green))
        current_blob = BLUE;
      else
        current_blob = NONE;

      /*
       * Kasus 3a: 
       * Tidak ada blob yang terdeteksi, robot terus berputar
       */
      if (current_blob == NONE) {
        left_speed = -SPEED;
        right_speed = SPEED;
      }
      /*
       * Kasus 3b: 
       * Blob terdeteksi, robot berhenti, menyimpan gambar, dan mengubah status
       */
      else {
        left_speed = 0;
        right_speed = 0;
        printf("Looks like I found a %s%s%s blob.\n", ansi_colors[current_blob], color_names[current_blob], ANSI_COLOR_RESET);
        // Menghitung path file di direktori pengguna
        char *filepath;
#ifdef _WIN32
        const char *user_directory = wbu_system_short_path(wbu_system_getenv("USERPROFILE"));
        filepath = (char *)malloc(strlen(user_directory) + 16);
        strcpy(filepath, user_directory);
        strcat(filepath, "\\");
#else
        const char *user_directory = wbu_system_getenv("HOME");
        filepath = (char *)malloc(strlen(user_directory) + 16);
        strcpy(filepath, user_directory);
        strcat(filepath, "/");
#endif
        strcat(filepath, filenames[current_blob]);
        // Menyimpan gambar blob yang terdeteksi
        wb_camera_save_image(camera, filepath, 100);
        free(filepath);
        pause_counter = 1280 / time_step;  // Menetapkan waktu tunggu untuk mencegah deteksi blob yang sama
      }
    }

    // Mengatur kecepatan motor berdasarkan status saat ini
    wb_motor_set_velocity(left_motor, left_speed);
    wb_motor_set_velocity(right_motor, right_speed);
  }

  wb_robot_cleanup();  // Membersihkan setelah robot selesai beroperasi

  return 0;
}
