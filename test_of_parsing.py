"""try:
    with open('a.txt', mode='r') as f:
        a = f.read()
        b = str(f)
        b = b.replace(f"<_io.TextIOWrapper name='{f.name}' mode='r' encoding='", '')
        b = b.replace("'>", '')
        a = a.encode(b)
        a = a.decode('utf-8')
        if 'Наркотики' in a:
            print('ААААА')
except:
    try:
        with open('a.txt', mode='r') as f:
            a = f.read()
            if 'Наркотики' in a:
                print('ААААА')
    except:
        pass

#Greate
"""
"""import  csv
with open('D:/Тест/Лист Microsoft Excel.csv', mode='r', encoding='utf-8') as f:
    a = f.read()
    print(a)"""
"""from docx import Document

document = Document('D:/Тест/Тест.docx')
for para in document.paragraphs:
    print(para.text)"""
"""import PyPDF2
import pdfminer
from pdfminer.high_level import extract_text
a = extract_text('D:/Users/pavel/Desktop/Сервис удаления/Документы к проекту/ПЗ - Чуйко Павел Алексеевич - Сервис удаления запрещенного контента.pdf')
a = str(a)
a = a.lower()
print(a)"""
"""import docx2txt
text = docx2txt.process("D:/Тест/Тест.docx")
text=str(text)
print(text)"""

