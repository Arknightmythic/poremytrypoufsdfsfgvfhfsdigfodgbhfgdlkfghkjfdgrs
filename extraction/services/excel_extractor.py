import pandas as pd
import re
import io
from fastapi import UploadFile
from dotenv import load_dotenv
import os

load_dotenv()

COLUMN_KEYWORDS = {
    "question": ["pertanyaan", "question", "soal"],
    "answer": ["jawaban", "answer", "respon"],
    "category": ["kategori", "category", "topik", "tema", "sub category"]
}


class ExcelExtractorHandler:
    def __init__(self):
        print("ExcelExtractor handler initialized")

    def _find_column(self, df, possible_names):
        for col in df.columns:
            col_clean = str(col).strip().lower()
            for name in possible_names:
                if name in col_clean:
                    return col
        return None

    def _detect_header_row(self, excel_bytes: bytes, keywords=None, max_rows=15):
        if keywords is None:
            keywords = COLUMN_KEYWORDS["question"] + COLUMN_KEYWORDS["answer"]

        preview = pd.read_excel(io.BytesIO(excel_bytes), header=None, nrows=max_rows)
        for i, row in preview.iterrows():
            row_values = " ".join(str(x).lower() for x in row.values if pd.notna(x))
            match_count = sum(1 for key in keywords if key in row_values)
            if match_count >= 2:
                return i
        return 0

    def _process_dataframe(self, df, file_name: str):
        col_question = self._find_column(df, COLUMN_KEYWORDS["question"])
        col_answer = self._find_column(df, COLUMN_KEYWORDS["answer"])
        col_category = self._find_column(df, COLUMN_KEYWORDS["category"])

        if not col_question or not col_answer:
            return f"[SKIP] {file_name}: invalid column QNA.\Detected column: {list(df.columns)}"

        default_title = os.path.splitext(file_name)[0].replace("_", " ").strip()
        default_topic = re.sub(r"\.xlsx?$", "", file_name).replace("_", " ").strip()

        results = []
        for _, row in df.iterrows():
            q = str(row.get(col_question, "")).strip()
            a = str(row.get(col_answer, "")).strip()
            cat_value = row.get(col_category, "") if col_category else ""

            if not q or not a:
                continue

            if pd.isna(cat_value) or str(cat_value).strip().lower() in ["", "nan"]:
                cat = default_topic
            else:
                cat = str(cat_value).strip()

            text_block = (
                f"document_title: {default_title}\n"
                f"document_topic: {cat}\n"
                f"chunk_description: {cat}\n\n"
                f"Q: {q}\n"
                f"A: {a}\n"
                f"---text---"
            )
            results.append(text_block)

        if not results:
            return f"[WARN] No valid entry in {file_name}"

        return "\n".join(results)

    async def extract_text(self, file: UploadFile, category: str = None) -> str:
        try:
            content = await file.read()
            header_row = self._detect_header_row(content)

            df = pd.read_excel(io.BytesIO(content), header=header_row)
            extracted_text = self._process_dataframe(df, file.filename)

            return extracted_text

        except Exception as e:
            return f"[ERROR processing uploaded file {file.filename}: {e}]"
