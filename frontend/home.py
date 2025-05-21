import streamlit as st


def main():
    st.set_page_config(
        page_title="Home",
        layout="wide"
    )
    st.title("系统功能介绍👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        这是一个基于RAG的应用，您可以构建个人知识库，用于辅助个人工作学习等用途，也可以基于该项目进行扩展研究。
        ### 使用方法
        - 您可以选择不上传文件，但这样只会调用普通的语言模型
        - 您可以上传附件，模型会对文档分块检索出和问题相关的信息，再进行回答
        - 您可以任意选择向量化模型和语言模型，以及文档的检索策略
        - 目前模型仅可以处理txt文件，后续扩展后可处理html,md,pdf,csv,Office及自定义文件
        ### 注意事项
        - 本应用不会泄露任何您的个人隐私信息
        - 若对该应用有任何问题，可以联系邮箱771493528@qq.com
        ### 项目源码
        """
    )

    st.link_button("Go to GitHub","https://github.com/18768975067/rag-demo")


if __name__ == '__main__':
    main()
