import os
import pymupdf as fitz

SOURCE_PDF = "Kathmandu_Rainfall_ML_Research_Presentation_Vector.pdf"
OUTPUT_PDF = "Kathmandu_Rainfall_ML_Research_Presentation.pdf"
PNG_DIR = "Presentation_Source"

def render_and_compile():
    print(f"Opening source vector PDF: {SOURCE_PDF}")
    src_doc = fitz.open(SOURCE_PDF)
    num_pages = len(src_doc)
    print(f"Total pages detected: {num_pages}")
    
    # Target 16:9 widescreen dimensions (pt)
    PAGE_W = 1920
    PAGE_H = 1080
    
    # 1.5x zoom gives 2880x1620 (crystal crisp, high DPI)
    zoom = 1.5
    matrix = fitz.Matrix(zoom, zoom)
    
    rendered_pngs = []
    
    for i in range(num_pages):
        page = src_doc[i]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        
        # Save both page_X.png and slide_X.png for consistency
        page_png = os.path.join(PNG_DIR, f"page_{i+1}.png")
        slide_png = os.path.join(PNG_DIR, f"slide_{i+1}.png")
        
        pix.save(page_png)
        pix.save(slide_png)
        rendered_pngs.append(page_png)
        print(f"Rendered Page {i+1}: {page_png} ({pix.width}x{pix.height}, {os.path.getsize(page_png)} bytes)")
        
    src_doc.close()
    
    print("\nCompiling all rendered PNG slides into unified Master Presentation PDF...")
    out_doc = fitz.open()
    
    for i, png_file in enumerate(rendered_pngs):
        # Create exact 16:9 widescreen page
        new_page = out_doc.new_page(width=PAGE_W, height=PAGE_H)
        # Insert image full-bleed to match 1920x1080 bounds
        rect = fitz.Rect(0, 0, PAGE_W, PAGE_H)
        new_page.insert_image(rect, filename=png_file)
        print(f"Embedded Slide {i+1} into Master PDF")
        
    out_doc.save(OUTPUT_PDF, deflate=True)
    out_doc.close()
    
    print(f"\nSuccessfully generated Master Presentation PDF: {OUTPUT_PDF}")
    print(f"File Size: {os.path.getsize(OUTPUT_PDF)} bytes")
    
    # Verification
    check_doc = fitz.open(OUTPUT_PDF)
    print(f"Verification: {len(check_doc)} pages in {OUTPUT_PDF}")
    for p_idx, p in enumerate(check_doc):
        print(f"  Page {p_idx+1}: {p.rect.width} x {p.rect.height} pt (Aspect: {p.rect.width/p.rect.height:.3f})")
    check_doc.close()

if __name__ == '__main__':
    render_and_compile()

