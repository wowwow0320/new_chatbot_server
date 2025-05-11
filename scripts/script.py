# API KEY를 환경변수로 관리하기 위한 설정 파일
# 설치: pip install python-dotenv
from dotenv import load_dotenv
import sys
import os
import warnings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utils.math import cosine_similarity  # 또는 직접 정의



# 모든 경고 무시
warnings.filterwarnings("ignore")

# 병렬 토크나이저 경고 비활성화
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# .env에서 API 키 불러오기
load_dotenv()

# HuggingFace 임베딩 모델 설정
model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Chroma DB 로드 (절대 경로로 설정)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../chroma_db"))
persist_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=hf_embeddings,
    collection_name="chatbot_markdown",
)

# 기본 Retriever 설정
retriever = persist_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "lambda_mult": 0.6, "fetch_k": 10}
)


# 프롬프트 템플릿 정의
template = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that "I don't know". 
Answer in Korean.

#Question: 
{question} 
#Context: 
{context} 

#Answer:"""
prompt = ChatPromptTemplate.from_template(template)

# LLM 정의
llm = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-4o-mini",
)

# 체인 구성
chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

# 실행부 (질문 받고 응답 출력)
if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    docs = retriever.invoke(question)

    if not docs:
        sys.stdout.write(
            "모르겠습니다.\n"
            "제가 제대로 이해하지 못했거나 챗봇에서 제공하지 않는 내용은 검색되지 않습니다.\n"
            "다른 학우들에게 도움이 될 정보인데 챗봇이 대답하지 못한다면, 우측 상단의 문의하기에 남겨주세요.\n"
        )
    else:
        response = chain.invoke(question)
        sys.stdout.write(response + "\n")
