#include <webots/camera.h>
#include <webots/distance_sensor.h>
#include <webots/motor.h>
#include <webots/robot.h>
#include <webots/utils/ansi_codes.h>

#include <math.h>
#include <stdio.h>

#define TIME_STEP 64       // Interval waktu simulasi
#define THRESHOLD 200      // Ambang batas untuk mendeteksi warna

#define RED 0              // Indeks untuk warna merah
#define GREEN 1            // Indeks untuk warna hijau
#define BLUE 2             // Indeks untuk warna biru

#define LEFT 0             // Indeks untuk sensor kiri
#define RIGHT 1            // Indeks untuk sensor kanan

#define X 0                // Indeks koordinat X
#define Y 1                // Indeks koordinat Y

// Fungsi untuk menghitung sudut berdasarkan koordinat 2D
double coord2D_to_angle(double x, double y) {
  if (x > 0.0 && y >= 0.0)
    return atan(y / x);
  else if (x > 0.0 && y < 0.0)
    return atan(y / x) + 2.0 * M_PI;
  else if (x < 0.0)
    return atan(y / x) + M_PI;
  else if (x == 0.0 && y > 0.0)
    return M_PI_2;
  else if (x == 0.0 && y < 0.0)
    return 3.0 * M_PI_2;
  else
    return 0.0; // Kondisi ketika x dan y adalah nol
}

int main(int argc, char **argv) {
  int i, k; // Variabel iterator untuk loop

  // Inisialisasi Webots
  wb_robot_init();

  // Inisialisasi kamera
  WbDeviceTag camera = wb_robot_get_device("camera");
  wb_camera_enable(camera, 2 * TIME_STEP);
  int width = wb_camera_get_width(camera);
  int height = wb_camera_get_height(camera);
  int color_index[3][2] = {{0, 0}, {0, 0}, {0, 0}};
  int x, y, r, g, b;

  // Inisialisasi sensor jarak
  WbDeviceTag us[2];
  double us_values[2];
  double coefficients[2][2] = {{6.0, -3.0}, {-5.0, 4.0}};
  us[LEFT] = wb_robot_get_device("us0");
  us[RIGHT] = wb_robot_get_device("us1");
  for (i = 0; i < 2; i++)
    wb_distance_sensor_enable(us[i], TIME_STEP);

  // Inisialisasi motor dan mengatur mode kontrol kecepatan
  WbDeviceTag left_motor = wb_robot_get_device("left wheel motor");
  WbDeviceTag right_motor = wb_robot_get_device("right wheel motor");
  wb_motor_set_position(left_motor, INFINITY);
  wb_motor_set_position(right_motor, INFINITY);
  wb_motor_set_velocity(left_motor, 0.0);
  wb_motor_set_velocity(right_motor, 0.0);

  double speed[2]; // Variabel untuk kecepatan motor

  while (wb_robot_step(TIME_STEP) != -1) {
    // Membaca sensor kamera
    const unsigned char *image = wb_camera_get_image(camera);
    for (i = 0; i < 2; i++)
      us_values[i] = wb_distance_sensor_get_value(us[i]);

    // Menghitung kecepatan berdasarkan sensor jarak
    for (i = 0; i < 2; i++) {
      speed[i] = 0.0;
      for (k = 0; k < 2; k++)
        speed[i] += us_values[k] * coefficients[i][k];
    }

    // Mendeteksi blob warna dan menentukan koordinat
    for (y = 0; y < height; y++) {
      for (x = 0; x < width; x++) {
        r = wb_camera_image_get_red(image, width, x, y);
        g = wb_camera_image_get_green(image, width, x, y);
        b = wb_camera_image_get_blue(image, width, x, y);
        if (r > THRESHOLD && g < THRESHOLD && b < THRESHOLD) {
          color_index[RED][X] = x;
          color_index[RED][Y] = y;
        } else if (r < THRESHOLD && g > THRESHOLD && b < THRESHOLD) {
          color_index[GREEN][X] = x;
          color_index[GREEN][Y] = y;
        } else if (r < THRESHOLD && g < THRESHOLD && b > THRESHOLD) {
          color_index[BLUE][X] = x;
          color_index[BLUE][Y] = y;
        }
      }
    }

    // Menampilkan hasil pada konsol
    ANSI_CLEAR_CONSOLE();
    for (i = 0; i < 3; i++) {
      printf("Last %s blob seen at (%d,%d) with an angle of %f\n",
             (i == GREEN) ? "Green" :
             (i == RED)   ? "Red" :
                            "Blue",
             color_index[i][X], color_index[i][Y],
             coord2D_to_angle((double)(color_index[i][X] + width / 2), (double)(color_index[i][Y] + height / 2)));
    }

    // Mengatur kecepatan motor
    wb_motor_set_velocity(left_motor, 3.0 + speed[LEFT]);
    wb_motor_set_velocity(right_motor, 3.0 + speed[RIGHT]);
  }

  wb_robot_cleanup();
  return 0;
}
