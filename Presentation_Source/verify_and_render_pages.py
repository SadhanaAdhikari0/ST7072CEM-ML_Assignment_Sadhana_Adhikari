import fitz # PyMuPDF
import os

pdf_path = 'Kathmandu_Rainfall_ML_Research_Presentation.pdf'
doc = fitz.open(pdf_path)

print(f"Total Pages in PDF: {len(doc)}")
assert len(doc) == 5, f"Expected exactly 5 pages, but found {len(doc)}!"

out_dir = 'Presentation_Source'
os.makedirs(out_dir, exist_ok=True)

for i in range(len(doc)):
    page = doc[i]
    # Render at 1.5x zoom for high definition inspection (approx 2880 x 1620)
    mat = fitz.Matrix(1.5, 1.5)
    pix = page.get_pixmap(matrix=mat)
    out_img = os.path.join(out_dir, f"page_{i+1}.png")
    pix.save(out_img)
    print(f"Saved: {out_img} ({pix.width}x{pix.height}, {os.path.getsize(out_img)} bytes)")

print("All 5 pages rendered and verified successfully!")

