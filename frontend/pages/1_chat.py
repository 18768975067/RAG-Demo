import streamlit as st
import requests


# 向后端发请求
def get_response(message, files):
    data = {
        "message": message
    }
    try:
        if not files:
            response = requests.post(
                url="http://127.0.0.1:8000/api/qwen",
                json=data
            )
            response.raise_for_status()

            # 对后端返回的json数据解封装，只保留模型生成内容
            data = response.json()
            answer = data['answer']

            return answer
        else:
            # 封装成form-data格式
            byte_data = files[0].getvalue()  # 字节流
            file = {
                "file": (files[0].name, byte_data, "text/plain")
            }

            response = requests.post(
                url="http://127.0.0.1:8000/api/rag",
                data=data,
                files=file
            )
            response.raise_for_status()

            # 对后端返回的json数据解封装，只保留模型生成内容
            data = response.json()
            answer = data['answer']

            return answer
    except requests.exceptions.RequestException as e:
        return "API请求错误:{}".format(e)


# 构建对话页面
def main():
    st.title("您的智能AI客服👋")
    st.sidebar.warning("该功能暂未实现，只能使用固定模型")
    st.sidebar.selectbox(
        "使用的语言模型：",
        ("模型1", "模型2")
    )
    st.sidebar.selectbox(
        "使用的向量化模型：",
        ("模型3", "模型4")
    )
    st.sidebar.slider(
        "选用Top-k的文档数量：", 1, 5, 2
    )

    # 增加会话状态，history保存历史记录
    if "history" not in st.session_state:
        st.session_state.history = []

    # 打印历史记录
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 如果用户输入了信息
    if user_input := st.chat_input("Chat with Alex: ", accept_file=True, file_type=["txt", "pdf"]):
        message = user_input.text
        files = user_input.files
        if not message:
            st.warning('你必须输入文本信息，否则不会执行任何操作!', icon="⚠️")
            return

        with st.chat_message("user"):
            st.markdown(message)

        # 向后端发出请求
        with st.spinner("获取输出中..."):
            response = get_response(message, files)

        with st.chat_message("assistant"):
            st.markdown(response)

        # 将用户和模型内容放入历史状态
        st.session_state.history.append({"role": "user", "content": message})
        st.session_state.history.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()
