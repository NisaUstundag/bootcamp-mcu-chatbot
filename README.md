# Akbank GenAI Bootcamp: Yeni Nesil Proje Kampı

Bu proje, Akbank & Global AI Hub iş birliğiyle düzenlenen "GenAI Bootcamp: Yeni Nesil Proje Kampı" kapsamında geliştirilmiştir.

## Proje: MCU Evren Asistanı

Proje, Marvel Sinematik Evreni (MCU) karakterleri hakkında doğal dilde sorulan soruları, **Retrieval-Augmented Generation (RAG)** mimarisi kullanarak yanıtlayan bir web uygulamasıdır.

### Projenin Amacı

Bu projenin temel amacı, belirli bir bilgi alanıyla (MCU karakterleri) sınırlandırılmış, güvenilir ve bağlama uygun cevaplar üreten bir chatbot geliştirmektir. Kullanıcı, arayüzden bir karakter seçtikten sonra, o karakterle ilgili sorular sorarak anında doğru bilgilere ulaşabilir.

### Veri Seti

Projede statik bir veri seti yerine, dinamik bir veri toplama yöntemi kullanılmıştır. Kullanıcı bir karakter seçtiğinde, uygulama ilgili karakterin **Marvel Fandom Wiki** sayfasından anlık olarak metin verilerini çeker. Bu sayede her zaman güncel bilgiye erişim sağlanır.

- **Veri Kaynağı:** [Marvel Fandom Wiki](https://marvelcinematicuniverse.fandom.com/wiki/Marvel_Cinematic_Universe_Wiki)
- **Karakterler:** Iron Man, Captain America, Thor, Hulk

### Kullanılan Yöntemler

Uygulama, modern ve popüler GenAI araçları kullanılarak RAG mimarisine uygun şekilde geliştirilmiştir:

-   **Web Arayüzü:** Streamlit
-   **RAG Framework:** LangChain
-   **Generation Model:** Google Gemini API (`gemini-1.5-pro-latest`)
-   **Embedding Model:** Google Embeddings (`text-embedding-004`)
-   **Vektör Veritabanı:** FAISS
-   **Veri Çekme (Web Scraping):** BeautifulSoup4

### Elde Edilen Sonuçlar

Proje başarıyla tamamlanmış ve kullanıcıların MCU karakterleri hakkında sorular sorup, RAG mimarisi sayesinde doğru ve tutarlı cevaplar alabildiği bir web uygulaması ortaya çıkmıştır.


### Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/NisaUstundag/bootcamp-mcu-chatbot.git](https://github.com/NisaUstundag/bootcamp-mcu-chatbot.git)
    ```
2.  **Proje dizinine gidin:**
    ```bash
    cd bootcamp-mcu-chatbot
    ```
3.  **Sanal ortamı oluşturun ve aktive edin:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Gerekli kütüphaneleri kurun:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **API Anahtarını Ekleyin:**
    Proje ana dizininde `.env` adında bir dosya oluşturun ve içine kendi Google API anahtarınızı aşağıdaki gibi ekleyin:
    ```
    GOOGLE_API_KEY="AIz...SENIN_ANAHTARIN"
    ```
6.  **Uygulamayı çalıştırın:**
    ```bash
    streamlit run app.py
    ```

### Web Arayüzü Linki

Projeyi canlı olarak denemek isterseniz aşağıdaki linki kullanabilirsiniz:

[https://bootcamp-mcu-chatbot.streamlit.app/]
