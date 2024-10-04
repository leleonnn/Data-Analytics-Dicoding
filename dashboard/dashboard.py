import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;  /* Set text color to black */
    }
    .stApp {
        background-color: white;
        color: black;  /* Set text color to black */
    }
    .sidebar .sidebar-content {
        background: white;
        color: black;  /* Set sidebar text color to black */
    }
    h1, h2, h3, h4, h5, h6, p {
        color: black;  /* Ensure headers and paragraphs are black */
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data(dir):
    df = pd.read_csv(dir)
    return df

st.title("- Dashboard -")
st.write("""
by Leonard Mars Kurniaputra
""")

script_dir = os.path.dirname(os.path.realpath(__file__))
hour_df = load_data(f'{script_dir}/hour.csv')
day_df = load_data(f'{script_dir}/day.csv')

count_by_weather_df = hour_df.groupby("weathersit").agg({
    "cnt": "mean",
    "casual": "mean",
    "registered": "mean"
}).sort_values(by="weathersit", ascending=True).reset_index()

count_by_weather_df["weathersit"] = str(count_by_weather_df["weathersit"])
category = ["Cerah", "Berawan", "Ringan", "Ekstrim"]
for i, index in enumerate(count_by_weather_df.index):
    count_by_weather_df.loc[index, "weathersit"] = category[i]

tab1, tab2 = st.tabs(["Jumlah Rental Per Kondisi Cuaca", "Tren Jumlah Rental Per Tahun"])

with tab1:
    st.subheader("Perbandingan Rata-Rata Rental Berdasarkan Kondisi Cuaca")

    plot_option = st.selectbox(
        "Kategori:",
        ("All", "Kategori Pelanggan")
    )

    if plot_option == "Kategori Pelanggan":
        plt.figure(figsize=(10, 10))
        Palette = sns.color_palette("Reds", n_colors=4)
        ax = sns.barplot(
            x="weathersit", 
            y="value", 
            hue="variable",
            data=count_by_weather_df.melt(id_vars=["weathersit"], value_vars=["casual", "registered"]),
            palette=Palette
        )
        plt.ylabel("Rata-Rata Rental Per Jam")
        plt.xlabel("Kondisi Cuaca")
        plt.title("Perbandingan Rata-Rata Rental Kategori Pelanggan Dalam Setiap Kondisi Cuaca")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f")
        plt.legend(title="Kategori Rental", labels=["Casual", "Registered"])
        st.pyplot(plt)

    else:
        plt.figure(figsize=(10, 10))
        ax = sns.barplot(y="cnt", x="weathersit", data=count_by_weather_df, palette=["#FF7F7F"], hue="weathersit", legend=False)
        plt.xlabel("Rata-Rata Rental Per Jam")
        plt.ylabel("Kondisi Cuaca")
        plt.title("Perbandingan Rata-Rata Rental Dalam Setiap Kondisi Cuaca")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f")
        st.pyplot(plt)

with tab2:
    st.subheader("Perbandingan Jumlah Rental Tahun 2011 dan 2012")

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    day_df['dteday'] = day_df['dteday'].dt.strftime('%m-%d')
    weekday_df_2011 = day_df[day_df["yr"] == 0][["dteday", "cnt"]].sort_values(by="dteday", ascending=True).reset_index(drop=True)
    weekday_df_2012 = day_df[day_df["yr"] == 1][["dteday", "cnt"]].sort_values(by="dteday", ascending=True).reset_index(drop=True)

    color_scheme = st.selectbox(
        "Tahun",
        ("All", "2011", "2012")
    )

    plt.figure(figsize=(10, 6))

    if color_scheme == "All":
        plt.plot(weekday_df_2012["dteday"], weekday_df_2012["cnt"], linestyle="-", color="b", label="2012")
        plt.plot(weekday_df_2011["dteday"], weekday_df_2011["cnt"], linestyle="-", color="g", label="2011")
    elif color_scheme == "2011":
        plt.plot(weekday_df_2012["dteday"], weekday_df_2012["cnt"], linestyle="-", color="gray", label="2012")
        plt.plot(weekday_df_2011["dteday"], weekday_df_2011["cnt"], linestyle="-", color="g", label="2011")
    else:
        plt.plot(weekday_df_2012["dteday"], weekday_df_2012["cnt"], linestyle="-", color="b", label="2012")
        plt.plot(weekday_df_2011["dteday"], weekday_df_2011["cnt"], linestyle="-", color="gray", label="2011")

    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Rental")
    plt.title("Perbandingan Jumlah Rental Tahun 2011 dengan Tahun 2012")
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
