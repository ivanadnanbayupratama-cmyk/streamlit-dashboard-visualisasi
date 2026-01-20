import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
# =============================
# IDENTITAS MAHASISWA
# =============================
NAMA = "Haydar Fahri Alaudin"
NIM = "32602300010"
# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title=f"{NAMA} | {NIM} | Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)
# =============================
# FIX HEADER STREAMLIT (PADDING TOP)
# =============================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =============================
# HEADER IDENTITAS (PASTI TAMPIL)
# =============================
st.markdown(
    f"""
    <div style="
        background: rgba(0,0,0,0.35);
        padding: 14px 22px;
        border-radius: 14px;
        margin-bottom: 18px;
        width: fit-content;
    ">
        <span style="color:white; font-size:16px;">
            <b>Nama:</b> {NAMA} &nbsp; | &nbsp;
            <b>NIM:</b> {NIM}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
# =============================
# CUSTOM STYLE
# =============================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    section {
        background: linear-gradient(180deg, #112937, #111827);
    }
    section * {
        color: white;
    }
    .metric-card {
        background: rgba(0,0,0,0.85);
        color: white;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    .metric-card h4 {
        color: #000000;
        margin-bottom: 6px;
    }
    .metric-card h2 {
        color: #333333;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =============================
# LOAD DATASET
# =============================
datasets = {
    "Tips": sns.load_dataset("tips"),
    "Iris": sns.load_dataset("iris"),
    "Titanic": sns.load_dataset("titanic"),
    "Flights": sns.load_dataset("flights")
}
# =============================
# SIDEBAR
# =============================
st.sidebar.title("🎛️ Dashboard Control")
dataset_name = st.sidebar.selectbox(
    "Pilih Dataset",
    list(datasets.keys())
)
plot_type = st.sidebar.selectbox(
    "Jenis Visualisasi",
    ["Scatter Plot", "Bar Chart", "Line Plot"]
)
df = datasets[dataset_name]
numeric_cols = df.select_dtypes(include="number").columns.tolist()

x_col = st.sidebar.selectbox("X Axis", df.columns)
y_col = st.sidebar.selectbox(
    "Y Axis (Numerik)",
    numeric_cols if numeric_cols else df.columns
)
# =============================
# TITLE
# =============================
st.title("📊 Data Visualization Dashboard")
st.caption(f"Dataset aktif: **{dataset_name}**")
# =============================
# METRICS
# =============================
c1, c2, c3, c4 = st.columns(4)
c1.markdown(
    f"<div class='metric-card'><h4>Total Data</h4><h2>{len(df)}</h2></div>",
    unsafe_allow_html=True
)
c2.markdown(
    f"<div class='metric-card'><h4>Rata-rata</h4><h2>{df[y_col].mean():.2f}</h2></div>",
    unsafe_allow_html=True
)
c3.markdown(
    f"<div class='metric-card'><h4>Nilai Maks</h4><h2>{df[y_col].max():.2f}</h2></div>",
    unsafe_allow_html=True
)
c4.markdown(
    f"<div class='metric-card'><h4>Nilai Min</h4><h2>{df[y_col].min():.2f}</h2></div>",
    unsafe_allow_html=True
)
st.markdown("---")
# =============================
# VISUALIZATION
# =============================
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("📌 Matplotlib")
    fig, ax = plt.subplots()
    if plot_type == "Scatter Plot":
        ax.scatter(df[x_col], df[y_col])
    elif plot_type == "Bar Chart":
        df.groupby(x_col)[y_col].mean().plot(kind="bar", ax=ax)
    elif plot_type == "Line Plot":
        df.groupby(x_col)[y_col].mean().plot(ax=ax)
    ax.set_title("Matplotlib Chart")
    st.pyplot(fig)
with col2:
    st.subheader("📌 Seaborn")
    fig, ax = plt.subplots()
    if plot_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    elif plot_type == "Bar Chart":
        sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
    elif plot_type == "Line Plot":
        sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
    ax.set_title("Seaborn Chart")
    st.pyplot(fig)
with col3:
    st.subheader("📌 Plotly")
    if plot_type == "Scatter Plot":
        fig = px.scatter(df, x=x_col, y=y_col, color=x_col)
    elif plot_type == "Bar Chart":
        fig = px.bar(df, x=x_col, y=y_col, color=x_col)
    elif plot_type == "Line Plot":
        fig = px.line(df, x=x_col, y=y_col, markers=True)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis=dict(gridcolor="rgba(255,255,255,0.2)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.2)")
    )
    st.plotly_chart(fig, use_container_width=True)
