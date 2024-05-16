import streamlit as st
from pages.Chuong3 import Negative, Logarit, Power, PiecewiseLinear, Histogram, HistEqual, HistEqualColor, LocalHist, HistStat, BoxFilter 
from pages.Chuong3 import GaussianFilter, Threshold, MedianFilter, Sharpen, Gradient

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.selectbox(
            'Chọn chủ đề:',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()

app = MultiApp()

st.subheader("""
Bài tập đồ án xử lý ảnh chương 3
""")
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

app.add_app("Làm âm ảnh (Negative)", Negative.app)
app.add_app("Logarit ảnh", Logarit.app)
app.add_app("Lũy thừa ảnh (Power)", Power.app)
app.add_app("Biến đổi tuyến tính từng phần (PiecewiseLinear)", PiecewiseLinear.app)
app.add_app("Histogram", Histogram.app)
app.add_app("Cân bằng Histogram (HistEqual)", HistEqual.app)
app.add_app("Cân bằng Histogram của ảnh màu (HistEqualColor)", HistEqualColor.app)
app.add_app("Local Histogram (LocalHist)", LocalHist.app)
app.add_app("Thống kê histogram (HistStat)", HistStat.app)
app.add_app("Lọc box (BoxFilter)", BoxFilter.app)
app.add_app("Lọc Gauss (GaussianFilter)", GaussianFilter.app)
app.add_app("Phân ngưỡng (Threshold)", Threshold.app)
app.add_app("Lọc median (MedianFilter)", MedianFilter.app)
app.add_app("Sharpen", Sharpen.app)
app.add_app("Gradient", Gradient.app)

app.run()