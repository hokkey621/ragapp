import io
import os
import sys
from google.cloud import vision
from PIL import Image
from pdf2image import convert_from_path
from typing import List

def pdf2images(pdf_path: str) -> List[Image.Image]:
    """
    PDFファイルを画像に変換する。

    Args:
        pdf_path (str): PDFファイルのパス。

    Returns:
        List[Image.Image]: 変換された画像のリスト。
    """
    images = convert_from_path(pdf_path)
    return images

def img2txt_GCP(image: Image.Image) -> str:
    """
    Google Cloud Vision APIを使用して画像からテキストを抽出する。

    Args:
        image (Image.Image): 入力画像。

    Returns:
        str: 抽出されたテキスト。
    """
    # 改行するテキストのリスト
    enter_txt = ['。', '.', '！', '!', '？', '?']  
    client = vision.ImageAnnotatorClient()

    # 画像をバイト配列に変換
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    content = img_byte_arr.getvalue()

    vision_image = vision.Image(content=content)
    response = client.document_text_detection(image=vision_image, image_context={'language_hints': ['ja']})

    output_text = ''
    # 抽出されたテキストをページごとに処理
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if symbol.text in enter_txt:
                            output_text += symbol.text + '\n'
                        else:
                            output_text += symbol.text
    return output_text

def main(argv):
    """
    メイン関数。入力ファイルを読み込み、テキストを抽出して出力ファイルに保存する。

    Args:
        argv: コマンドライン引数。
    """
    if len(argv) != 2:
        print("Usage: python ocr.py <input_file>")
        sys.exit(1)
    
    input_path = argv[1]
    output_path = os.path.splitext(input_path)[0] + ".txt"

    text = ""
    if input_path.lower().endswith('.pdf'):
        images = pdf2images(input_path)
        for image in images:
            text += img2txt_GCP(image)
    else:
        image = Image.open(input_path)
        text = img2txt_GCP(image)
    
    # 出力ファイルにテキストを書き込む
    with open(output_path, "w") as file:
        file.write(text)
    print(f"Extracted text saved to: {output_path}")

if __name__ == "__main__":
    main(sys.argv)
