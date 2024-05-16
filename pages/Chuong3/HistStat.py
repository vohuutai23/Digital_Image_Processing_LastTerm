import streamlit as st
import numpy as np
from PIL import Image
import cv2

def HistStat(imgin):
    hist = cv2.calcHist([imgin], [0], None, [256], [0, 256])
    mean_val = np.mean(imgin)
    std_dev = np.std(imgin)
    return hist, mean_val, std_dev

def app():
    st.title('Ứng dụng Thống kê Histogram ảnh')

    st.markdown('**Vui lòng tải lên hình ảnh:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image)

        if st.button('Thống kê Histogram'):
            if len(frame.shape) == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            hist, mean_val, std_dev = HistStat(frame)
            st.write(f'Giá trị trung bình của ảnh: {mean_val:.2f}')
            st.write(f'Độ lệch chuẩn của ảnh: {std_dev:.2f}')
            st.bar_chart(hist)