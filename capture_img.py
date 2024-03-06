# 參考:https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/opencv_viewer_example.py
## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
import os

def save_frame(depth_frame, color_frame, file_name):
    np.save(file_name+"depth", depth_frame)
    np.save(file_name+"color", color_frame)
    # ex:image_0306_093856_20_depth.npy

save_main_folder = "captured_images/"

# 创建主文件夹（如果不存在）
if not os.path.exists(save_main_folder):
    os.makedirs(save_main_folder)

# 初始化保存图像的标志和后缀
save_flag = False
folder_name = ''


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        # 检查是否按下 'q' 键或 'Esc' 键，如果是则退出循环

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # save_frame(depth_frame.get_data(), color_frame.get_data())
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

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
            file_name = f"{folder_path}image_{current_time}_"

            # 创建文件夹（如果不存在）
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # 保存图像
            save_frame(depth_frame.get_data(), color_frame.get_data(),file_name )
            print(f"Image saved: {file_name}")
            print("\r\nPlease press the keyboard button to save the photo. ")
            print("1.Mature、2.Immature、3.overripe (slightly rotten)、4.bitten by insects")

            # 重置保存标志和文件夹名称
            save_flag = False
            folder_name = ''


finally:

    # Stop streaming
    pipeline.stop()