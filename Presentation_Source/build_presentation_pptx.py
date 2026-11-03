import os
from pptx import Presentation
from pptx.util import Inches

SLIDE_WIDTH_IN = 13.333333
SLIDE_HEIGHT_IN = 7.5

def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH_IN)
    prs.slide_height = Inches(SLIDE_HEIGHT_IN)
    blank_layout = prs.slide_layouts[6]
    
    png_dir = "Presentation_Source"
    
    for i in range(1, 6):
        png_path = os.path.join(png_dir, f"page_{i}.png")
        if not os.path.exists(png_path):
            png_path = os.path.join(png_dir, f"slide_{i}.png")
            
        slide = prs.slides.add_slide(blank_layout)
        # Add full-bleed high-definition slide image (16:9 widescreen)
        slide.shapes.add_picture(png_path, 0, 0, Inches(SLIDE_WIDTH_IN), Inches(SLIDE_HEIGHT_IN))
        print(f"Added Slide {i} to PowerPoint presentation from {png_path}")
        
    out_pptx = "Kathmandu_Rainfall_ML_Research_Presentation.pptx"
    prs.save(out_pptx)
    print(f"Successfully saved PowerPoint Presentation: {out_pptx} ({os.path.getsize(out_pptx)} bytes)")

if __name__ == '__main__':
    build_pptx()
