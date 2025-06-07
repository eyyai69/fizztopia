import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Media Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Translation Dictionary ---
translations = {
    "en": {
        "main_title": "Interactive Media Intelligence Dashboard",
        "main_subtitle": "Upload your social media data to generate insights.",
        "upload_title": "Upload your CSV File",
        "upload_help": "Please select a CSV file with the columns: Date, Platform, Sentiment, Location, Engagements, Media Type.",
        "filter_title": "Filters",
        "date_range": "Date Range",
        "platform": "Platform",
        "sentiment": "Sentiment",
        "media_type": "Media Type",
        "all": "All",
        "chart_title_sentiment": "Sentiment Breakdown",
        "chart_title_engagement_trend": "Engagement Trend Over Time",
        "chart_title_platform": "Platform Engagements",
        "chart_title_media_type": "Media Type Mix",
        "chart_title_location": "Top 5 Locations by Engagement",
        "generate_gemini_btn": "Generate Gemini AI Analysis",
        "generate_openrouter_btn": "Generate with OpenRouter AI",
        "download_pdf_btn": "Download Report (PDF)",
        "insights_title": "Key Insights:",
        "dominant_sentiment": "<b>Overall Tone:</b> The conversation is predominantly <b>{0}</b> ({1}%), setting the general tone for public reception.",
        "sentiment_anomaly": "<b>Anomaly Detected:</b> A significant volume of <b>{0}</b> sentiment on {1} suggests a specific event or piece of content drove a strong reaction.",
        "sentiment_ratio": "<b>Sentiment Ratio:</b> The ratio of Positive to Negative sentiment is <b>{0}</b>.",
        "engagement_spike": "<b>Engagement Spike:</b> A notable spike on <b>{0}</b> ({1}) suggests a highly successful post or event.",
        "lowest_engagement": "<b>Learning Opportunity:</b> The lowest engagement occurred on <b>{0}</b>, providing a chance to analyze underperforming content.",
        "steady_growth": "<b>Performance Trend:</b> Engagement shows a general trend of {0}, indicating the current strategy is {1}.",
        "platform_dominance": "<b>Platform Focus:</b> <b>{0}</b> overwhelmingly dominates engagement ({1}%).",
        "platform_efficiency": "<b>Emerging Opportunity:</b> <b>{0}</b> shows high content efficiency (engagement per post).",
        "underperforming_platform": "<b>Strategic Review:</b> <b>{0}</b> is the lowest-performing platform by engagement.",
        "media_engagement_mismatch": "<b>Strategy Mismatch:</b> <b>{0}</b> is most-produced, but <b>{1}</b> drives more engagement per post.",
        "media_engagement_match": "<b>Content Synergy:</b> The most-produced type, <b>{0}</b>, is also the most engaging.",
        "least_engaging_media": "<b>Efficiency Check:</b> <b>{0}</b> generates the least engagement.",
        "location_concentration": "<b>Market Concentration:</b> Engagement is heavily concentrated in <b>{0}</b> ({1}%).",
        "emerging_market": "<b>Emerging Market:</b> <b>{0}</b> shows promise as a secondary market.",
        "geographic_reach": "<b>Geographic Reach:</b> Content reached <b>{0}</b> distinct locations.",
        "summary_title": "Executive Summary & Recommendations",
        "summary_perf_title": "Overall Performance Summary",
        "summary_reco_title": "Strategic Campaign Recommendations",
        "openrouter_settings_title": "OpenRouter AI Settings",
        "openrouter_api_key_label": "OpenRouter API Key",
        "openrouter_model_label": "Select AI Model",
        "api_key_error": "OpenRouter API Key is required.",
        "no_data": "No data available for the selected filters.",
        "gemini_summary_title": "Executive Summary & Recommendations (Gemini AI)",
        "openrouter_summary_title": "Analysis from OpenRouter AI ({0})",
    },
    "id": {
        "main_title": "Dasbor Intelijen Media Interaktif",
        "main_subtitle": "Unggah data media sosial Anda untuk menghasilkan wawasan.",
        "upload_title": "Unggah File CSV Anda",
        "upload_help": "Silakan pilih file CSV dengan kolom: Date, Platform, Sentiment, Location, Engagements, Media Type.",
        "filter_title": "Filter",
        "date_range": "Rentang Tanggal",
        "platform": "Platform",
        "sentiment": "Sentimen",
        "media_type": "Jenis Media",
        "all": "Semua",
        "chart_title_sentiment": "Rincian Sentimen",
        "chart_title_engagement_trend": "Tren Keterlibatan dari Waktu ke Waktu",
        "chart_title_platform": "Keterlibatan Platform",
        "chart_title_media_type": "Campuran Jenis Media",
        "chart_title_location": "5 Lokasi Teratas berdasarkan Keterlibatan",
        "generate_gemini_btn": "Hasilkan Analisis AI Gemini",
        "generate_openrouter_btn": "Hasilkan dengan OpenRouter AI",
        "download_pdf_btn": "Unduh Laporan (PDF)",
        "insights_title": "Wawasan Utama:",
        "dominant_sentiment": "<b>Nada Keseluruhan:</b> Percakapan didominasi oleh sentimen <b>{0}</b> ({1}%), yang menentukan nada umum penerimaan publik.",
        "sentiment_anomaly": "<b>Anomali Terdeteksi:</b> Volume sentimen <b>{0}</b> yang signifikan pada tanggal {1} menunjukkan peristiwa atau konten tertentu yang memicu reaksi kuat.",
        "sentiment_ratio": "<b>Rasio Sentimen:</b> Rasio sentimen Positif terhadap Negatif adalah <b>{0}</b>.",
        "engagement_spike": "<b>Lonjakan Keterlibatan:</b> Lonjakan yang signifikan pada <b>{0}</b> ({1}) menunjukkan postingan atau acara yang sangat sukses.",
        "lowest_engagement": "<b>Peluang Belajar:</b> Keterlibatan terendah terjadi pada <b>{0}</b>, memberikan kesempatan untuk menganalisis konten yang berkinerja buruk.",
        "steady_growth": "<b>Tren Kinerja:</b> Keterlibatan menunjukkan tren umum {0}, yang mengindikasikan strategi saat ini {1}.",
        "platform_dominance": "<b>Fokus Platform:</b> <b>{0}</b> sangat mendominasi keterlibatan ({1}%).",
        "platform_efficiency": "<b>Peluang Baru:</b> <b>{0}</b> menunjukkan efisiensi konten yang tinggi (keterlibatan per postingan).",
        "underperforming_platform": "<b>Tinjauan Strategis:</b> <b>{0}</b> adalah platform dengan kinerja terendah berdasarkan keterlibatan.",
        "media_engagement_mismatch": "<b>Ketidaksesuaian Strategi:</b> Meskipun <b>{0}</b> adalah jenis konten yang paling banyak diproduksi, <b>{1}</b> mendorong keterlibatan yang jauh lebih tinggi per postingan.",
        "media_engagement_match": "<b>Sinergi Konten:</b> Jenis konten yang paling banyak diproduksi, <b>{0}</b>, juga yang paling menarik.",
        "least_engaging_media": "<b>Pemeriksaan Efisiensi:</b> <b>{0}</b> menghasilkan keterlibatan paling sedikit.",
        "location_concentration": "<b>Konsentrasi Pasar:</b> Keterlibatan sangat terkonsentrasi di <b>{0}</b> ({1}%).",
        "emerging_market": "<b>Pasar Berkembang:</b> <b>{0}</b> menunjukkan potensi sebagai pasar sekunder.",
        "geographic_reach": "<b>Jangkauan Geografis:</b> Konten telah menjangkau <b>{0}</b> lokasi yang berbeda.",
        "summary_title": "Ringkasan & Rekomendasi Eksekutif",
        "summary_perf_title": "Ringkasan Kinerja Keseluruhan",
        "summary_reco_title": "Rekomendasi Kampanye Strategis",
        "openrouter_settings_title": "Pengaturan OpenRouter AI",
        "openrouter_api_key_label": "Kunci API OpenRouter",
        "openrouter_model_label": "Pilih Model AI",
        "api_key_error": "Kunci API OpenRouter diperlukan.",
        "no_data": "Tidak ada data yang tersedia untuk filter yang dipilih.",
        "gemini_summary_title": "Ringkasan & Rekomendasi Eksekutif (Gemini AI)",
        "openrouter_summary_title": "Analisis dari OpenRouter AI ({0})",
    }
}

# --- State Management ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'

# --- Helper Functions ---
def T(key):
    return translations[st.session_state.lang].get(key, key)

@st.cache_data
def clean_data(df):
    """Cleans and preprocesses the uploaded dataframe."""
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['engagements'] = pd.to_numeric(df['engagements'], errors='coerce').fillna(0)
    df.dropna(subset=['date'], inplace=True)
    return df

def get_summary_data(df):
    """Generates a summary dictionary from the dataframe for AI prompts."""
    summary = {}
    
    # Platform data
    platform_engagements = df.groupby('platform')['engagements'].sum().sort_values(ascending=False)
    summary['top_platform'] = platform_engagements.index[0] if not platform_engagements.empty else 'N/A'
    
    # Sentiment data
    sentiment_counts = df['sentiment'].value_counts()
    summary['dominant_sentiment'] = sentiment_counts.index[0] if not sentiment_counts.empty else 'N/A'
    summary['sentiment_distribution'] = sentiment_counts.to_dict()

    # Media type data
    media_engagements = df.groupby('media_type')['engagements'].sum().sort_values(ascending=False)
    summary['top_media_type'] = media_engagements.index[0] if not media_engagements.empty else 'N/A'
    
    # Location data
    location_engagements = df.groupby('location')['engagements'].sum().sort_values(ascending=False)
    summary['top_location'] = location_engagements.index[0] if not location_engagements.empty else 'N/A'
    
    return summary

# --- Sidebar ---
with st.sidebar:
    st.sidebar.title("Settings")
    
    # Language switcher
    st.session_state.lang = st.radio("Language", ["en", "id"], format_func=lambda x: "English" if x == "en" else "Indonesia")

    # File uploader
    uploaded_file = st.file_uploader(
        T("upload_title"),
        type=["csv"],
        help=T("upload_help")
    )

    df_filtered = pd.DataFrame()

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df_cleaned = clean_data(df.copy())
        
        st.header(T("filter_title"))
        
        # Date filter
        min_date = df_cleaned['date'].min().date()
        max_date = df_cleaned['date'].max().date()
        date_range = st.date_input(
            T("date_range"),
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        # Other filters
        platform_options = [T("all")] + df_cleaned['platform'].unique().tolist()
        sentiment_options = [T("all")] + df_cleaned['sentiment'].unique().tolist()
        media_type_options = [T("all")] + df_cleaned['media_type'].unique().tolist()

        selected_platforms = st.multiselect(T("platform"), platform_options, default=T("all"))
        selected_sentiments = st.multiselect(T("sentiment"), sentiment_options, default=T("all"))
        selected_media_types = st.multiselect(T("media_type"), media_type_options, default=T("all"))

        # Apply filters
        start_date, end_date = date_range
        df_filtered = df_cleaned[
            (df_cleaned['date'].dt.date >= start_date) & 
            (df_cleaned['date'].dt.date <= end_date)
        ]
        
        if T("all") not in selected_platforms:
            df_filtered = df_filtered[df_filtered['platform'].isin(selected_platforms)]
        if T("all") not in selected_sentiments:
            df_filtered = df_filtered[df_filtered['sentiment'].isin(selected_sentiments)]
        if T("all") not in selected_media_types:
            df_filtered = df_filtered[df_filtered['media_type'].isin(selected_media_types)]

# --- Main Page ---
st.title(T("main_title"))
st.markdown(T("main_subtitle"))

if not df_filtered.empty:
    col1, col2 = st.columns(2)

    with col1:
        # Sentiment Chart
        st.subheader(T("chart_title_sentiment"))
        sentiment_counts = df_filtered['sentiment'].value_counts()
        fig = px.pie(
            names=sentiment_counts.index, 
            values=sentiment_counts.values, 
            hole=.4, 
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment Insights
        with st.expander(T("insights_title")):
            total_sentiments = sentiment_counts.sum()
            dominant_sentiment = sentiment_counts.index[0]
            st.markdown(T("dominant_sentiment").format(dominant_sentiment, f"{(sentiment_counts.iloc[0] / total_sentiments * 100):.1f}"))
            
            neg_by_date = df_filtered[df_filtered['sentiment'] == 'Negative'].groupby(df_filtered['date'].dt.date).size().idxmax()
            st.markdown(T("sentiment_anomaly").format("Negative", neg_by_date))
            
            pos_count = sentiment_counts.get('Positive', 0)
            neg_count = sentiment_counts.get('Negative', 0)
            ratio = f"{(pos_count / neg_count):.2f}:1" if neg_count > 0 else "N/A"
            st.markdown(T("sentiment_ratio").format(ratio))

    with col2:
        # Platform Engagements Chart
        st.subheader(T("chart_title_platform"))
        platform_engagements = df_filtered.groupby('platform')['engagements'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=platform_engagements.index, 
            y=platform_engagements.values, 
            color_discrete_sequence=['#8b5cf6']
        )
        st.plotly_chart(fig, use_container_width=True)

        # Platform Insights
        with st.expander(T("insights_title")):
            total_engagements = platform_engagements.sum()
            st.markdown(T("platform_dominance").format(platform_engagements.index[0], f"{(platform_engagements.iloc[0]/total_engagements*100):.1f}"))
            
            post_counts = df_filtered.groupby('platform').size()
            efficiency = (platform_engagements / post_counts).sort_values(ascending=False)
            if len(efficiency) > 1 and efficiency.index[0] != platform_engagements.index[0]:
                st.markdown(T("platform_efficiency").format(efficiency.index[0]))
            
            if len(platform_engagements) > 1:
                st.markdown(T("underperforming_platform").format(platform_engagements.index[-1]))


    col3, col4 = st.columns(2)
    
    with col3:
        # Engagement Trend Chart
        st.subheader(T("chart_title_engagement_trend"))
        engagement_by_date = df_filtered.groupby(df_filtered['date'].dt.date)['engagements'].sum()
        fig = px.line(
            x=engagement_by_date.index, 
            y=engagement_by_date.values, 
            markers=True,
            color_discrete_sequence=['#3b82f6']
        )
        fig.update_layout(xaxis_title=T("axis_date"), yaxis_title=T("axis_total_engagements"))
        st.plotly_chart(fig, use_container_width=True)

        # Engagement Insights
        with st.expander(T("insights_title")):
            st.markdown(T("engagement_spike").format(engagement_by_date.idxmax(), f"{engagement_by_date.max():,}"))
            st.markdown(T("lowest_engagement").format(engagement_by_date.idxmin()))
            trend = "growth" if engagement_by_date.iloc[-1] > engagement_by_date.iloc[0] else "decline"
            trend_verb = "improving" if trend == "growth" else "declining"
            st.markdown(T("steady_growth").format(trend, trend_verb))

    with col4:
        # Media Type Mix Chart
        st.subheader(T("chart_title_media_type"))
        media_type_counts = df_filtered['media_type'].value_counts()
        fig = px.pie(
            names=media_type_counts.index, 
            values=media_type_counts.values, 
            hole=.4, 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)

        # Media Type Insights
        with st.expander(T("insights_title")):
            most_produced = media_type_counts.index[0]
            media_engagements = df_filtered.groupby('media_type')['engagements'].sum().sort_values(ascending=False)
            most_engaging = media_engagements.index[0]

            if most_produced == most_engaging:
                st.markdown(T("media_engagement_match").format(most_produced))
            else:
                st.markdown(T("media_engagement_mismatch").format(most_produced, most_engaging))
            
            st.markdown(T("least_engaging_media").format(media_engagements.index[-1]))


    # Location Chart (Full Width)
    st.subheader(T("chart_title_location"))
    location_engagements = df_filtered.groupby('location')['engagements'].sum().nlargest(5).sort_values(ascending=False)
    fig = px.bar(
        x=location_engagements.index, 
        y=location_engagements.values,
        color_discrete_sequence=['#14b8a6']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Location Insights
    with st.expander(T("insights_title")):
        total_location_eng = location_engagements.sum()
        st.markdown(T("location_concentration").format(location_engagements.index[0], f"{(location_engagements.iloc[0] / total_location_eng * 100):.1f}"))
        if len(location_engagements) > 1:
            st.markdown(T("emerging_market").format(location_engagements.index[1]))
        st.markdown(T("geographic_reach").format(len(df_filtered['location'].unique())))
    
    # --- AI Analysis Section ---
    st.markdown("---")
    st.header(T("summary_title"))

    # AI Buttons
    ai_col1, ai_col2 = st.columns(2)
    with ai_col1:
        if st.button(T("generate_gemini_btn")):
            summary_data = get_summary_data(df_filtered)
            st.subheader(T("gemini_summary_title"))
            with st.spinner(f"{T('generating')}..."):
                st.markdown(f"**{T('summary_perf_title')}**")
                st.success(f"Top Platform: {summary_data['top_platform']}, Dominant Sentiment: {summary_data['dominant_sentiment']}, Top Media: {summary_data['top_media_type']}, Top Location: {summary_data['top_location']}")
                st.markdown(f"**{T('summary_reco_title')}**")
                st.info(f"Focus on {summary_data['top_platform']} and create more {summary_data['top_media_type']} content. Target campaigns in {summary_data['top_location']}.")

    with ai_col2:
        with st.expander(T("openrouter_settings_title")):
            api_key = st.text_input(T("openrouter_api_key_label"), type="password", key="api_key")
            model = st.selectbox(T("openrouter_model_label"), [
                "openai/gpt-3.5-turbo",
                "anthropic/claude-3-haiku-20240307",
                "google/gemini-pro",
                "mistralai/mistral-7b-instruct",
                "meta-llama/llama-3-8b-instruct"
            ])
        if st.button(T("generate_openrouter_btn")):
            if not api_key:
                st.error(T("api_key_error"))
            else:
                summary_data = get_summary_data(df_filtered)
                prompt = f"""
                Analyze this social media data summary and provide a concise summary and 3 strategic recommendations.
                Data:
                - Top Platform: {summary_data['top_platform']}
                - Dominant Sentiment: {summary_data['dominant_sentiment']} ({summary_data['sentiment_distribution']})
                - Top Media Type by Engagement: {summary_data['top_media_type']}
                - Top Location by Engagement: {summary_data['top_location']}
                """
                
                with st.spinner(f"{T('generating')}..."):
                    try:
                        response = requests.post(
                            url="https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {api_key}",
                            },
                            data=json.dumps({
                                "model": model,
                                "messages": [{"role": "user", "content": prompt}]
                            })
                        )
                        response.raise_for_status()
                        result = response.json()
                        st.subheader(T("openrouter_summary_title").format(model))
                        st.markdown(result['choices'][0]['message']['content'])
                    except requests.exceptions.RequestException as e:
                        st.error(f"API Request Failed: {e}")

else:
    st.info("Awaiting CSV file upload.")

