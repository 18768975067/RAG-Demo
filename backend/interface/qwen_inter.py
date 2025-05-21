from typing import Union

from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM

qwen_router = APIRouter()


# 接收的前端数据格式
class Data(BaseModel):
    message: str = None


@qwen_router.post("/qwen", summary="大语言模型接口")
def generate_response(data: Data):
    message = data.message

    model_path = "D:/Project/Model-Fine/Qwen2.5-1.5B-Instruct"
    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype="auto"
    )

    # 构建模型输入（Qwen的指令模板）
    message = f"<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"

    # 编码输入
    inputs = tokenizer(message, return_tensors="pt").to(model.device)

    # 直接生成完整输出
    output_ids = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id
    )

    # 解码并截断输入部分，这里只保留模型的生成内容
    input_length = inputs.input_ids.shape[1]
    response = tokenizer.decode(
        output_ids[0][input_length:],
        skip_special_tokens=True
    )

    # 将用户问题和模型生成结果组成json返回
    return {
        "message": message,
        "answer": response
    }
