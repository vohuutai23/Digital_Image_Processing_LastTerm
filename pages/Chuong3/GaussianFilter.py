import streamlit as st
import numpy as np
from PIL import Image
import cv2

def GaussianFilter(imgin, kernel_size=3, sigma=1):
    imgout = cv2.GaussianBlur(imgin, (kernel_size, kernel_size), sigma)
    return imgout

def app():
    st.title('Ứng dụng Lọc Gauss ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Lọc Gauss'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                B, G, R = cv2.split(frame)
                B_filtered = GaussianFilter(B)
                G_filtered = GaussianFilter(G)
                R_filtered = GaussianFilter(R)
                frame_filtered = cv2.merge((B_filtered, G_filtered, R_filtered))
                frame_filtered = cv2.cvtColor(frame_filtered, cv2.COLOR_BGR2RGB)
            else:
                frame_filtered = GaussianFilter(frame)
            st.image(frame_filtered, caption='Kết quả sau khi áp dụng Lọc Gauss', use_column_width=True)