# RAG App

## 概要
東京農工大学皐槻祭のパンフレットを参照情報としたRAGアプリケーションです．
パンフレットの読み出しは Google Cloudの `Cloud Vision API`，ウェブフレームワークは`Streamlit`，生成AIは`gemini-1.5-flash-latest`を使っています．
## デモ
![demo](https://github.com/hokkey621/ragapp/assets/70475604/21ac02a9-3e29-484c-bda9-dfdb25629e51)
## 必要条件
このプロジェクトはRyeを使用して依存関係を管理しています．以下のパッケージが必要です:
- Python==3.12
- google-cloud-vision==3.7.2
- google-generativeai==0.5.3
- numpy==1.26.4
- opencv-python==4.9.0.80
- pdf2image==1.17.0
- streamlit==1.34.0
## ディレクトリ構造
<pre>
.
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements-dev.lock
├── requirements.lock
└── src
    ├── db
    │   ├── ocr.py
    │   ├── 第2回皐槻祭パンフレット_全体-圧縮.txt
    │   ├── 第2回皐槻祭パンフレット_全体-圧縮_formatted.txt
    │   └── 第2回皐槻祭パンフレット_全体-圧縮.pdf
    └── ragapp
        ├── __init__.py
        ├── config.py
        └── streamlit_app.py
</pre>
## 使い方
リポジトリをクローンし，必要な依存関係をインストールしてプロジェクトを実行します:

OCRをする際は`src/db/ocr.py`を実行してください．実行をする前にCloud Vision APIの設定をしてください．
```bash
python ocr.py /path/to/pdffile
```
RAGアプリケーションを実行する際は`src/ragapp/streamlit_app.py`を実行してください．
今回はローカルで実行することを想定しています．
```bash
streamlit run streamlit_app.py & sleep 3 && npx localtunnel --port 8501
```
## ライセンス
`ragapp`は[MITライセンス](https://en.wikipedia.org/wiki/MIT_License)のもとで公開されています．
