import streamlit as st
import numpy as np
from PIL import Image
import cv2

def Power(imgin, gamma=5.0):
    L = 256
    M, N = imgin.shape[:2]
    imgout = np.zeros((M, N), np.uint8)
    c = np.power(L-1, 1-gamma)
    for x in range(M):
        for y in range(N):
            r = imgin[x, y]
            s = c * np.power(r, gamma)
            imgout[x, y] = np.uint8(s)
    return imgout

def app():
    st.title('Ứng dụng biến đổi lũy thừa ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Biến đổi lũy thừa'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Power(frame)
            st.image(result_image, caption='Kết quả sau khi áp dụng biến đổi lũy thừa', use_column_width=True)