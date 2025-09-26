import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set plot style
sns.set(style="whitegrid")

# Load cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv', low_memory=False)
    df = df.dropna(subset=['title', 'publish_time'])
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['journal'] = df['journal'].fillna('Unknown')
    df['source_x'] = df['source_x'].fillna('Unknown')
    df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
year_range = st.sidebar.slider("Select publication year range", 2019, 2023, (2020, 2021))
selected_journal = st.sidebar.selectbox("Select journal", ["All"] + sorted(df['journal'].unique()))
selected_source = st.sidebar.selectbox("Select source", ["All"] + sorted(df['source_x'].unique()))

# Apply filters
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
if selected_journal != "All":
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]
if selected_source != "All":
    filtered_df = filtered_df[filtered_df['source_x'] == selected_source]

# Title and description
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research metadata with interactive filters and visualizations.")

# Show sample data
st.subheader("Sample of Filtered Data")
st.dataframe(filtered_df[['title', 'journal', 'year', 'source_x']].head(10))

# Publications by Year
st.subheader("Publications by Year")
year_counts = filtered_df['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_title('Publications by Year')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Papers')
st.pyplot(fig1)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax2, palette='viridis')
ax2.set_title('Top Journals Publishing COVID-19 Research')
ax2.set_xlabel('Number of Papers')
st.pyplot(fig2)

# Word Cloud of Titles
st.subheader("Word Cloud of Paper Titles")
title_text = ' '.join(filtered_df['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(title_text)
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

# Source Distribution
st.subheader("Top Sources of Papers")
source_counts = filtered_df['source_x'].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=source_counts.values, y=source_counts.index, ax=ax4, palette='mako')
ax4.set_title('Top Sources of Papers')
ax4.set_xlabel('Number of Papers')
st.pyplot(fig4)
