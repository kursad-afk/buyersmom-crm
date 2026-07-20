import streamlit as st
import pandas as pd
import os

# 🔒 GÜVENLİK: Giriş Bilgileri (Burayı kendinize göre değiştirebilirsiniz)
KULLANICI_ADI = "admin"
SIFRE = "Buyersmom2026!" # Şifrenizi istediğiniz gibi güncelleyin

# Verilerin kaydedileceği geçici dosya
VERI_DOSYASI = "crm_verileri.csv"

if not os.path.exists(VERI_DOSYASI):
    df = pd.DataFrame(columns=["Müşteri Adı", "Şirket", "Telefon", "E-posta", "Durum", "Notlar"])
    df.to_csv(VERI_DOSYASI, index=False)

st.set_page_config(page_title="Buyersmom CRM", layout="wide")

# Giriş Kontrol Sistemi
if "giris_yapildi" not in st.session_state:
    st.session_state["giris_yapildi"] = False

if not st.session_state["giris_yapildi"]:
    st.subheader("🔑 Buyersmom CRM Giriş Paneli")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        if username == KULLANICI_ADI and password == SIFRE:
            st.session_state["giris_yapildi"] = True
            st.success("Giriş başarılı!")
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")
    st.stop() # Giriş yapılmadıysa uygulamanın kalanını gösterme

# --- GİRİŞ YAPILDIKTAN SONRA GÖRÜNECEK CRM EKRANI ---
st.title("💼 Buyersmom CRM Takip Programı")
df_crm = pd.read_csv(VERI_DOSYASI)

# Çıkış Butonu
if st.sidebar.button("🚪 Güvenli Çıkış"):
    st.session_state["giris_yapildi"] = False
    st.rerun()

st.sidebar.header("➕ Yeni Müşteri Ekle")
yeni_ad = st.sidebar.text_input("Müşteri Adı Soyadı")
yeni_sirket = st.sidebar.text_input("Şirket Adı")
yeni_tel = st.sidebar.text_input("Telefon")
yeni_eposta = st.sidebar.text_input("E-posta")
yeni_durum = st.sidebar.selectbox("Müşteri Durumu", ["Yeni Başvuru", "Görüşme Yapılıyor", "Teklif Verildi", "Kazanıldı", "Kaybedildi"])
yeni_not = st.sidebar.text_area("Görüşme Notları")

if st.sidebar.button("Müşteriyi Kaydet"):
    if yeni_ad and yeni_sirket:
        yeni_veri = pd.DataFrame([[yeni_ad, yeni_sirket, yeni_tel, yeni_eposta, yeni_durum, yeni_not]], columns=df_crm.columns)
        df_crm = pd.concat([df_crm, yeni_veri], ignore_index=True)
        df_crm.to_csv(VERI_DOSYASI, index=False)
        st.sidebar.success(f"{yeni_ad} başarıyla kaydedildi!")
        st.rerun()
    else:
        st.sidebar.error("Lütfen alanları doldurun.")

sekme1, sekme2 = st.tabs(["📊 Müşteri Listesi & Güncelleme", "📈 Genel Özet"])

with sekme1:
    st.subheader("Mevcut Müşterileriniz")
    if df_crm.empty:
        st.info("Henüz müşteri yok.")
    else:
        st.dataframe(df_crm, use_container_width=True)
        st.write("---")
        st.subheader("🔄 Durum Güncelle veya Müşteri Sil")
        secilen_musteri = st.selectbox("Müşteri Seçin:", df_crm["Müşteri Adı"].unique())
        col1, col2 = st.columns(2)
        with col1:
            yeni_asama = st.selectbox("Yeni Durum:", ["Yeni Başvuru", "Görüşme Yapılıyor", "Teklif Verildi", "Kazanıldı", "Kaybedildi"])
            if st.button("Durumu Güncelle"):
                df_crm.loc[df_crm["Müşteri Adı"] == secilen_musteri, "Durum"] = yeni_asama
                df_crm.to_csv(VERI_DOSYASI, index=False)
                st.success("Güncellendi!")
                st.rerun()
        with col2:
            st.write(" ")
            st.write(" ")
            if st.button("🚨 Müşteriyi Sistemden Sil"):
                df_crm = df_crm[df_crm["Müşteri Adı"] != secilen_musteri]
                df_crm.to_csv(VERI_DOSYASI, index=False)
                st.warning("Silindi.")
                st.rerun()

with sekme2:
    st.subheader("Satış Süreci Analizi")
    if not df_crm.empty:
        st.bar_chart(df_crm["Durum"].value_counts())