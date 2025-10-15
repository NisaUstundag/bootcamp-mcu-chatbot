# Gerekli kütüphaneleri import ediyoruz.
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# LangChain kütüphanelerini import ediyoruz.
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


# .env dosyasındaki environment değişkenlerini yükler.
# Bu sayede os.environ.get('GOOGLE_API_KEY') komutuyla anahtara erişebiliriz.
load_dotenv()

def get_character_data(url):
    """
    Belirtilen URL'den bir Marvel karakterinin metin verilerini çeker.
    Sadece ana içerik alanındaki metinleri alır ('mw-content-text').
    """
    try:
        response = requests.get(url)
        # HTTP isteği başarılıysa devam et (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Fandom wiki'lerindeki ana içerik genellikle bu div içinde bulunur.
            content_div = soup.find(id='mw-content-text')
            
            if content_div:
                # Reklamları, navigasyon kutularını ve diğer istenmeyen elementleri temizleyelim.
                for unwanted_tag in content_div.select('.mw-references-wrap, .reference, .toc, .thumb, .gallery, .infobox'):
                    unwanted_tag.decompose()
                
                # Sadece temizlenmiş metni al
                text = content_div.get_text(separator='\n', strip=True)
                return text
            else:
                return "İçerik alanı bulunamadı."
        else:
            return f"Sayfa yüklenemedi. Status Kodu: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Bir hata oluştu: {e}"

def create_vector_store(text):
    """
    Verilen metni parçalara ayırır, embedding'lerini oluşturur ve 
    bir FAISS vektör veritabanı oluşturur.
    """
    if not text:
        print("Metin içeriği boş, işlem yapılamıyor.")
        return None

    # 1. Metin Parçalama (Splitting)
    # Metni daha küçük, yönetilebilir parçalara ayırıyoruz.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200, # Parçalar arası anlam bütünlüğü için overlap değerini artırdık.
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    if not chunks:
        print("Metin parçalara ayrılamadı.")
        return None

    # 2. Embedding Modelini Yükleme
    # Google'ın text-embedding-004 modelini kullanarak metinleri vektörlere dönüştüreceğiz.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # 3. Vektör Veritabanı Oluşturma (FAISS)
    # Metin parçalarını ve embedding modelini kullanarak veritabanını oluşturuyoruz.
    db = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    return db

def get_conversational_chain():
    """
    Kullanıcı sorusuna ve bulunan belgelere dayanarak cevap üretecek olan
    konuşma zincirini (conversational chain) oluşturur ve döndürür.
    """
    # Cevabın nasıl formatlanması gerektiğini belirleyen şablon (prompt template)
    prompt_template = """
    Verilen bilgilere dayanarak soruyu detaylı bir şekilde cevapla. Eğer cevap metinlerde yoksa, "Bu konuda bilgim yok" de.\n\n
    Bağlam:\n {context}?\n
    Soru: \n{question}\n

    Cevap:
    """
    

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
    # Prompt şablonunu oluşturuyoruz.
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # LangChain'in soru-cevap zincirini yüklüyoruz.
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    return chain