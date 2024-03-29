import numpy as np
import cv2

# folder and img name 
save_main_folder = "captured_images"
folder_name = "1.Mature"
image_name = "image_0319_193545_88_"
# image_0306_091435_41.npycolor

folder_path = f"{save_main_folder}\\{folder_name}\\"
depth_name = f"{folder_path}{image_name}depth.npy"
color_name = f"{folder_path}{image_name}color.npy"

depth_frame = np.load(depth_name)
color_frame = np.load(color_name)

# '''
import matplotlib.pyplot as plt

depth_frame_1 = depth_frame/1000
plt.imshow(depth_frame_1, "gray")
plt.show()

# '''

#Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame)
color_image = np.asanyarray(color_frame)



while(1):
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), cv2.COLORMAP_JET)
    plt.imshow(depth_colormap, "gray")
    plt.show()  
    plt.imshow(depth_frame_1, "gray", vmin = 0, vmax = 255)
    plt.show()
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
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break