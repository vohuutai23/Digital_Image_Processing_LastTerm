import streamlit as st
import numpy as np
from PIL import Image
import cv2
def app():
    def Logarit(imgin):
        L = 256
        M, N = imgin.shape[:2]
        imgout = np.zeros((M, N), np.uint8)
        c = (L - 1) / np.log(L)
        for x in range(M):
            for y in range(N):
                r = imgin[x, y]
                if r == 0:
                    r = 1
                s = c * np.log(1 + r)
                imgout[x, y] = np.uint8(s)
        return imgout

    st.title('Ứng dụng biến đổi logarit ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Biến đổi logarit'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Logarit(frame)
            st.image(result_image, caption='Kết quả sau khi biến đổi logarit', use_column_width=True)
