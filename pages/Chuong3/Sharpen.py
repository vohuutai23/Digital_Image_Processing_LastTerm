import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Định nghĩa hàm Sharpen
def Sharpen(imgin):
    L = 256  # Giả sử giá trị tối đa cho pixel là 256
    # Đạo hàm cấp 2 của ảnh
    w = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    temp = cv2.filter2D(imgin, cv2.CV_32FC1, w)
    # Tính ảnh làm sắc nét
    imgout = imgin - temp
    imgout = np.clip(imgout, 0, L - 1)
    imgout = imgout.astype(np.uint8)
    return imgout

def app():
    st.title('Ứng dụng Làm sắc nét ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Áp dụng Làm sắc nét'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            result_image = Sharpen(frame)
            st.image(result_image, caption='Kết quả sau khi áp dụng Làm sắc nét', use_column_width=True)