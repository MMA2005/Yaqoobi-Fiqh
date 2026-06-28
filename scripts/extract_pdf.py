import pdfplumber
import os
import re
import glob
import arabic_reshaper
from bidi.algorithm import get_display

def process_all_pdfs_fixed(raw_dir, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    pdf_files = glob.glob(os.path.join(raw_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"❌ لم يتم العثور على أي ملفات PDF.")
        return

    print(f"📁 تم العثور على {len(pdf_files)} كتب. بدء المعالجة والتصحيح العربي...\n")
    print("-" * 50)

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        md_filename = filename.replace('.pdf', '.md')
        output_md_path = os.path.join(processed_dir, md_filename)
        
        print(f"⏳ استخراج وتصحيح كتاب: {filename}...")
        
        full_text = f"# كتاب: {filename}\n\n"
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                for i, page in enumerate(pdf.pages, 1):
                    # استخراج النص الخام
                    raw_text = page.extract_text()
                    
                    if raw_text:
                        # 1. إعادة تشكيل الحروف (ربط الحروف المقطعة)
                        reshaped_text = arabic_reshaper.reshape(raw_text)
                        
                        # 2. تعديل اتجاه النص (من اليمين لليسار)
                        bidi_text = get_display(reshaped_text)
                        
                        full_text += f"\n\n\n\n{bidi_text}"
                    
                    if i % 50 == 0 or i == total_pages:
                        print(f"  ▓ تمت معالجة {i}/{total_pages} صفحة...")

            # تنظيف المسافات والأسطر الفارغة المفرطة
            cleaned_text = re.sub(r'\n{3,}', '\n\n', full_text)
            
            with open(output_md_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
                
            print(f"✅ تم الحفظ بنجاح بتنسيق سليم في {md_filename}\n")
            
        except Exception as e:
            print(f"❌ خطأ أثناء معالجة {filename}: {e}\n")

    print("-" * 50)
    print("🎉 اكتملت العملية! يرجى مراجعة الملفات.")

if __name__ == "__main__":
    raw_folder = os.path.join("data", "raw")
    processed_folder = os.path.join("data", "processed")
    
    process_all_pdfs_fixed(raw_folder, processed_folder)