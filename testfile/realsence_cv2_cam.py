import cv2
import numpy as np
import datetime
import time
import os

# 打开摄像机
cap = cv2.VideoCapture(0)

# 指定保存图像的主文件夹
save_main_folder = "captured_images/"

# 创建主文件夹（如果不存在）
if not os.path.exists(save_main_folder):
    os.makedirs(save_main_folder)

# 初始化保存图像的标志和后缀
save_flag = False
folder_name = ''

while True:
    # 读取摄像机画面
    ret, frame = cap.read()

    # 显示画面
    cv2.imshow("Camera", frame)

    # 检查是否按下 'q' 键或 'Esc' 键，如果是则退出循环
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        print("user interrupt")
        break

    # 如果按下 '1'、'2' 或 '3' 键，设置保存标志和文件夹名称
    if key == ord('1'):
        save_flag = True
        folder_name = "1.Mature"
    elif key == ord('2'):
        save_flag = True
        folder_name = "2.Immature"
    elif key == ord('3'):
        save_flag = True
        folder_name = "3.overripe (slightly rotten)"
    elif key == ord('4'):
        save_flag = True
        folder_name = "4.bitten by insects"        

    # 获取当前时间（不包含年份，添加毫秒）
    current_time = datetime.datetime.now().strftime("%m%d_%H%M%S_%f")[:-4]

    # 如果保存标志为真，保存图像
    if save_flag:
        # 构建文件夹路径和文件名
        folder_path = f"{save_main_folder}{folder_name}/"
        file_name = f"{folder_path}image_{current_time}.npy"

        # 创建文件夹（如果不存在）
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 保存图像
        np.save(file_name, frame)
        print(f"Image saved: {file_name}")
        print("\r\nPlease press the keyboard button to save the photo. ")
        print("1.Mature、2.Immature、3.overripe (slightly rotten)、4.bitten by insects")

        # 重置保存标志和文件夹名称
        save_flag = False
        folder_name = ''

# 释放摄像机资源
cap.release()

# 关闭所有窗口
cv2.destroyAllWindows()
