import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from gpu_exporter import get_gpu_details # Yardımcı dosyamızdan veriyi çekiyoruz

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="Local GPU Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Stil (Daha modern görünüm için) ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background-color: #00ADB5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Local GPU Monitoring Dashboard")
st.caption("Real-time tracking of NVIDIA GPU resources")

# --- Yer Tutucular (Canlı güncellenecek alanlar) ---
col1, col2, col3 = st.columns(3)
with col1:
    placeholder_temp = st.empty()
with col2:
    placeholder_load = st.empty()
with col3:
    placeholder_mem = st.empty()

st.divider()
placeholder_chart = st.empty()
placeholder_table = st.empty()

# --- Veri Geçmişi (Grafik için) ---
if 'history_temp' not in st.session_state:
    st.session_state['history_temp'] = []
    st.session_state['history_time'] = []

# --- Ana Döngü (Verileri sürekli günceller) ---
def update_dashboard():
    while True:
        gpu_data = get_gpu_details()
        
        if not gpu_data:
            st.error("GPU bulunamadı veya NVIDIA sürücüleri yüklü değil.")
            time.sleep(5)
            continue

        gpu = gpu_data[0] # İlk GPU'yu al

        # 1. Metrik Kartları
        placeholder_temp.metric(label="Sıcaklık (°C)", value=f"{gpu['temperature']} °C", delta=None)
        placeholder_load.metric(label="GPU Yükü (%)", value=f"{gpu['load']}%")
        placeholder_mem.metric(label="Bellek (VRAM)", value=f"{gpu['memory_used']} / {gpu['memory_total']} MB")

        # 2. Grafik Verisi Güncelleme
        current_time = pd.Timestamp.now().strftime('%H:%M:%S')
        st.session_state['history_temp'].append(gpu['temperature'])
        st.session_state['history_time'].append(current_time)

        # Listeyi son 50 veriyle sınırla (Hafıza şişmesin)
        if len(st.session_state['history_temp']) > 50:
            st.session_state['history_temp'].pop(0)
            st.session_state['history_time'].pop(0)

        # 3. Grafik Çizimi
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state['history_time'], 
            y=st.session_state['history_temp'],
            mode='lines+markers',
            name='Sıcaklık',
            line=dict(color='#FF4B4B', width=2)
        ))
        fig.update_layout(
            title="Sıcaklık Zaman Çizelgesi",
            xaxis_title="Saat",
            yaxis_title="Derece (°C)",
            template="plotly_dark",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        placeholder_chart.plotly_chart(fig, use_container_width=True)

        # 4. Yenileme Hızı
        time.sleep(2) # 2 saniyede bir günceller

if __name__ == "__main__":
    update_dashboard()
