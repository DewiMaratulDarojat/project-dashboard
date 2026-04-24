import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

# ── Page config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ── Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main { background-color: #F4F3EF; }
    .block-container { padding: 1.5rem 2.5rem 3rem; }

    /* ── Header ── */
    .db-header {
        background: #1C1C2E;
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .db-header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #EDF2FB;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .db-header-sub {
        font-size: 0.82rem;
        color: #8895A7;
        margin: 0.2rem 0 0;
    }
    .db-badge {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        color: #8895A7;
        font-size: 0.78rem;
        padding: 0.4rem 0.9rem;
        border-radius: 99px;
        font-family: 'DM Mono', monospace;
        white-space: nowrap;
    }

    /* ── Metric Cards ── */
    .metric-grid { display: flex; gap: 12px; margin-bottom: 1.4rem; }
    .metric-card {
        flex: 1;
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        border: 1px solid #E8E6E1;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 14px 14px 0 0;
    }
    .metric-card.blue::before  { background: #378ADD; }
    .metric-card.green::before { background: #27B070; }
    .metric-card.amber::before { background: #E8930A; }
    .metric-card.pink::before  { background: #D4537E; }
    .metric-label {
        font-size: 0.72rem;
        color: #8895A7;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1C1C2E;
        font-family: 'DM Mono', monospace;
        line-height: 1;
    }
    .metric-sub { font-size: 0.76rem; color: #B0BAC5; margin-top: 0.35rem; }

    /* ── Section titles ── */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #8895A7;
        margin: 0.3rem 0 0.7rem;
    }

    /* ── Chart cards ── */
    .chart-card {
        background: white;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        border: 1px solid #E8E6E1;
        height: 100%;
    }
    .chart-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: #1C1C2E;
        margin-bottom: 0.15rem;
    }
    .chart-sub {
        font-size: 0.76rem;
        color: #B0BAC5;
        margin-bottom: 1rem;
    }

    /* ── Insight box ── */
    .insight {
        background: #F4F3EF;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #4A5568;
        margin-top: 0.9rem;
        border: 1px solid #E8E6E1;
    }
    .insight b { color: #1C1C2E; }

    div[data-testid="stHorizontalBlock"] { gap: 14px; }

    /* ── Finding cards ── */
    .finding-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.4rem; }
    .finding-card {
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        border: 1px solid #E8E6E1;
    }
    .finding-icon  { font-size: 1.2rem; margin-bottom: 0.45rem; }
    .finding-title { font-size: 0.86rem; font-weight: 700; color: #1C1C2E; margin-bottom: 0.3rem; }
    .finding-body  { font-size: 0.79rem; color: #6B7280; line-height: 1.55; }
    .finding-card.dark { background: #1C1C2E; border-color: #1C1C2E; }
    .finding-card.dark .finding-title { color: #EDF2FB; }
    .finding-card.dark .finding-body  { color: #8895A7; }

    /* ── Rekomendasi ── */
    .rekom-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.4rem; }
    .rekom-card {
        background: white;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        border: 1px solid #E8E6E1;
    }
    .rekom-num   { font-size: 1.8rem; font-weight: 700; font-family: 'DM Mono', monospace; color: #E8E6E1; line-height: 1; }
    .rekom-title { font-size: 0.84rem; font-weight: 700; color: #1C1C2E; margin: 0.35rem 0 0.25rem; }
    .rekom-body  { font-size: 0.78rem; color: #6B7280; line-height: 1.5; }

    /* ── Footer ── */
    .db-footer {
        text-align: center;
        color: #B0BAC5;
        font-size: 0.76rem;
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid #E8E6E1;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Load Data
# ────────────────────────────────────────────
@st.cache_data
def load_data():
    url_day  = 'https://drive.google.com/uc?id=1dDO2C_TDEgcad2aJMRUUHiPaUV4JZMst'
    url_hour = 'https://drive.google.com/uc?id=1cbnFQ0b5ey1tI4HGQ_os8T5Ciy8NWotf'
    day_df   = pd.read_csv(url_day)
    hour_df  = pd.read_csv(url_hour)

    day_df['dteday']  = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    season_map  = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}

    for df in [day_df, hour_df]:
        df['season']     = df['season'].map(season_map)
        df['weathersit'] = df['weathersit'].map(weather_map)

    # Year column for trend chart
    day_df['year'] = day_df['dteday'].dt.year
    day_df['month_dt'] = day_df['dteday'].dt.to_period('M').dt.to_timestamp()

    return day_df, hour_df

day_df, hour_df = load_data()

# ────────────────────────────────────────────
# Sidebar Filter
# ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Bike Sharing")
    st.markdown("Analisis data penyewaan sepeda harian, Washington D.C. 2011–2012.")
    st.divider()

    st.markdown("### Filter Data")

    year_map = {2011: "2011", 2012: "2012", 0: "Semua Tahun"}
    selected_year = st.selectbox("Tahun", options=[0, 2011, 2012], format_func=lambda x: year_map[x])

    all_seasons = ["Spring", "Summer", "Fall", "Winter"]
    selected_seasons = st.multiselect("Musim", options=all_seasons, default=all_seasons)

    all_weather = day_df['weathersit'].dropna().unique().tolist()
    selected_weather = st.multiselect("Kondisi Cuaca", options=all_weather, default=all_weather)

    st.divider()
    st.caption("Dewi Maratul Darojat · Proyek Analisis Data Dicoding")

# ── Apply filters
df_filtered = day_df.copy()
if selected_year != 0:
    df_filtered = df_filtered[df_filtered['year'] == selected_year]
if selected_seasons:
    df_filtered = df_filtered[df_filtered['season'].isin(selected_seasons)]
if selected_weather:
    df_filtered = df_filtered[df_filtered['weathersit'].isin(selected_weather)]

hr_filtered = hour_df.copy()
if selected_year != 0:
    hr_filtered = hr_filtered[hr_filtered['dteday'].dt.year == selected_year]

# ────────────────────────────────────────────
# Colour palette (consistent)
# ────────────────────────────────────────────
BLUE   = '#378ADD'
GREEN  = '#27B070'
AMBER  = '#E8930A'
PINK   = '#D4537E'
GRAY   = '#E8E6E1'
TEXT   = '#1C1C2E'
MUTED  = '#8895A7'

def style_ax(ax):
    ax.set_facecolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY)
    ax.spines['bottom'].set_color(GRAY)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.yaxis.label.set_color(MUTED)
    ax.yaxis.label.set_size(9)
    ax.xaxis.label.set_color(MUTED)
    ax.xaxis.label.set_size(9)
    ax.grid(axis='y', color=GRAY, linewidth=0.8)
    ax.grid(axis='x', visible=False)

# ────────────────────────────────────────────
# Header
# ────────────────────────────────────────────
total_rentals = int(df_filtered['cnt'].sum())
avg_daily     = int(df_filtered['cnt'].mean())
peak_hour     = int(hr_filtered.groupby('hr')['cnt'].mean().idxmax())
best_weather  = df_filtered.groupby('weathersit')['cnt'].mean().idxmax()
yr0 = day_df[day_df['year'] == 2011]['cnt'].sum()
yr1 = day_df[day_df['year'] == 2012]['cnt'].sum()
growth = (yr1 - yr0) / yr0 * 100
pct_reg = df_filtered['registered'].sum() / df_filtered['cnt'].sum() * 100

st.markdown(f"""
<div class="db-header">
  <div>
    <p class="db-header-title">🚲 Bike Sharing Dashboard</p>
    <p class="db-header-sub">Proyek Analisis Data · Dewi Maratul Darojat · Dataset 2011–2012</p>
  </div>
  <span class="db-badge">{len(df_filtered):,} hari ditampilkan</span>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Metric Cards
# ────────────────────────────────────────────
st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card blue">
    <div class="metric-label">Total Penyewaan</div>
    <div class="metric-value">{total_rentals:,}</div>
    <div class="metric-sub">periode terpilih</div>
  </div>
  <div class="metric-card green">
    <div class="metric-label">Rata-rata Harian</div>
    <div class="metric-value">{avg_daily:,}</div>
    <div class="metric-sub">per hari</div>
  </div>
  <div class="metric-card amber">
    <div class="metric-label">Jam Puncak</div>
    <div class="metric-value">{peak_hour:02d}.00</div>
    <div class="metric-sub">tertinggi sepanjang hari</div>
  </div>
  <div class="metric-card pink">
    <div class="metric-label">Member Terdaftar</div>
    <div class="metric-value">{pct_reg:.1f}%</div>
    <div class="metric-sub">dari total penyewaan</div>
  </div>
  <div class="metric-card blue">
    <div class="metric-label">Pertumbuhan YoY</div>
    <div class="metric-value">+{growth:.1f}%</div>
    <div class="metric-sub">2011 → 2012</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Section 1 — Pola Jam
# ────────────────────────────────────────────


col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Pola penyewaan per jam</div><div class="chart-sub">rata-rata jumlah penyewaan tiap jam dalam sehari</div>', unsafe_allow_html=True)

    filtered = hr_filtered
    line_color = BLUE

    hourly_avg = filtered.groupby('hr')['cnt'].mean().reset_index()
    peak_r = hourly_avg.loc[hourly_avg['cnt'].idxmax()]
    low_r  = hourly_avg.loc[hourly_avg['cnt'].idxmin()]

    fig, ax = plt.subplots(figsize=(9, 3.4))
    fig.patch.set_facecolor('white')
    style_ax(ax)

    ax.fill_between(hourly_avg['hr'], hourly_avg['cnt'], alpha=0.12, color=line_color)
    ax.plot(hourly_avg['hr'], hourly_avg['cnt'], color=line_color, linewidth=2.2, zorder=3)
    ax.scatter([peak_r['hr']], [peak_r['cnt']], color=GREEN,  s=60, zorder=5, edgecolors='white', linewidth=1.5)
    ax.scatter([low_r['hr']],  [low_r['cnt']],  color='#E24B4A', s=60, zorder=5, edgecolors='white', linewidth=1.5)

    ax.annotate(f"Puncak {int(peak_r['hr'])}:00\n({int(peak_r['cnt'])})",
                xy=(peak_r['hr'], peak_r['cnt']), xytext=(peak_r['hr']-3.5, peak_r['cnt']-55),
                fontsize=7.5, color=GREEN, fontweight='600',
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))
    ax.annotate(f"Terendah {int(low_r['hr'])}:00\n({int(low_r['cnt'])})",
                xy=(low_r['hr'], low_r['cnt']), xytext=(low_r['hr']+1, low_r['cnt']+80),
                fontsize=7.5, color='#E24B4A', fontweight='600',
                arrowprops=dict(arrowstyle='->', color='#E24B4A', lw=1.2))

    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_xticks(range(0, 24))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> Penyewaan mencapai puncak saat <b>jam 08.00</b> (berangkat kerja) dan <b>17.00–18.00</b> (pulang kerja).
        Di akhir pekan, pola lebih merata di siang hari — mencerminkan penggunaan rekreasi.
    </div></div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Hari kerja vs akhir pekan</div><div class="chart-sub">perbandingan pola jam</div>', unsafe_allow_html=True)

    wday  = hr_filtered[hr_filtered['workingday']==1].groupby('hr')['cnt'].mean()
    wkend = hr_filtered[hr_filtered['workingday']==0].groupby('hr')['cnt'].mean()

    fig2, ax2 = plt.subplots(figsize=(5, 3.4))
    fig2.patch.set_facecolor('white')
    style_ax(ax2)

    ax2.plot(wday.index,  wday.values,  color=BLUE,  linewidth=2,   label='Hari Kerja')
    ax2.plot(wkend.index, wkend.values, color=PINK,  linewidth=2,   label='Akhir Pekan', linestyle='--')
    ax2.fill_between(wday.index,  wday.values,  alpha=0.07, color=BLUE)
    ax2.fill_between(wkend.index, wkend.values, alpha=0.07, color=PINK)

    p1 = mpatches.Patch(color=BLUE, label='Hari Kerja')
    p2 = mpatches.Patch(color=PINK, label='Akhir Pekan', linestyle='--')
    ax2.legend(handles=[p1, p2], fontsize=8, frameon=False, labelcolor=MUTED)
    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Rata-rata')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout(pad=0.5)
    st.pyplot(fig2)
    plt.close()

st.markdown('<br>', unsafe_allow_html=True)

# ────────────────────────────────────────────
# Section 2 — Cuaca
# ────────────────────────────────────────────


col3, col4 = st.columns(2, gap="medium")

WEATHER_COLORS = {
    'Clear':           '#378ADD',
    'Mist':            '#27B070',
    'Light Snow/Rain': '#E8930A',
    'Heavy Rain/Snow': '#E24B4A',
}

with col3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Rata-rata penyewaan per kondisi cuaca</div><div class="chart-sub">diurutkan dari tertinggi</div>', unsafe_allow_html=True)

    weather_avg = df_filtered.groupby('weathersit')['cnt'].mean().reset_index().sort_values('cnt', ascending=True)
    colors_bar  = [WEATHER_COLORS.get(w, MUTED) for w in weather_avg['weathersit']]

    fig3, ax3 = plt.subplots(figsize=(6, 3.4))
    fig3.patch.set_facecolor('white')
    style_ax(ax3)

    bars = ax3.barh(weather_avg['weathersit'], weather_avg['cnt'],
                    color=colors_bar, height=0.5, zorder=3)
    ax3.bar_label(bars, labels=[f'{v:,.0f}' for v in weather_avg['cnt']],
                  padding=8, fontsize=8, color=TEXT, fontweight='600')
    ax3.set_xlim(0, weather_avg['cnt'].max() * 1.2)
    ax3.set_xlabel('Rata-rata Penyewaan Harian')
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax3.grid(axis='x', color=GRAY, linewidth=0.8)
    ax3.grid(axis='y', visible=False)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig3)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> Cuaca cerah menghasilkan rata-rata penyewaan <b>4.500+ per hari</b>.
        Hujan lebat menyebabkan penurunan hingga <b>~91%</b> — paling drastis dibanding kondisi lain.
    </div></div>""", unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Suhu vs jumlah penyewaan</div><div class="chart-sub">per kondisi cuaca</div>', unsafe_allow_html=True)

    cuaca_filter = df_filtered['weathersit'].dropna().unique().tolist()
    filtered_weather = df_filtered[df_filtered['weathersit'].isin(cuaca_filter)]

    fig4, ax4 = plt.subplots(figsize=(6, 3.4))
    fig4.patch.set_facecolor('white')
    style_ax(ax4)

    for w in cuaca_filter:
        subset = filtered_weather[filtered_weather['weathersit'] == w]
        ax4.scatter(subset['temp'], subset['cnt'],
                    alpha=0.35, s=18,
                    color=WEATHER_COLORS.get(w, MUTED),
                    label=w, edgecolors='none')

    ax4.set_xlabel('Suhu (Normalized)')
    ax4.set_ylabel('Jumlah Penyewaan')
    ax4.legend(fontsize=7.5, frameon=False, labelcolor=MUTED, markerscale=1.5)
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.tight_layout(pad=0.5)
    st.pyplot(fig4)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> Suhu lebih hangat berkorelasi positif dengan penyewaan.
        Titik data Clear tersebar lebih luas dan tinggi — menunjukkan kombinasi terbaik.
    </div></div>""", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# ────────────────────────────────────────────
# Section 3 (BARU) — Tren Bulanan & Musim
# ────────────────────────────────────────────


col5, col6 = st.columns(2, gap="medium")

with col5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Tren penyewaan bulanan</div><div class="chart-sub">2011 vs 2012</div>', unsafe_allow_html=True)

    monthly = df_filtered.groupby(['year', 'month_dt'])['cnt'].sum().reset_index()
    m2011 = monthly[monthly['year'] == 2011]
    m2012 = monthly[monthly['year'] == 2012]

    fig5, ax5 = plt.subplots(figsize=(6, 3.4))
    fig5.patch.set_facecolor('white')
    style_ax(ax5)

    ax5.plot(range(len(m2011)), m2011['cnt'].values, color=BLUE,  linewidth=2, label='2011', marker='o', markersize=4)
    ax5.plot(range(len(m2012)), m2012['cnt'].values, color=GREEN, linewidth=2, label='2012', marker='o', markersize=4, linestyle='--')
    ax5.fill_between(range(len(m2011)), m2011['cnt'].values, alpha=0.08, color=BLUE)
    ax5.fill_between(range(len(m2012)), m2012['cnt'].values, alpha=0.08, color=GREEN)

    month_labels = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des']
    ax5.set_xticks(range(12))
    ax5.set_xticklabels(month_labels, fontsize=7.5, color=MUTED)
    ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))

    p1 = mpatches.Patch(color=BLUE, label='2011')
    p2 = mpatches.Patch(color=GREEN, label='2012')
    ax5.legend(handles=[p1, p2], fontsize=8, frameon=False, labelcolor=MUTED)
    ax5.set_ylabel('Total Penyewaan')
    plt.tight_layout(pad=0.5)
    st.pyplot(fig5)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> Penyewaan 2012 jauh lebih tinggi dari 2011 di semua bulan — menunjukkan
        <b>pertumbuhan bisnis yang konsisten</b>. Puncak di Agustus–Oktober (musim gugur).
    </div></div>""", unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Penyewaan per musim</div><div class="chart-sub">total & rata-rata harian per musim</div>', unsafe_allow_html=True)

    SEASON_COLORS = {'Fall': BLUE, 'Summer': GREEN, 'Winter': AMBER, 'Spring': PINK}
    season_stats = df_filtered.groupby('season')['cnt'].agg(['sum', 'mean']).reset_index()
    season_stats = season_stats.sort_values('sum', ascending=False)
    season_stats['color'] = season_stats['season'].map(SEASON_COLORS)

    fig6, ax6 = plt.subplots(figsize=(6, 3.4))
    fig6.patch.set_facecolor('white')
    style_ax(ax6)

    x = np.arange(len(season_stats))
    bars6 = ax6.bar(x, season_stats['sum'], color=season_stats['color'].values, width=0.55, zorder=3)
    ax6.bar_label(bars6,
                  labels=[f"{int(v/1000)}K" for v in season_stats['sum']],
                  padding=5, fontsize=8.5, color=TEXT, fontweight='600')

    ax6.set_xticks(x)
    ax6.set_xticklabels(season_stats['season'], fontsize=9, color=TEXT)
    ax6.set_ylabel('Total Penyewaan')
    ax6.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))
    ax6.set_ylim(0, season_stats['sum'].max() * 1.15)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig6)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> <b>Fall (Gugur)</b> mendominasi penyewaan — cuaca sejuk dan tidak terlalu panas ideal
        untuk bersepeda. Spring paling rendah, kemungkinan karena banyak hujan di awal musim.
    </div></div>""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Section 4 (BARU) — Casual vs Registered
# ────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)


col7, col8 = st.columns(2, gap="medium")

with col7:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Komposisi pengguna per hari dalam seminggu</div><div class="chart-sub">kasual vs terdaftar (registered)</div>', unsafe_allow_html=True)

    day_df['weekday_name'] = day_df['dteday'].dt.day_name()
    df_filtered['weekday_name'] = df_filtered['dteday'].dt.day_name()
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_labels = ['Sen','Sel','Rab','Kam','Jum','Sab','Min']
    wday_agg = df_filtered.groupby('weekday_name')[['casual','registered']].mean().reindex(day_order)

    fig7, ax7 = plt.subplots(figsize=(6, 3.4))
    fig7.patch.set_facecolor('white')
    style_ax(ax7)

    x7 = np.arange(7)
    ax7.bar(x7, wday_agg['registered'], label='Terdaftar', color=BLUE, width=0.5, zorder=3)
    ax7.bar(x7, wday_agg['casual'],     label='Kasual',    color=PINK, width=0.5, bottom=wday_agg['registered'], zorder=3)

    ax7.set_xticks(x7)
    ax7.set_xticklabels(day_labels, fontsize=9, color=TEXT)
    ax7.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax7.set_ylabel('Rata-rata Penyewaan')

    p1 = mpatches.Patch(color=BLUE, label='Terdaftar')
    p2 = mpatches.Patch(color=PINK, label='Kasual')
    ax7.legend(handles=[p1, p2], fontsize=8, frameon=False, labelcolor=MUTED)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig7)
    plt.close()

    st.markdown("""<div class="insight">
        💡 <b>Insight:</b> Pengguna terdaftar mendominasi hari kerja (commuter).
        Pengguna kasual meningkat tajam di <b>Sabtu–Minggu</b> — pengguna rekreasional.
    </div></div>""", unsafe_allow_html=True)

with col8:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi penyewaan harian</div><div class="chart-sub">histogram frekuensi jumlah penyewaan per hari</div>', unsafe_allow_html=True)

    fig8, ax8 = plt.subplots(figsize=(6, 3.4))
    fig8.patch.set_facecolor('white')
    style_ax(ax8)

    ax8.hist(df_filtered['registered'], bins=30, color=BLUE,  alpha=0.7, label='Terdaftar', edgecolor='white', linewidth=0.5, zorder=3)
    ax8.hist(df_filtered['casual'],     bins=30, color=PINK,  alpha=0.7, label='Kasual',    edgecolor='white', linewidth=0.5, zorder=3)

    ax8.axvline(df_filtered['registered'].median(), color=BLUE,  linewidth=1.5, linestyle='--', alpha=0.8)
    ax8.axvline(df_filtered['casual'].median(),     color=PINK,  linewidth=1.5, linestyle='--', alpha=0.8)

    ax8.set_xlabel('Jumlah Penyewaan per Hari')
    ax8.set_ylabel('Frekuensi')
    ax8.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax8.legend(fontsize=8, frameon=False, labelcolor=MUTED)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig8)
    plt.close()

    med_reg = int(df_filtered['registered'].median())
    med_cas = int(df_filtered['casual'].median())
    st.markdown(f"""<div class="insight">
        💡 <b>Insight:</b> Median penyewaan terdaftar = <b>{med_reg:,}</b>/hari vs kasual = <b>{med_cas:,}</b>/hari.
        Pengguna terdaftar jauh lebih banyak dan konsisten (distribusi lebih sempit).
    </div></div>""", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# ────────────────────────────────────────────
# Section 5 — Korelasi Faktor Cuaca
# ────────────────────────────────────────────
col9, col10 = st.columns([3, 2], gap="medium")

with col9:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Hubungan suhu vs jumlah penyewaan</div><div class="chart-sub">warna berdasarkan musim</div>', unsafe_allow_html=True)

    SEASON_COLORS2 = {'Spring': PINK, 'Summer': GREEN, 'Fall': BLUE, 'Winter': AMBER}
    fig9, ax9 = plt.subplots(figsize=(8, 3.4))
    fig9.patch.set_facecolor('white')
    style_ax(ax9)

    for season, grp in df_filtered.groupby('season'):
        ax9.scatter(grp['temp'], grp['cnt'],
                    color=SEASON_COLORS2.get(season, MUTED),
                    alpha=0.35, s=16, edgecolors='none', label=season)

    # Trend line
    z = np.polyfit(df_filtered['temp'], df_filtered['cnt'], 1)
    p = np.poly1d(z)
    xline = np.linspace(df_filtered['temp'].min(), df_filtered['temp'].max(), 100)
    ax9.plot(xline, p(xline), color='#E24B4A', linewidth=1.8, linestyle='--', alpha=0.8, label='Tren')

    ax9.set_xlabel('Suhu (Normalized)')
    ax9.set_ylabel('Jumlah Penyewaan')
    ax9.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    handles = [mpatches.Patch(color=SEASON_COLORS2[s], label=s) for s in SEASON_COLORS2 if s in df_filtered['season'].unique()]
    ax9.legend(handles=handles, fontsize=8, frameon=False, labelcolor=MUTED, ncol=2)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig9)
    plt.close()

with col10:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Korelasi faktor cuaca</div><div class="chart-sub">terhadap jumlah penyewaan</div>', unsafe_allow_html=True)

    corr_temp  = round(df_filtered['temp'].corr(df_filtered['cnt']), 2)
    corr_hum   = round(df_filtered['hum'].corr(df_filtered['cnt']), 2)
    corr_wind  = round(df_filtered['windspeed'].corr(df_filtered['cnt']), 2)
    corr_vals  = [corr_temp, corr_hum, corr_wind]
    corr_labels = ['Suhu', 'Kelembapan', 'Kec. Angin']
    corr_colors = [BLUE if v > 0 else '#E24B4A' for v in corr_vals]

    fig10, ax10 = plt.subplots(figsize=(5, 3.4))
    fig10.patch.set_facecolor('white')
    style_ax(ax10)

    bars10 = ax10.barh(corr_labels, corr_vals, color=corr_colors, height=0.45, zorder=3)
    ax10.bar_label(bars10, labels=[f'{v:+.2f}' for v in corr_vals],
                   padding=6, fontsize=9, color=TEXT, fontweight='600')
    ax10.axvline(0, color=GRAY, linewidth=1.2)
    ax10.set_xlim(-0.5, 0.9)
    ax10.set_xlabel('Koefisien Korelasi (r)')
    ax10.grid(axis='x', color=GRAY, linewidth=0.8)
    ax10.grid(axis='y', visible=False)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig10)
    plt.close()

    st.markdown(f"""<div class="insight">
        💡 Suhu adalah prediktor terkuat (<b>r = {corr_temp:+.2f}</b>).
        Kelembapan & angin berkorelasi negatif — makin tinggi, makin sedikit penyewaan.
    </div></div>""", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)

# ────────────────────────────────────────────
# Temuan Kunci
# ────────────────────────────────────────────
st.markdown("""
<div class="finding-grid">
  <div class="finding-card dark">
    <div class="finding-icon">📈</div>
    <div class="finding-title">Pertumbuhan 64.9% dalam setahun</div>
    <div class="finding-body">Dari 1.24 juta (2011) menjadi 2.05 juta (2012). Adopsi bike sharing tumbuh sangat pesat dalam dua tahun pertama operasional.</div>
  </div>
  <div class="finding-card">
    <div class="finding-icon">🌧️</div>
    <div class="finding-title">Hujan/salju memangkas penyewaan hingga −63%</div>
    <div class="finding-body">Rata-rata 4.877/hari saat cerah, anjlok ke 1.803 saat hujan/salju. Faktor risiko terbesar dalam operasional harian.</div>
  </div>
  <div class="finding-card">
    <div class="finding-icon">🌡️</div>
    <div class="finding-title">Suhu adalah prediktor terkuat (r = 0.63)</div>
    <div class="finding-body">Dari tiga faktor cuaca, suhu paling berpengaruh dan bisa dipakai sebagai dasar forecasting demand harian.</div>
  </div>
  <div class="finding-card">
    <div class="finding-icon">🏆</div>
    <div class="finding-title">Juni–September adalah masa panen</div>
    <div class="finding-body">Tiga bulan terbaik berturut-turut: Juni (5.772), September (5.767), Agustus (5.664) penyewaan per hari rata-rata.</div>
  </div>
  <div class="finding-card">
    <div class="finding-icon">🎉</div>
    <div class="finding-title">Hari libur justru lebih sepi (−17%)</div>
    <div class="finding-body">Rata-rata 3.735 saat hari libur vs 4.527 hari biasa. Commuter berhenti, dan pengguna kasual belum cukup menutupi.</div>
  </div>
  <div class="finding-card">
    <div class="finding-icon">👥</div>
    <div class="finding-title">Casual vs member: dua karakter berbeda</div>
    <div class="finding-body">Casual naik +126% di akhir pekan (rekreasi). Member justru lebih aktif di hari kerja untuk keperluan commuting.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Rekomendasi
# ────────────────────────────────────────────
st.markdown("""
<div class="rekom-grid">
  <div class="rekom-card">
    <div class="rekom-num">01</div>
    <div class="rekom-title">Armada musim panas</div>
    <div class="rekom-body">Tingkatkan ketersediaan sepeda di Juni–September saat demand mencapai puncak.</div>
  </div>
  <div class="rekom-card">
    <div class="rekom-num">02</div>
    <div class="rekom-title">Promo hari libur</div>
    <div class="rekom-body">Buat paket khusus akhir pekan dan hari libur untuk mendorong penyewaan kasual.</div>
  </div>
  <div class="rekom-card">
    <div class="rekom-num">03</div>
    <div class="rekom-title">Retensi member</div>
    <div class="rekom-body">Fokus program loyalitas untuk 81% pengguna terdaftar yang jadi tulang punggung pendapatan.</div>
  </div>
  <div class="rekom-card">
    <div class="rekom-num">04</div>
    <div class="rekom-title">Manajemen cuaca</div>
    <div class="rekom-body">Kurangi operasional saat prediksi hujan/salju untuk efisiensi biaya pemeliharaan armada.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────
# Raw Data Expander
# ────────────────────────────────────────────
with st.expander("Lihat Data Mentah"):
    st.dataframe(
        df_filtered[['dteday','season','weathersit','temp','hum','windspeed','casual','registered','cnt']].rename(columns={
            'dteday': 'Tanggal', 'season': 'Musim', 'weathersit': 'Cuaca',
            'temp': 'Suhu', 'hum': 'Kelembapan', 'windspeed': 'Angin',
            'casual': 'Kasual', 'registered': 'Terdaftar', 'cnt': 'Total',
        }),
        use_container_width=True,
        hide_index=True,
    )

# ── Footer
st.markdown("""
<div class="db-footer">
    Dewi Maratul Darojat · Bike Sharing Dataset 2011–2012 · Proyek Analisis Data Dicoding
</div>
""", unsafe_allow_html=True)