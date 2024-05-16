import streamlit as st
from pages.Chuong5 import CreateMotionfilter, DenoiseMotion, DenoisestMotion
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
Bài tập đồ án xử lý ảnh chương 5
""")
st.sidebar.title("Nhóm sinh viên thực hiện:")
st.sidebar.write("""
                - 1. **Hành Phúc Công - 21110817**
                - 2. **Võ Hữu Tài - 21110294**
                """)

app.add_app("Tạo nhiễu chuyển động (CreateMotionfilter)", CreateMotionfilter.app)
app.add_app("Gỡ nhiễu của ảnh có ít nhiễu (DenoiseMotion)", DenoiseMotion.app)
app.add_app("Gỡ nhiễu của ảnh có nhiều nhiễu (DenoisestMotion)", DenoisestMotion.app)

app.run()