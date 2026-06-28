import requests
from bs4 import BeautifulSoup
import os
import re

def scrape_book_text(url, output_path):
    print(f"⏳ جاري الاتصال بالرابط: {url} ...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # سحب النص بالكامل (قد تحتاج لتعديل الـ 'div' و الـ 'class' حسب البنية الفعلية للموقع)
        # نستخدم الكلاسات الشائعة، ويمكنك فحص (Inspect) الموقع لتحديد الكلاس الدقيق إذا لزم الأمر
        content_div = soup.find('div', class_='entry-content') or soup.find('div', class_='book-content') or soup.find('body')
        
        # تنظيف العناصر غير المرغوبة
        for element in content_div(["script", "style", "nav", "footer", "header", "a"]):
            element.decompose()
            
        raw_text = content_div.get_text(separator="\n")
        
        # تنظيف المسافات والأسطر الفارغة الزائدة
        cleaned_text = re.sub(r'\n{3,}', '\n\n', raw_text).strip()
        
        # حفظ النص في المجلد المخصص
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# رسالة سبل السلام - المرجع اليعقوبي\n\n")
            f.write(cleaned_text)
            
        print(f"✅ تم سحب الكتاب وحفظه بنجاح في: {output_path}")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء سحب البيانات: {e}")

if __name__ == "__main__":
    # رابط الكتاب الذي أرسلته
    book_url = "https://library.yaqoobi.net/book/%D8%B3%D8%A8%D9%84-%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%B7%D8%A8%D8%B9%D8%A9-%D8%A7%D9%84%D8%B3%D8%A7%D8%AF%D8%B3%D8%A9"
    
    # المسار الذي سيتم حفظ الملف المنظف فيه
    output_file = os.path.join("data", "processed", "subul_al_salam.md")
    
    scrape_book_text(book_url, output_file)