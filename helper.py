from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
import re

# Fetch stats of the chat
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    num_links_shared = len(links)

    return num_messages, len(words), num_media_messages, num_links_shared

#Finding users with most messages
def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user': 'Names', 'count': 'Percentage'})
    return x, new_df

# Generate WordCloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    cloud = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    words = []
    f = open('../stop_hinglish.txt','r')
    stop_words = f.read()
    stop_words = stop_words.split()
    words = []
    new_df = df[df['user'] != "group_notification"]
    for message in new_df['message']:
        for msg in remove_emoji(message).lower().split():
            if "<Media omitted>" not in message and "This message was deleted" not in message:
                if msg not in stop_words:
                    words.append(msg)
    
    wordcloud = cloud.generate(" ".join(words))

    return wordcloud

# Remove Emojis
def remove_emoji(text):
    emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002700-\U000027BF"  # Dingbats
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A (🫠 etc.)
            u"\U00002600-\U000026FF"  # Miscellaneous Symbols
            u"\U000025A0-\U000025FF"  # Geometric Shapes
            u"\U00002300-\U000023FF"  # Miscellaneous Technical
            u"\U0001F1F2-\U0001F1F4"  # Flags
            u"\U0001F191-\U0001F251"  # Enclosed characters
            u"\U0001F004"             # Mahjong Tile Red Dragon
            u"\U0001F0CF"             # Playing Card Black Joker
            u"\u200d"                 # Zero Width Joiner
            u"\u2640-\u2642"          # Gender symbols
            u"\u2600-\u2B55"          # Misc symbols and arrows
            u"\u23cf"                 # Eject symbol
            u"\u23e9"                 # Black right-pointing double triangle
            u"\u231a"                 # Watch
            u"\ufe0f"                 # Variation selector
            u"\u3030"                 # Wavy dash
            "]+", flags=re.UNICODE)
        
    return emoji_pattern.sub(r'', text)

# Top 20 words
def top_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('../stop_hinglish.txt','r')
    stop_words = f.read()
    stop_words = stop_words.split()
    words = []
    new_df = df[df['user'] != "group_notification"]
    for message in new_df['message']:
        for msg in remove_emoji(message).lower().split():
            if "<Media omitted>" not in message and "This message was deleted" not in message:
                if msg not in stop_words:
                    words.append(msg)
    
    return words

# Working with Emoji
def fetch_emoji(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    import emoji
    emojis = []

    for message in df['message']:
        emojis.extend([e for e in message if e in emoji.EMOJI_DATA])
    
    return emojis

# Monthly Timeline
def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline

# Dailt Timeline
def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    day_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return day_timeline

# Analysis by day
def day_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    day_df = df['day_name'].value_counts()
    return day_df

# Analysis by month
def monthly_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    month_df = df['month'].value_counts()
    return month_df

# Heatmap of time-period
def time_period_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    time_period = df.pivot_table(index='day', columns='time_period', values='message', aggfunc='count').fillna(0)
    time_period = time_period[sorted(time_period.columns, key=lambda x: int(x.split("-")[0]))].sort_values(by='day', ascending=False)

    return time_period