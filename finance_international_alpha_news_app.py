
import streamlit as st
import pandas as pd
import requests
import os

# Alpha Vantage API setup
API_URL = "https://www.alphavantage.co/query"
API_KEY = "A2P16LEIUBU7WZKf"  # Replace with your actual Alpha Vantage API key

# Topic-specific queries
topic_queries = {
"International Finance"
}

# Function to fetch news sentiment data for a topic
def fetch_alpha_news(query):
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": API_KEY,
        "topics": query
    }
    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            return response.json().get("feed", [])
        else:
            return []
    except:
        return []

DATA_FILE = "fin420_group_responses.csv"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Group Name", "Topic", "Group Response", "Values Reflection"])
    df_init.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

page = st.sidebar.radio("Navigate", ["Live News", "Submit Response", "View Responses", "Reset App"])

if page == "Live News":
    st.title("Live International Finance News - Alpha Vantage")
    st.write("Latest headlines tailored to discussion topics:")
    for topic, query in topic_queries.items():
        st.subheader(topic)
        articles = fetch_alpha_news(query)
        if articles:
            for article in articles:
                st.markdown(f"**{article.get('title', 'No Title')}**")
                st.write(article.get("summary", "No Summary"))
                st.markdown(f"[Read more]({article.get('url', '#')})")
                st.markdown("---")
        else:
            st.info("No news available or API key missing.")

elif page == "Submit Response":
    st.title("International Finance - News-Based Group Activity")
    topics = list(topic_queries.keys())
    group_name = st.text_input("Enter your group name:")
    selected_topic = st.selectbox("Choose a topic to analyze:", topics)
    st.subheader("Discussion Prompts")
    st.write("""
    - What are the key financial challenges in this topic?
    - How does this topic relate to international financial management?
    - What risks or ethical issues might be present?
    """)
    group_response = st.text_area("Enter your group's insights and analysis here:")
    reflection = st.text_area("How does responsible stewardship apply to this topic in a global context?")
    if st.button("Submit Responses"):
        new_entry = pd.DataFrame([[group_name, selected_topic, group_response, reflection]],
                                 columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Thank you! Your responses have been saved.")

elif page == "View Responses":
    st.title("Submitted Group Responses")
    if df.empty:
        st.info("No responses submitted yet.")
    else:
        for group in df["Group Name"].unique():
            st.subheader(f"Group: {group}")
            group_data = df[df["Group Name"] == group]
            for _, row in group_data.iterrows():
                st.markdown(f"**Topic:** {row['Topic']}")
                st.markdown(f"**Response:** {row['Group Response']}")
                st.markdown(f"**Reflection:** {row['Values Reflection']}")
                st.markdown("---")

elif page == "Reset App":
    st.title("Reset App")
    if st.button("Delete All Responses"):
        df_empty = pd.DataFrame(columns=df.columns)
        df_empty.to_csv(DATA_FILE, index=False)
        st.success("All responses have been deleted.")
