import streamlit as st
import numpy as np
from PIL import Image
import cv2

def Gradient(imgin):
    L = 256 
    sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_y = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    mygx = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_x)
    mygy = cv2.filter2D(imgin, cv2.CV_32FC1, sobel_y)

    imgout = abs(mygx) + abs(mygy)
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def app():
    st.title('Ứng dụng Phát hiện cạnh bằng Gradient')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Gradient'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Gradient(frame)
            st.image(result_image, caption='Kết quả sau khi áp dụng Gradient', use_column_width=True)
