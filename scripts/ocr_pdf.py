import os
from pdf2image import convert_from_path
import pytesseract

def ocr_stubborn_pdf(pdf_path, output_md_path):
    print(f"⏳ جاري تحويل الكتاب إلى صور ثم استخراج النص (OCR)...")
    print(f"ملف: {pdf_path}")
    
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    full_text = f"# كتاب: الرسالة الاستفتائية (مستخرج بالـ OCR)\n\n"
    
    try:
        # تحويل الـ PDF إلى قائمة من الصور (الصفحات)
        print("📸 يتم الآن تحويل الصفحات إلى صور (قد يستغرق بعض الوقت بناءً على حجم الكتاب)...")
        images = convert_from_path(pdf_path)
        
        total_pages = len(images)
        for i, image in enumerate(images, 1):
            # استخدام محرك Tesseract مع تحديد اللغة العربية
            # إعداد --psm 6 يساعد في قراءة الكتل النصية بشكل أفضل
            custom_config = r'-l ara --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            full_text += f"\n\n\n\n{text}"
            
            # طباعة التقدم كل 10 صفحات
            if i % 10 == 0 or i == total_pages:
                print(f"  ▓ تمت معالجة {i}/{total_pages} صفحة...")
                
        # حفظ النص في ملف Markdown
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        print(f"✅ اكتملت عملية الـ OCR بنجاح! تم الحفظ في: {output_md_path}")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")

if __name__ == "__main__":
    # استهداف الملف الرئيسي المتمرد (سبل السلام)
    input_pdf = os.path.join("data", "raw", "subul.pdf")
    output_md = os.path.join("data", "processed", "subul.md")
    
    ocr_stubborn_pdf(input_pdf, output_md)