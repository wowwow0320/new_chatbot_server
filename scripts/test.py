import os
# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv
import sys
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_core.runnables import RunnablePassthrough


# 기존 상대 경로
RELATIVE_DB_PATH = "../chroma_db"
# ✅ HuggingFace 임베딩 모델 설정

model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# 절대 경로로 변환
DB_PATH = os.path.abspath(RELATIVE_DB_PATH)
print("Chroma DB 절대 경로:", DB_PATH)  # 디버깅용 출력

# 이후에 그대로 사용
persist_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=hf_embeddings,
    collection_name="chatbot_markdown",
)