import streamlit as st


def main():
    st.title("欢迎来到第二个页面👋")
    st.sidebar.success("同时上传多个多种文件")

    file_upload = st.file_uploader("Choose a file")

    if file_upload is not None:
        # 将文件读取为字节流
        bytes_data = file_upload.getvalue()

        st.write("该功能开发中...")


if __name__ == '__main__':
    main()
