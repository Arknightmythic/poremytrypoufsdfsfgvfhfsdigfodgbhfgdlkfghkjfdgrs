from langchain_text_splitters import RecursiveCharacterTextSplitter

def recursive_chunking(text, chunk_size=2000, chunk_overlap=300):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = splitter.split_text(text)
    print(f"Text Splitter selesai — total {len(chunks)} chunk.")
    return chunks
