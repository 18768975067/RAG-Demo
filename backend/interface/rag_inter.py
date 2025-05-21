from typing import Annotated

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from fastapi import APIRouter, UploadFile, Form, File

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"  # 关闭langchain的追踪功能

rag_router = APIRouter()


# 处理文档，返回检索器
def load_txt(file: UploadFile):
    # with open('C:/Users/77149/Desktop/hello.txt','rb') as f:
    #     byte_data = f.read()
    byte_data = file.file.read()
    text_data = byte_data.decode('utf-8')
    raw_documents = [
        Document(
            page_content=text_data,
            metadata={"source": "file_path"}  # 元数据可自定义
        )
    ]

    # 加载文档并分块
    # raw_documents = TextLoader('C:/Users/77149/Desktop/hello.txt', encoding='utf-8').load()
    print(raw_documents)
    text_splitter = CharacterTextSplitter(
        separator=r'\n\n|\r\n\r\n',  # 段落分隔符（根据实际文档调整）
        chunk_size=100,  # 设置足够大的值避免段落被二次切割
        chunk_overlap=0,
        strip_whitespace=True,  # 自动清理空白符
        is_separator_regex=True
    )
    documents = text_splitter.split_documents(raw_documents)

    # 向量化并生成检索器
    embedding_model = HuggingFaceEmbeddings(model_name="D:/Project/models/all-mpnet-base-v2")
    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        # persist_directory="D:/Project/rag/backend/chroma",
    )
    retriever = db.as_retriever(search_kwargs={"k": 1})

    return retriever


def load_model():
    tokenizer = AutoTokenizer.from_pretrained("D:/Project/Model-Fine/Qwen2.5-1.5B-Instruct")
    model = AutoModelForCausalLM.from_pretrained(
        "D:/Project/Model-Fine/Qwen2.5-1.5B-Instruct",
        device_map="auto",
        trust_remote_code=True
    )
    qwen_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.8,
        device_map="auto",
        pad_token_id=tokenizer.eos_token_id  # 关键！Qwen需要特殊设置
    )
    llm = HuggingFacePipeline(pipeline=qwen_pipe)

    return llm


# 将检索到的多个文档连接起来
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@rag_router.post("/rag", summary="rag模型接口")
async def main(message: Annotated[str, Form(...)], file: UploadFile = File()):
    print(message)

    retriever = load_txt(file)
    llm = load_model()

    system_template = """根据以下上下文回答问题。
    上下文内容：
    {context}
    """
    user_template = "问题：{question}"
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(user_template),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    result = rag_chain.invoke(message)
    return {
        "answer": result
    }
