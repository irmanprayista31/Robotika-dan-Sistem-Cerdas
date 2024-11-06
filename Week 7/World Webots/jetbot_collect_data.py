# Copyright 1996-2021 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os  # Mengimpor modul os untuk operasi file dan direktori
import os.path  # Mengimpor modul os.path untuk operasi terkait path

from controller import Supervisor  # Mengimpor Supervisor dari modul controller (Webots) untuk mengontrol simulasi
import jetbot_train  # Mengimpor modul jetbot_train untuk melakukan pelatihan model AI

# Membuat instance dari Supervisor untuk robot
robot = Supervisor()

# Menampilkan instruksi penggunaan program kepada pengguna
print('Collect data to build the training dataset for AI collision avoidance classifier\n'
      'Manually move the robot to the desired position and press:\n'
      '- "F": if the robot can safely move forward\n'
      '- "B": if the robot should turn\n'
      'Datasets images will be automatically stored in two different folders named "free" and "blocked".\n'
      'At least 20 images per category are needed.\n'
      'When dataset is ready, press "C" to compute the model.\n'
      'Copy the resulting "best_model.pth" file in the "jetbot_collision_avoidance" controller directory to use the model.')

# Mendapatkan nilai timestep dari simulasi saat ini
timestep = int(robot.getBasicTimeStep())

# Mengaktifkan perangkat kamera pada robot dengan timestep yang sudah diatur
camera = robot.getDevice('camera')
camera.enable(timestep)

# Mengaktifkan perangkat keyboard untuk menerima input dari pengguna
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

# Inisialisasi variabel index untuk penomoran gambar yang akan disimpan
index = 1

# Loop utama
while robot.step(4 * timestep) != -1:  # Loop berlanjut selama simulasi berjalan
    key = keyboard.getKey()  # Membaca input dari keyboard
    dir_name = 'dataset/'  # Menentukan nama direktori awal untuk menyimpan dataset
    if not os.path.isdir(dir_name):  # Membuat direktori dataset jika belum ada
        os.mkdir(dir_name)
    
    # Mengecek input dari keyboard
    if key == ord('F'):  # Jika pengguna menekan tombol 'F'
        dir_name += 'free'  # Tentukan direktori sebagai 'free'
    elif key == ord('B'):  # Jika pengguna menekan tombol 'B'
        dir_name += 'blocked'  # Tentukan direktori sebagai 'blocked'
    elif key == ord('C'):  # Jika pengguna menekan tombol 'C'
        print('Start training model.\nThis could take a while...')
        robot.step(timestep)  # Memberikan jeda untuk memulai pelatihan model
        jetbot_train.train()  # Memanggil fungsi train() dari modul jetbot_train untuk melatih model AI
        print('Trained model ready.')
        continue  # Melanjutkan loop ke iterasi berikutnya
    else:
        continue  # Jika tidak ada tombol yang ditekan, lanjutkan ke iterasi berikutnya

    # Membuat direktori 'free' atau 'blocked' jika belum ada
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    # Menyimpan gambar dari kamera robot ke dalam direktori yang sesuai
    path = os.path.join(dir_name, 'image' + str(index) + '.jpg')  # Menentukan path file gambar yang akan disimpan
    camera.saveImage(path, 100)  # Menyimpan gambar dengan kualitas 100%
    print(path)  # Menampilkan path gambar yang disimpan
    index += 1  # Menambahkan nilai index untuk penomoran gambar berikutnya
