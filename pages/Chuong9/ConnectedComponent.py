import streamlit as st
import numpy as np
import cv2
from PIL import Image

L = 256

def MyConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 200, L-1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    M, N = temp.shape
    dem = 0
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            if temp[x,y] == L-1:
                mask = np.zeros((M+2,N+2), np.uint8)
                cv2.floodFill(temp, mask, (y,x), (color,color,color))
                dem = dem + 1
                color = color + 1
    a = np.zeros(L, int) 
    for x in range(0, M):
        for y in range(0, N):
            r = temp[x,y]
            if r > 0:
                a[r] = a[r] + 1
    dem = 1
    for r in range(0, L):
        if a[r] > 0:
            st.write('%4d   %5d' % (dem, a[r]))
            dem = dem + 1
    return temp

def ConnectedComponent(imgin):
    ret, temp = cv2.threshold(imgin, 200, L-1, cv2.THRESH_BINARY)
    temp = cv2.medianBlur(temp, 7)
    dem, label = cv2.connectedComponents(temp)
    text = 'Co %d thanh phan lien thong' % (dem-1) 

    a = np.zeros(dem, int)  
    M, N = label.shape
    color = 150
    for x in range(0, M):
        for y in range(0, N):
            r = label[x, y]
            a[r] = a[r] + 1
            if r > 0:
                label[x,y] = label[x,y] + color

    for r in range(1, dem):
        st.write('%4d %10d' % (r, a[r]))
    label = label.astype(np.uint8)
    cv2.putText(label, text, (1,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
    return label

def app():
    st.title('Đếm Thành Phần Liên Thông')

    st.markdown('**Vui lòng tải lên hình ảnh miếng phi lê gà:**')
    img_file_buffer = st.file_uploader("", type=["bmp", "png", "jpg", "jpeg"])
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        st.image(image, caption='Hình ảnh được tải lên', use_column_width=True)

        frame = np.array(image.convert('L')) 

        if st.button('Đếm Thành Phần Liên Thông'):
            result_image = MyConnectedComponent(frame)
            st.image(result_image, caption='Kết quả sau khi đếm', use_column_width=True)
