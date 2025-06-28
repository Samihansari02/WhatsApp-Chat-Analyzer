import streamlit as st
import preprocessor, helper
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from helper import daily_timeline

st.sidebar.title('Whatsapp Chat Analyzer')
st.sidebar.image(
    'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg',
    caption='WhatsApp Chat Analyzer',
    use_container_width=True
)




uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button('Show Analysis'):

        st.markdown("""
        <style>
        [data-testid="stMetricLabel"] p {
            font-size: 25px !important;
            font-weight: bold !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.title('Top Statistics')

        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Messages", value=num_messages)
        with col2:
            st.metric(label="Total Words", value=words)
        with col3:
            st.metric(label="Media Shared", value=num_media_messages)
        with col4:
            st.metric(label="Links Shared", value=links)



        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='purple')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='brown')
        plt.xticks(rotation=90)
        st.pyplot(fig)



        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.write('## Most Busy Day')
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.write("## Most Busy Months")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)


        # activity heatmap
        st.title('Activity Heatmap')
        pvt = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        sns.heatmap(pvt)
        st.pyplot(fig)


        # finding the busiest users in the group
        if selected_user =='Overall':
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            x.columns = ['User', 'Message Count']
            fig, ax = plt.subplots()

            col5, col6 = st.columns(2)
            with col5:
                ax.bar(x['User'], x['Message Count'])
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col6:
                st.dataframe(new_df)


        # WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words

        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation=90)
        st.title('Most Common Words')
        st.pyplot(fig)



        # emoji analysis
        st.title('Emoji Analysis')
        emoji_df = helper.extract_emoji(selected_user,df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


