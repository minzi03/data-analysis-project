import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Upload files for user input
st.title("Email Campaign Data Analysis")

# File upload widget for the CSV files
holidays_file = st.file_uploader("Upload holidays.csv", type="csv")
campaigns_file = st.file_uploader("Upload campaigns.csv", type="csv")
messages_file = st.file_uploader("Upload messages-demo.csv", type="csv")

if holidays_file and campaigns_file and messages_file:
    # Step 2: Load the data from the uploaded files
    holidays_df = pd.read_csv(holidays_file)
    holidays_df['date'] = pd.to_datetime(holidays_df['date'], errors='coerce')

    campaigns_df = pd.read_csv(campaigns_file)
    campaigns_df['id'] = campaigns_df['id'].astype('int64')
    campaigns_df['campaign_type'] = campaigns_df['campaign_type'].astype('category')
    campaigns_df['channel'] = campaigns_df['channel'].astype('category')
    campaigns_df['topic'] = campaigns_df['topic'].astype('category')
    campaigns_df['started_at'] = pd.to_datetime(campaigns_df['started_at'], errors='coerce')
    campaigns_df['finished_at'] = pd.to_datetime(campaigns_df['finished_at'], errors='coerce')
    campaigns_df['total_count'] = campaigns_df['total_count'].astype('Int64')
    campaigns_df['ab_test'] = campaigns_df['ab_test'].astype('bool')
    campaigns_df['warmup_mode'] = campaigns_df['warmup_mode'].astype('bool')
    campaigns_df['hour_limit'] = campaigns_df['hour_limit'].astype('Int64')
    campaigns_df['subject_length'] = campaigns_df['subject_length'].astype('Int64')
    campaigns_df['subject_with_personalization'] = campaigns_df['subject_with_personalization'].astype('bool')
    campaigns_df['subject_with_deadline'] = campaigns_df['subject_with_deadline'].astype('bool')
    campaigns_df['subject_with_emoji'] = campaigns_df['subject_with_emoji'].astype('bool')
    campaigns_df['subject_with_bonuses'] = campaigns_df['subject_with_bonuses'].astype('bool')
    campaigns_df['subject_with_discount'] = campaigns_df['subject_with_discount'].astype('bool')
    campaigns_df['subject_with_saleout'] = campaigns_df['subject_with_saleout'].astype('bool')
    campaigns_df['is_test'] = campaigns_df['is_test'].astype('bool')
    campaigns_df['position'] = campaigns_df['position'].astype('Int64')
    campaigns_df = campaigns_df.drop(['warmup_mode', 'hour_limit','is_test','ab_test','position'], axis=1, errors='ignore')

    messages_df = pd.read_csv(messages_file, index_col='message_id', low_memory=False)
    messages_df.drop(labels=['id', 'created_at', 'updated_at', 'category'], inplace=True, axis=1)
    
    # Process Boolean columns
    def convert_to_bool(value):
        if value == 't':
            return True
        else:
            return False

    messages_df['is_opened'] = messages_df['is_opened'].apply(convert_to_bool)
    messages_df['is_clicked'] = messages_df['is_clicked'].apply(convert_to_bool)
    messages_df['is_unsubscribed'] = messages_df['is_unsubscribed'].apply(convert_to_bool)
    messages_df['is_hard_bounced'] = messages_df['is_hard_bounced'].apply(convert_to_bool)
    messages_df['is_soft_bounced'] = messages_df['is_soft_bounced'].apply(convert_to_bool)
    messages_df['is_complained'] = messages_df['is_complained'].apply(convert_to_bool)
    messages_df['is_blocked'] = messages_df['is_blocked'].apply(convert_to_bool)
    messages_df['is_purchased'] = messages_df['is_purchased'].apply(convert_to_bool)

    # Date parsing
    messages_df['date'] = pd.to_datetime(messages_df['date'])
    messages_df['sent_at'] = pd.to_datetime(messages_df['sent_at'])
    messages_df['opened_first_time_at'] = pd.to_datetime(messages_df['opened_first_time_at'])
    messages_df['opened_last_time_at'] = pd.to_datetime(messages_df['opened_last_time_at'])
    messages_df['clicked_first_time_at'] = pd.to_datetime(messages_df['clicked_first_time_at'])
    messages_df['clicked_last_time_at'] = pd.to_datetime(messages_df['clicked_last_time_at'])
    messages_df['unsubscribed_at'] = pd.to_datetime(messages_df['unsubscribed_at'])
    messages_df['hard_bounced_at'] = pd.to_datetime(messages_df['hard_bounced_at'])
    messages_df['soft_bounced_at'] = pd.to_datetime(messages_df['soft_bounced_at'])
    messages_df['complained_at'] = pd.to_datetime(messages_df['complained_at'])
    messages_df['blocked_at'] = pd.to_datetime(messages_df['blocked_at'])
    messages_df['purchased_at'] = pd.to_datetime(messages_df['purchased_at'])

    # Limit to first 500 rows
    messages_df = messages_df.head(500)

    # Step 3: Perform the data processing and user summary calculations as in your original code
    # Assuming `user_summary_df` is already processed according to your logic

    purchase_distribution = user_summary_df['is_purchased_sum'].apply(lambda x: 'Purchased' if x > 0 else 'Not Purchased').value_counts()
    open_distribution = user_summary_df['is_opened_sum'].apply(lambda x: 'Opened' if x > 0 else 'Not Opened').value_counts()
    click_distribution = user_summary_df['is_clicked_sum'].apply(lambda x: 'Clicked' if x > 0 else 'Not Clicked').value_counts()

    # Step 4: Create a figure with 3 pie charts
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))  

    # Pie chart for email open distribution
    axs[0].pie(open_distribution.values, labels=open_distribution.index, autopct='%1.01f%%', startangle=0, colors=['lightblue', 'lightgray'])
    axs[0].set_title('Proportion of Users Who Opened Emails', fontsize=14)
    axs[0].axis('equal')

    # Pie chart for email click distribution
    axs[1].pie(click_distribution.values, labels=click_distribution.index, autopct='%1.01f%%', startangle=0, colors=['orange', 'lightyellow'])
    axs[1].set_title('Proportion of Users Who Clicked', fontsize=14)
    axs[1].axis('equal')

    # Pie chart for purchase distribution
    axs[2].pie(purchase_distribution.values, labels=purchase_distribution.index, autopct='%1.01f%%', startangle=0, colors=['lightgreen', 'lightcoral'])
    axs[2].set_title('Proportion of Users Who Purchased', fontsize=14)
    axs[2].axis('equal')

    # Adjust layout to avoid overlap
    plt.tight_layout()

    # Step 5: Display the plot in Streamlit
    st.pyplot(fig)

else:
    st.warning("Please upload all required CSV files (holidays.csv, campaigns.csv, messages-demo.csv) to proceed.")
