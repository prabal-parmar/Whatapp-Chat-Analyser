import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyser",
    layout="wide",
    initial_sidebar_state="expanded")

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat txt file")

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    try:
        data = bytes_data.decode("utf-8")
    except UnicodeDecodeError:
        st.header("Upload Whatsapp txt file only")
        st.stop()
    
    
    df = preprocessor.preprocess(data)
    users = df['user'].unique().tolist()
    users.remove('group_notification')
    users = sorted(users, key=str.lower)
    users.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Select particular user",users)
    
    if st.sidebar.button("Show Analysis"):

        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links_shared = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Links Shared")
            st.title(num_links_shared)

        
        # Monthly Timeeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.xticks(rotation='vertical')
        ax.plot(timeline['time'], timeline['message'], color='green')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        day_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.xticks(rotation="vertical")
        ax.plot(day_timeline['only_date'], day_timeline['message'], color='red')
        st.pyplot(fig)

        # most interactive day and month
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Interactive Day")
            day_df = helper.day_analysis(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(day_df.index, day_df.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Interactive Month")
            month_df = helper.monthly_analysis(selected_user, df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(month_df.index, month_df.values)
            st.pyplot(fig)


        # Time Period Analysis
        time_period = helper.time_period_analysis(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(time_period)
        st.pyplot(fig)

        
        # Busy User Data
        if selected_user == "Overall":
            st.title("Most Busy User")
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.write(new_df)


        # Word Cloud
        st.title("Word Cloud")
        wordcloud = helper.create_wordcloud(selected_user, df)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        # Top Used Words
        st.title("Top Words Used")
        top_words = helper.top_words(selected_user, df)
        most_common_df = pd.DataFrame(Counter(top_words).most_common(20))
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Emojis
        st.title("Emojis Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            all_emojis = helper.fetch_emoji(selected_user, df)
            emoji_df = pd.DataFrame(Counter(all_emojis).most_common(len(Counter(all_emojis)))).rename(columns={0:'Emoji', 1: "Number of times used"})
            if not emoji_df.empty:
                st.write(emoji_df)
            else:
                st.write("No emoji used")

        with col2:
            try:
                fig, ax = plt.subplots()
                ax.pie(emoji_df['Number of times used'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
                st.pyplot(fig)
            except:
                pass
