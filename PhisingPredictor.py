import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from nltk.tokenize import RegexpTokenizer
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from nltk.stem.snowball import SnowballStemmer


st.title('Prediksi Website Phishing Menggunakan Machine Learning :fish:')
st.subheader('by: Kelompok 7 / Tim Hore Hore Hackathon :star:')
st.caption('Members: Tiara Angelica, Annisa Salsabila Ahdyani, Ina Mutmainah')

st.image("https://csirt.umm.ac.id/wp-content/uploads/2022/06/bigstock-Data-Phishing-Hacker-Attack-t-319270852.jpg")

"""
Phishing adalah upaya untuk mendapatkan informasi data seseorang dengan teknik pengelabuan. 
Data yang menjadi sasaran phising adalah data pribadi (nama, usia, alamat), data akun (username dan password), 
dan data finansial (informasi kartu kredit, rekening). Istilah resmi phising adalah phishing, yang berasal dari kata fishing yaitu memancing.

Informasi yang didapat atau dicari oleh phiser adalah berupa password account atau nomor kartu kredit korban. 
Penjebak/phiser menggunakan email, banner atau pop-up window untuk menjebak user agar mengarahkan ke situs web palsu (fake webpage), 
dimana user diminta untuk memberikan informasi pribadinya. Disinilah phiser memanfaatkan kecerobohan dan 
ketidak-telitian user dalam web palsu tersebut untuk mendapatkan informasi.

"""
phishing_data = st.selectbox("Pilih dataset phishing URLs yang sudah kami siapkan untuk digunakan", ("C:\\Users\\TIARA ANGELICA S\\Downloads\\phishing_site_urls.xlsx","data-sample-2"))
st.markdown("**atau**")

uploaded_file = st.file_uploader("Mau upload datanya sendiri? Monggo...")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    #st.dataframe(df)
    st.caption('Terima kasih buat datanya :D')

if not uploaded_file:
    df = pd.read_excel(phishing_data)
    #st.dataframe(df)
    st.caption('Mari kita gunakan data ini.')


"""
Mengenai Dataset:

"""
lbl_counts = pd.DataFrame(phishing_data.Label.value_counts())
sns.set_style('darkgrid')
sns.barplot(lbl_counts.index, lbl_counts.Label)
st.pyplot()

tokenizer = RegexpTokenizer(r'[A-Za-z]+')
st.write(phishing_data.URL[0])

clean_text = tokenizer.tokenize(phishing_data.URL[0])
st.write(clean_text)

import time
start = time.time()
phishing_data['text_tokenized'] = phishing_data.URL.map(lambda text: tokenizer.tokenize(text))
end = time.time()
time_req = end - start
formatted_time = "{:.2f}".format(time_req)
st.write(f"Time required to tokenize text is: \n{formatted_time} sec")

st.dataframe(phishing_data.sample(7))

sbs = SnowballStemmer("english")
start = time.time()
phishing_data['text_stemmed'] = phishing_data['text_tokenized'].map(lambda text: [sbs.stem(word) for word in text])
end = time.time()
time_req = end - start
formatted_time = "{:.2f}".format(time_req)
print(f"??? Time required for stemming all the tokenized text is: \n{formatted_time} sec")


predict_bad = ['www.yeniik.com.tr/wp-admin/js/login.alibaba.com/login.jsp.php',
    'www.fazan-pacir.rs/temp/libraries/ipad',
    'www.tubemoviez.exe/',
    'www.svision-online.de/mgfi/administrator/components/com_babackup/classes/fx29id1.txt']
predict_good = ['www.youtube.com/','www.python.org/', 'www.google.com/', 'www.kaggle.com/']

loaded_model = pickle.load(open('C:\\Users\\TIARA ANGELICA S\\Downloads\\phishing.pkl', 'rb'))

result_1 = loaded_model.predict(predict_bad)
result_2 = loaded_model.predict(predict_good)

st.write(f"{result_1} \n {'-'*26} \n{result_2}")