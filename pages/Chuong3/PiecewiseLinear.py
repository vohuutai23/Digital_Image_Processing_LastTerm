import streamlit as st
import numpy as np
from PIL import Image
import cv2

def PiecewiseLinear(imgin):
    L = 256
    M, N = imgin.shape[:2]
    imgout = np.zeros((M, N), np.uint8)
    rmin, rmax, _, _ = cv2.minMaxLoc(imgin)
    r1 = rmin
    s1 = 0
    r2 = rmax
    s2 = L - 1
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            if r < r1:
                s = s1 / r1 * r
            elif r < r2:
                s = (s2 - s1) / (r2 - r1) * (r - r1) + s1
            else:
                s = (L - 1 - s2) / (L - 1 - r2) * (r - r2) + s2
            imgout[x, y] = np.uint8(s)
    return imgout

def app():
    st.title('Ứng dụng biến đổi tuyến tính từng phần ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Biến đổi tuyến tính từng phần'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = PiecewiseLinear(frame)
            st.image(result_image, caption='Kết quả sau khi áp dụng biến đổi tuyến tính từng phần', use_column_width=True)