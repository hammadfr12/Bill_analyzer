import tempfile, os, pytesseract
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_images(path: str) -> list[Image.Image]:
    return convert_from_path(path, dpi=300)

def image_to_text(img: Image.Image) -> str:
    return pytesseract.image_to_string(img, lang="eng")

def file_to_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg"]:
        return image_to_text(Image.open(file_path))
    elif ext == ".pdf":
        text = ""
        for img in pdf_to_images(file_path):
            text += "\n" + image_to_text(img)
        return text
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
