import streamlit as st
import google.generativeai as genai

# Sayfa tasarımı ve başlık
st.set_page_config(page_title="Akıllı Bütçe Asistanı", page_icon="💰")
st.title("💰 Harcama Kategorizasyonu ve Bütçe Tavsiyecisi")
st.markdown("Aylık harcamalarınızı serbestçe yazın, yapay zeka sizin için kategorilesin ve tavsiye versin!")

# API Anahtarı ve Metin girişi
api_key = st.text_input("Google Gemini API Anahtarınızı girin:")
harcama_metni = st.text_area("Harcamalarınızı anlatın:", "Örn: Dün markete 500 TL verdim, bugün 200 TL kahve içtim...")

if st.button("Analiz Et"):
    if not api_key:
        st.warning("Lütfen bir API anahtarı girin.")
    elif not harcama_metni:
        st.warning("Lütfen harcamalarınızı yazın.")
    else:
        with st.spinner("Yapay zeka harcamalarınızı inceliyor..."):
            try:
                genai.configure(api_key=api_key)
                
                # SİHİRLİ KISIM: Google'ın izin verdiği çalışan ilk modeli otomatik bul!
                secilen_model = "gemini-1.5-flash" # Varsayılan
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        secilen_model = m.name
                        break
                        
                model = genai.GenerativeModel(secilen_model)
                
                # Yapay zekaya talimat
                prompt = f"""
                Şu harcama metnini incele: '{harcama_metni}'. 
                Lütfen şu adımları uygula:
                1. Harcamaları 'Gıda', 'Eğlence', 'Ulaşım' gibi mantıklı kategorilere ayır.
                2. Her kategori için ne kadar harcandığını ve toplam harcamayı hesapla.
                3. Bu harcama alışkanlıklarına göre kısa ve dostça bir finansal tavsiye ver.
                """
                
                # Cevabı alıp yazdırma
                response = model.generate_content(prompt)
                st.success("Analiz Tamamlandı!")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu. Hata detayı: {e}")
