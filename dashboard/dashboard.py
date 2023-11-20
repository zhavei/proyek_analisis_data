import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

'''Tahap berikutnya adalah menyiapkan 
DataFrame yang akan digunakan untuk membuat visualisasi data. Untuk melakukan hal ini, 
kita perlu membuat beberapa helper function seperti berikut. Sebagai catatan, kode di 
bawah ini merupakan contoh kode yang telah kita  gunakan pada materi latihan sebelumnya.'''

#create_daily_orders_df() digunakan untuk menyiapkan daily_orders_df.
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

#create_sum_order_items_df() bertanggung jawab untuk menyiapkan sum_orders_items_df.
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

#create_bygender_df() digunakan untuk menyiapkan bygender_df.
def create_bygender_df(df):
    bygender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
    bygender_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bygender_df

#create_byage_df() merupakan helper function yang digunakan untuk menyiapkan byage_df.
def create_byage_df(df):
    byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])
    
    return byage_df

# create_bystate_df() digunakan untuk menyiapkan bystate_df.
def create_bystate_df(df):
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

#create_rfm_df() bertanggung jawab untuk menghasilkan rfm_df.
def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

'''Nah, setelah menyiapkan beberapa helper function tersebut, tahap berikutnya
ialah load berkas all_data.csv sebagai sebuah DataFrame menggunakan kode berikut.'''

all_df = pd.read_csv("all_data.csv")

'''Seperti yang telah kita lihat pada materi Latihan Exploratory Data Analysis, all_df memiliki dua kolom yang bertipe datetime, 
yaitu order_date dan delivery_date. Kolom order_date inilah yang akan menjadi kunci dalam pembuatan filter nantinya. Nah, untuk 
mendukung hal ini, kita perlu mengurutkan DataFrame berdasarkan order_date serta memastikan kedua kolom tersebut bertipe datetime.  
Berikut kode yang dapat kita gunakan untuk melakukan hal tersebut.'''

datetime_columns = ["order_date", "delivery_date"]
all_df.sort_values(by="order_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
## membuat komponen filter