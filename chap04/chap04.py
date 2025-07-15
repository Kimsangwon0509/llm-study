import pymupdf
import os

pdf_file= '../chap04/data/소프트웨어사업영향평가_가이드라인_1810152.pdf'
doc = pymupdf.open(pdf_file)

full_text = ''

header_height = 90
footer_height = 100


for page in doc:
    rect = page.rect
    header = page.get_text(clip=(0, 0, rect.width, header_height))
    footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))
    text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))
    full_text += text + '\n----------------------------------\n'


    #text = page.get_text()
    #full_text += text

pdf_file_name = os.path.basename(pdf_file)
pdf_file_name = os.path.splitext(pdf_file_name)[0] # 확장자 제거
#txt_file_path = f'../chap04/data/{pdf_file_name}.txt'
txt_file_path = f'../chap04/data/{pdf_file_name}_with_preprocessing.txt'
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)
