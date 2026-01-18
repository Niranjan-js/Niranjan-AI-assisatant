
import os
import shutil
from livekit.agents import function_tool

@function_tool
def ocr_scan_tool(file_path: str):
    """
    Scans a document image or PDF and extracts text.
    Uses 'easyocr' for images and 'pypdf' for PDFs.
    """
    if not os.path.exists(file_path):
        return f"❌ Error: File not found at {file_path}"
    
    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""
    method_used = ""

    try:
        # Image OCR
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            try:
                import easyocr
            except ImportError:
                return "❌ Error: 'easyocr' not installed. Please run `pip install easyocr`."
            
            # Initialize reader (downloads model on first use)
            reader = easyocr.Reader(['en'], gpu=False) # GPU=False for compatibility
            result = reader.readtext(file_path, detail=0)
            extracted_text = "\n".join(result)
            method_used = "EasyOCR (Image)"

        # PDF Text Extraction
        elif ext == '.pdf':
            try:
                import pypdf
            except ImportError:
                return "❌ Error: 'pypdf' not installed. Please run `pip install pypdf`."
            
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                text_list = []
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_list.append(f"--- Page {i+1} ---\n{page_text}")
                
                extracted_text = "\n\n".join(text_list)
            method_used = f"PyPDF (Text Layer, {len(reader.pages)} pages)"
            
            if len(extracted_text.strip()) < 10:
                extracted_text += "\n[⚠️ Warning: Document appears to be scanned/empty. Image OCR for PDFs requires 'pdf2image' + Poppler.]"

        else:
            return f"❌ Unsupported file format: {ext}"

        # Save simulated ingest (Paperless-ngx style)
        ingest_dir = os.path.join(os.path.expanduser("~"), "Documents", "Niranjan_Docs_Ingest")
        if not os.path.exists(ingest_dir):
            os.makedirs(ingest_dir)
        
        filename = os.path.basename(file_path)
        dest_path = os.path.join(ingest_dir, filename)
        shutil.copy(file_path, dest_path)
        
        # Save text sidecar
        text_filename = filename + ".txt"
        with open(os.path.join(ingest_dir, text_filename), "w", encoding="utf-8") as f:
            f.write(extracted_text)

        summary_preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text

        return (f"📄 Document Processed ({method_used}):\n"
                f"- File: {filename}\n"
                f"- Saved to: {ingest_dir}\n"
                f"- Extracted Text Preview:\n{summary_preview}")

    except Exception as e:
        return f"Doc processing error: {e}"

@function_tool
def summarize_doc_tool(text_content: str):
    """
    Summarizes a long document text (Helper tool).
    """
    # Simple truncation summary for now, or could use LLM if available
    lines = text_content.split('\n')
    if len(lines) > 10:
        summary = "\n".join(lines[:10]) + "\n...(more content)..."
    else:
        summary = text_content
    return f"📝 Summary:\n{summary}"
