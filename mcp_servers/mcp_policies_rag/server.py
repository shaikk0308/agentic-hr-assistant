import sqlite3  # (not used now, but fine if you want later)
from pathlib import Path

from fastmcp import FastMCP
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings

BASE_DIR = Path(__file__).resolve().parents[2]  # employee-assistant/
PDF_DIR = BASE_DIR / "docs" / "policies"
VECTOR_DIR = BASE_DIR / "vectorstore"
VECTOR_DIR.mkdir(exist_ok=True)

mcp = FastMCP("policies-rag-server")


def get_chroma_collection():
    client = chromadb.PersistentClient(
        path=str(VECTOR_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_or_create_collection("policies_collection")


def pdf_to_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    texts = []
    for page in reader.pages:
        t = page.extract_text() or ""
        texts.append(t)
    return "\n\n".join(texts).strip()


@mcp.tool()
def list_policy_pdfs():
    """
    List all policy PDFs available for RAG ingestion.
    """
    if not PDF_DIR.exists():
        return {
            "success": False,
            "message": f"PDF directory does not exist: {PDF_DIR}",
            "files": [],
        }

    files = [
        f.name
        for f in PDF_DIR.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    return {
        "success": True,
        "dir": str(PDF_DIR),
        "files": files,
    }


@mcp.tool()
def build_policy_index():
    """
    Build or rebuild the Chroma index from the policy PDFs.
    Reads all PDFs in docs/policies, extracts text, and indexes them.
    """
    try:
        if not PDF_DIR.exists():
            return {
                "success": False,
                "message": f"PDF directory does not exist: {PDF_DIR}",
            }

        pdf_files = [
            p for p in PDF_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
        ]
        if not pdf_files:
            return {
                "success": False,
                "message": f"No PDF files found in {PDF_DIR}",
            }

        collection = get_chroma_collection()

        ids = []
        docs = []
        metas = []

        for pdf_path in pdf_files:
            text = pdf_to_text(pdf_path)
            if not text:
                continue

            doc_id = pdf_path.name  # e.g. "leave_policy.pdf"
            ids.append(doc_id)
            docs.append(text)
            metas.append(
                {
                    "filename": pdf_path.name,
                    "path": str(pdf_path),
                }
            )

        if not ids:
            return {
                "success": False,
                "message": "No text extracted from any PDFs.",
            }

        collection.delete(ids=ids)
        collection.add(ids=ids, documents=docs, metadatas=metas)

        return {
            "success": True,
            "indexed_count": len(ids),
            "indexed_files": ids,
        }
    except Exception as e:
        # Log error and return it so we can see what went wrong
        return {
            "success": False,
            "message": f"build_policy_index failed: {type(e).__name__}: {e}",
        }


@mcp.tool()
def rag_search_policies(question: str, top_k: int = 3):
    """
    Use Chroma to find the most relevant policy text for a natural-language question.
    Returns top_k matches with text and metadata.
    """
    collection = get_chroma_collection()

    result = collection.query(
        query_texts=[question],
        n_results=top_k,
    )

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]

    items = []
    for text, meta in zip(docs, metas):
        items.append(
            {
                "text": text,
                "metadata": meta,
            }
        )

    return {
        "success": True,
        "matches": items,
    }

if __name__ == "__main__":
    # Debug: print registered tools
    try:
        tool_names = [t.name for t in mcp.tools]
    except Exception:
        tool_names = []
    print("Registered FastMCP tools:", tool_names)

    mcp.run()



if __name__ == "__main__":
    mcp.run()
