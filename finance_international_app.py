
import streamlit as st
import pandas as pd
import os

# Hardcoded topics from the syllabus
topics = [
    "Module 1: Multinational Financial Management Opportunities and Challenges",
    "Module 2: The Foreign Exchange Market",
    "Module 3: Foreign Currency Derivatives and Interest Rate Risk and Swaps",
    "Module 4: Transaction Exposure and Translation Exposure",
    "Module 5: Operating Exposure",
    "Module 6: Global Cost and Availability of Capital",
    "Module 7: International Tax Management",
    "Module 8: Foreign Direct Investment and Political Risk"
]

DATA_FILE = "fin420_group_responses.csv"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Group Name", "Topic", "Group Response", "Values Reflection"])
    df_init.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

page = st.sidebar.radio("Navigate", ["Submit Response", "View Responses", "Reset App"])

if page == "Submit Response":
    st.title("International Finance - Group Activity")
    st.write("Select a topic from the syllabus and submit your group's analysis and reflection.")

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
