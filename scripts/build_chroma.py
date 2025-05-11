from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# ✅ 환경 변수 및 설정
load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ✅ 텍스트 로딩
loader = TextLoader("files/output.md", encoding="utf-8")  # 인코딩 명시 추천
documents = loader.load()
markdown_document = documents[0].page_content  # 파일 내용 문자열 추출

# ✅ 마크다운 헤더 기준으로 1차 분할
headers_to_split_on = [
    ("#", "Header 1")
]
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)
md_header_splits = markdown_splitter.split_text(markdown_document)

# ✅ 문자 기준으로 2차 분할
chunk_size = 300  # 각 청크의 최대 길이
chunk_overlap = 20  # 청크 간 중복 문자 수
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
split_doc = text_splitter.split_documents(md_header_splits)

# ✅ HuggingFace 임베딩 설정
model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# ✅ Chroma DB에 문서 저장
DB_PATH = "../chroma_db"
persist_db = Chroma.from_documents(
    split_doc,
    hf_embeddings,
    persist_directory=DB_PATH,
    collection_name="chatbot_markdown"
)
