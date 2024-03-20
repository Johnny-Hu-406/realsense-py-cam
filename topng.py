import os
import numpy as np
import cv2

# 資料夾路徑
folder_path = "copy_xx_captured_images"
# 輸出的 PNG 檔案儲存的資料夾路徑
output_folder = "convert_png_xx"

# 確保輸出資料夾存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 獲取資料夾下的所有 .npy 檔案
file_list = [f for f in os.listdir(folder_path) if f.endswith('color.npy')]
print(file_list)

for file_name in file_list:
    # 讀取 .npy 檔案
    np_array = np.load(os.path.join(folder_path, file_name))
    # 將 NumPy 陣列轉換為彩色影像
    # colored_image = cv2.cvtColor(np_array, cv2.COLOR_GRAY2BGR)
    # 儲存為 PNG 檔案
    output_file = os.path.splitext(file_name)[0] + '.png'
    cv2.imwrite(os.path.join(output_folder, output_file), np_array)