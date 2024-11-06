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

"""jetbot_collision_avoidance controller."""

# The code is taken from the Jupyter notebook at
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/notebooks/collision_avoidance/live_demo_resnet18.ipynb

import torch  # Mengimpor library PyTorch untuk bekerja dengan model deep learning
import torchvision.transforms as transforms  # Mengimpor modul transformasi untuk preprocessing data gambar
import torch.nn.functional as F  # Mengimpor fungsi aktivasi dan utilitas lainnya dari PyTorch
import torchvision  # Mengimpor library torchvision untuk model pre-trained
import PIL.Image  # Mengimpor modul untuk mengelola gambar dari pustaka PIL
import os.path  # Mengimpor modul untuk operasi terkait path

from jetbot_python_control import JetBot  # Mengimpor kelas JetBot untuk mengontrol robot JetBot

# Menetapkan nilai mean dan standar deviasi untuk normalisasi gambar
mean = torch.Tensor([0.485, 0.456, 0.406])  # Nilai mean untuk normalisasi
std = torch.Tensor([0.229, 0.224, 0.225])  # Nilai standar deviasi untuk normalisasi

# Mengonfigurasi fungsi normalisasi dengan mean dan std yang telah ditetapkan
normalize = torchvision.transforms.Normalize(mean, std)

# Menentukan path untuk model yang telah dilatih
model_path = 'best_model_resnet18.pth'


# Fungsi untuk melakukan preprocessing pada gambar dari kamera
def preprocessCameraImage(camera):
    global device, normalize  # Menggunakan variabel global device dan normalize
    data = camera.getImage()  # Mengambil data gambar dari kamera
    # Mengonversi data gambar menjadi objek PIL Image dan mengonversinya ke RGB
    image = PIL.Image.frombytes('RGBA', (camera.getWidth(), camera.getHeight()), data, 'raw', 'BGRA').convert('RGB')
    # Mengonversi gambar ke tensor dan mengirimnya ke perangkat (device)
    image = transforms.functional.to_tensor(image).to(device)
    # Melakukan normalisasi pada gambar dengan mean dan std yang telah ditetapkan
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]  # Mengembalikan gambar sebagai batch dengan ukuran 1

# Memeriksa apakah file model yang dilatih ada
if not os.path.isfile(model_path):
    print('Trained model "' + model_path + '" not found, please use the "jetbot_collect_data" controller to generate it.')
    exit()  # Keluar dari program jika model tidak ditemukan

# Membuat instance JetBot
robot = JetBot()

# Mengatur timestep untuk kontrol
timestep = 5 * int(robot.getBasicTimeStep())

# Mengaktifkan kamera dengan timestep yang telah ditentukan
robot.camera.enable(timestep)

# Menunggu beberapa waktu agar kamera siap
robot.step(10 * timestep)

print('Load the trained model..')  # Menampilkan pesan bahwa model sedang dimuat
# Memuat model ResNet-18 dan mengganti lapisan output terakhir sesuai kebutuhan
model = torchvision.models.resnet18(weights=None)  # Menginisialisasi model ResNet-18 tanpa bobot pre-trained
model.fc = torch.nn.Linear(512, 2)  # Mengubah lapisan terakhir untuk menghasilkan dua output (free atau blocked)
device = torch.device('cpu')  # Menetapkan perangkat (device) sebagai CPU
model.load_state_dict(torch.load(model_path))  # Memuat bobot model yang dilatih dari file
model = model.to(device)  # Mengirim model ke perangkat (device) CPU
model = model.eval()  # Mengatur model ke mode evaluasi (inference)


# Loop utama
print('Start collision avoidance control..')  # Menampilkan pesan kontrol penghindaran tabrakan dimulai
direction = ''  # Variabel untuk menyimpan arah pergerakan terakhir
while robot.step(timestep) != -1:  # Melakukan iterasi selama simulasi berjalan
    camera_value = preprocessCameraImage(robot.camera)  # Memproses gambar dari kamera
    y = model(camera_value)  # Mendapatkan prediksi dari model
    y = F.softmax(y, dim=1)  # Menghitung softmax untuk mendapatkan distribusi probabilitas
    prob_blocked = float(y.flatten()[0])  # Mengambil probabilitas bahwa jalan terhalang
    if prob_blocked < 0.5:  # Jika probabilitas blocked < 0.5
        # Deteksi jalan bebas: bergerak maju
        if direction != 'forward':  # Mengecek apakah arah terakhir bukan 'forward'
            robot.forward(0.5)  # Menggerakkan robot maju dengan kecepatan 0.5
            direction = 'forward'  # Mengatur arah terakhir sebagai 'forward'
    elif direction != 'left':  # Jika jalan terhalang dan arah terakhir bukan 'left'
        # Deteksi tepi: robot harus berbelok
        direction = 'left'  # Mengatur arah terakhir sebagai 'left'
        robot.left(0.4)  # Menggerakkan robot untuk berbelok kiri dengan kecepatan 0.4
    pass  # Melanjutkan ke iterasi berikutnya