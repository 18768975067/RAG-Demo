import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.interface.qwen_inter import qwen_router
from backend.interface.rag_inter import rag_router

app = FastAPI()

# 处理跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(qwen_router, prefix="/api", tags=["AI客服接口"])
app.include_router(rag_router,prefix="/api", tags=["AI客服接口"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
