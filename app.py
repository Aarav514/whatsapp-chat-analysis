import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.title("Welcome to WhatsApp Chat Analyzer 👋")
st.markdown("Upload a WhatsApp chat `.txt` file using the left sidebar to begin analysis.")



st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is None:
    st.warning("📄 Please upload a chat file from the left sidebar to get started.")

if uploaded_file is not None:
    bytes = uploaded_file.getvalue()
    data = bytes.decode('utf-8')
    df = preprocess.preprocess(data)




    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt',user_list)
    if st.sidebar.button('Show Analysis'):
        num_messages,total_words,num_media,num_links   = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(total_words)
        with col3:
            st.header('Media shared')
            st.title(num_media)

        with col4:
            st.header('Link Shared')
            st.title(num_links)

        # Monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        daily = helper.daily_timeline(selected_user,df)
        st.title('Daily Timeline')
        fig,ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Days')
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)






        # finding the busiest users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header('Busy Users')
                st.dataframe(new_df)

        df_wc = helper.create_word_cloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)


        return_df = helper.most_common_words(selected_user, df)
        fig,ax = plt.subplots()
        ax.barh(return_df[0],return_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        emoji = helper.emoji_df(selected_user,df)
        st.title('Emoji')
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji['Count'], labels=emoji['Emoji'], autopct='%1.1f%%')
            st.pyplot(fig)

        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)









