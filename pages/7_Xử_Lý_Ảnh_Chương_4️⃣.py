import streamlit as st
from pages.Chuong4 import Spectrum, FrequencyFilter, RejectFilter, RemoveMoire
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
Bài tập đồ án xử lý ảnh chương 4
""")
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

app.add_app("Spectrum", Spectrum.app)
app.add_app("Lọc trong miền tần số  (FrequencyFilter)", FrequencyFilter.app)
app.add_app("Vẽ bộ lọc Notch Reject (RejectFilter)", RejectFilter.app)
app.add_app("Xóa nhiễu moire (RemoveMoire)", RemoveMoire.app)

app.run()