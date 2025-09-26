# 📦 Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 📊 Set plot style
sns.set(style="whitegrid")

# 📁 Load the dataset
df = pd.read_csv('metadata.csv', low_memory=False)

# 🧹 Clean the data
df = df.dropna(subset=['title', 'publish_time'])
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['journal'] = df['journal'].fillna('Unknown')
df['source_x'] = df['source_x'].fillna('Unknown')
df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))

# 📈 Publications by Year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
plt.bar(year_counts.index, year_counts.values, color='skyblue')
plt.title('Publications by Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.tight_layout()
plt.show()

# 🏛️ Top Journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top Journals Publishing COVID-19 Research')
plt.xlabel('Number of Papers')
plt.tight_layout()
plt.show()

# 🧠 Word Cloud of Titles
title_text = ' '.join(df['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(title_text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Frequent Words in Paper Titles')
plt.tight_layout()
plt.show()

# 🗂️ Distribution by Source
source_counts = df['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=source_counts.values, y=source_counts.index, palette='mako')
plt.title('Top Sources of Papers')
plt.xlabel('Number of Papers')
plt.tight_layout()
plt.show()
