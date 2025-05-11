import os
import re
import nest_asyncio
from dotenv import load_dotenv

# 필요한 라이브러리 임포트
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

load_dotenv()
nest_asyncio.apply()

# 파서 설정
parser = LlamaParse(
    result_type="markdown",  # "markdown"과 "text" 사용 가능
    num_workers=8,
    verbose=True,
    language="ko",
)

file_extractor = {".pdf": parser}
pdf_file_path = "inform.pdf"

# PDF 파싱
documents = SimpleDirectoryReader(
    input_files=[pdf_file_path],
    file_extractor=file_extractor,
).load_data()

if not documents:
    print("파일을 파싱하는데 문제가 발생했습니다.")
else:
    print(f"{len(documents)}개의 문서가 성공적으로 파싱되었습니다.")

# ✅ 텍스트 전처리 함수
def preprocess_text(text: str) -> str:
    text = text.replace('\r\n', '\n')  # 윈도우 줄바꿈 정리
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # 문장 중간 줄바꿈 제거
    text = re.sub(r'\n{2,}', '\n\n', text)  # 문단 구분 유지 (2줄 이상 → 1줄)
    return text.strip()

# ✅ 전처리 후 마크다운 저장
output_path = "files/output.md"
try:
    with open(output_path, "w", encoding="utf-8") as md_file:
        for doc in documents:
            if hasattr(doc, 'text'):
                cleaned = preprocess_text(doc.text)
                md_file.write(cleaned)
                md_file.write("\n\n")
    print(f"마크다운 파일이 성공적으로 저장되었습니다: {output_path}")
except Exception as e:
    print(f"파일 저장 중 오류가 발생했습니다: {e}")
