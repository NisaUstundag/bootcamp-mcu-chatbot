import streamlit as st
from rag_chain import get_character_data, create_vector_store, get_conversational_chain

# --- Streamlit Arayüz Ayarları ---
st.set_page_config(page_title="MCU Evren Asistanı", layout="wide")
st.title("🤖 Marvel Sinematik Evreni Asistanı")

# CSS ile arayüzü biraz daha güzelleştirelim (Opsiyonel)
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2E2E2E;
        color: white;
    }
    .stButton>button {
        background-color: #E62429;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)


# --- Veri Yükleme ve RAG Zinciri Oluşturma ---

# Karakterlerin wiki URL'leri
# Daha fazla karakter ekleyerek chatbot'un bilgi dağarcığını genişletebilirsin.
character_urls = {
    "Iron Man": "https://marvelcinematicuniverse.fandom.com/wiki/Iron_Man",
    "Captain America": "https://marvelcinematicuniverse.fandom.com/wiki/Captain_America",
    "Thor": "https://marvelcinematicuniverse.fandom.com/wiki/Thor",
    "Hulk": "https://marvelcinematicuniverse.fandom.com/wiki/Hulk",
}

# Streamlit'in session state'ini kullanarak veritabanını ve zinciri bellekte tutuyoruz.
# Bu sayede her soru sorulduğunda tekrar tekrar veri çekip veritabanı oluşturmuyoruz.
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'chain' not in st.session_state:
    st.session_state.chain = get_conversational_chain()


# Kenar çubuğu (sidebar) oluşturma
with st.sidebar:
    st.header("Karakter Veritabanı")
    selected_character = st.selectbox("Hakkında bilgi almak istediğiniz karakteri seçin:", list(character_urls.keys()))

    if st.button("Veritabanını Yükle"):
        with st.spinner(f"{selected_character} verileri işleniyor ve vektör veritabanı oluşturuluyor... Lütfen bekleyin."):
            # Seçilen karakterin URL'sinden veriyi çek
            character_text = get_character_data(character_urls[selected_character])
            
            if character_text:
                # Vektör veritabanını oluştur
                st.session_state.vector_store = create_vector_store(character_text)
                st.success(f"{selected_character} veritabanı başarıyla yüklendi! Artık soru sorabilirsiniz.")
            else:
                st.error("Veri çekilemedi. Lütfen URL'yi kontrol edin veya başka bir karakter seçin.")

st.info("Lütfen kenar çubuğundan bir karakter seçip 'Veritabanını Yükle' butonuna basın.")

# --- Soru-Cevap Bölümü ---

# Kullanıcıdan soru almak için bir metin giriş alanı
user_question = st.text_input("Karakter hakkında sorunuzu sorun:")

# Eğer kullanıcı bir soru sorduysa ve veritabanı yüklüyse...
if user_question and st.session_state.vector_store:
    # Vektör veritabanında kullanıcının sorusuna en çok benzeyen belgeleri (chunk'ları) bul
    docs = st.session_state.vector_store.similarity_search(user_question)
    
    # Konuşma zincirini çalıştırarak cevabı üret
    response = st.session_state.chain(
        {"input_documents": docs, "question": user_question}, 
        return_only_outputs=True
    )
    
    # Üretilen cevabı ekrana yazdır
    st.write("### Cevap:")
    st.write(response["output_text"])