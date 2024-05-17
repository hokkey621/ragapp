import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import config


# 設定
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest')

def load_sentences():
    with open(config.DB_PATH, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def embed_sentences(sentences_list):
    return genai.embed_content(
        model="models/embedding-001",
        content=sentences_list,
        task_type="retrieval_document",
        title="文字列リストの埋め込み",
    )['embedding']

def embed_query(query):
    return genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_document",
        title="単一文字列の埋め込み",
    )['embedding']

def get_top_n_sentences(query_embedding, embeddings, sentences_list, n=3):
    embeddings_array = np.array(embeddings)
    query_emb = np.array(query_embedding).reshape(1, -1)
    cos_similarities = cosine_similarity(query_emb, embeddings_array)
    top_n_indices = np.argsort(cos_similarities[0])[::-1][:n]
    return [sentences_list[i] for i in top_n_indices]

def generate_response(question, reference_info):
    return model.generate_content(
        f'次の質問に対する答えを生成してください．参考情報が質問と関係ありそうな場合は参考情報を利用してください．質問：{question} 参考情報：{reference_info}'
    ).text

def init_page():
    st.set_page_config(
        page_title='RAGアプリケーションのデモ',
        page_icon="🧑‍💻"
    )
    st.header('RAGアプリケーションのデモ')

def main():
    init_page()
    sentences_list = load_sentences()
    embeddings = embed_sentences(sentences_list)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message('assistant'):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message('user'):
                st.markdown(message["content"])

    if user_input := st.chat_input('質問を入力して下さい'):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message('user'):
            st.markdown(user_input)
        with st.chat_message('assistant'):
            with st.spinner('Gemini is typing ...'):
                query_embedding = embed_query(user_input)
                top_sentences = get_top_n_sentences(query_embedding, embeddings, sentences_list)
                reference_info = " ".join(top_sentences)
                response_text = generate_response(user_input, reference_info)
                st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

if __name__ == '__main__':
    main()
