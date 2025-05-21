import streamlit as st
import pandas as pd
from io import BytesIO
import re
from datetime import datetime
import matplotlib.pyplot as plt
import os
import json

# --- Voting Time Settings ---
VOTING_START = datetime(2025, 5, 20, 9, 0, 0)  # 9:00 AM
VOTING_END = datetime(2025, 5, 23, 12, 0, 0)   # 12:00 PM

# --- Helper Functions ---
def clean_spaces(value):
    if isinstance(value, str):
        return re.sub(r'\s+', ' ', value.strip())
    return value

def load_voter_data():
    try:
        df = pd.read_csv("votersdetails.csv")
        df = df.applymap(clean_spaces)
        df['Mat Number'] = df['Mat Number'].astype(str)
        return df
    except:
        st.error("Error loading voter data. Please ensure 'votersdetails.csv' exists.")
        return pd.DataFrame({"Mat Number": [], "Password": []})

def has_already_voted(mat_number):
    return str(mat_number) in st.session_state.voted

def load_saved_results():
    """Load previously saved election results if they exist"""
    if os.path.exists('election_results.json'):
        with open('election_results.json', 'r') as f:
            data = json.load(f)
            st.session_state.votes = data['votes']
            st.session_state.voted = set(data['voted'])
            st.success("Previously saved results loaded successfully.")

def save_results():
    """Save current election results to file"""
    data = {
        'votes': st.session_state.votes,
        'voted': list(st.session_state.voted),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('election_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Also save as CSV for easy analysis
    results_df = pd.DataFrame(st.session_state.votes).T
    results_df.to_csv('election_results.csv')
    
    # Save list of voters who have voted
    voted_df = pd.DataFrame({'Matriculation Number': list(st.session_state.voted)})
    voted_df.to_csv('voted_students.csv', index=False)
    
    return results_df

def export_excel():
    """Export results to Excel file"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Results sheet
        results_df = pd.DataFrame(st.session_state.votes).T
        results_df.to_excel(writer, sheet_name='Results')
        
        # Participation sheet
        voted_df = pd.DataFrame({'Matriculation Number': list(st.session_state.voted), 'Status': 'Voted'})
        voted_df.to_excel(writer, sheet_name='Voted Students', index=False)
        
        # Summary sheet
        total_voters = len(st.session_state.voter_df)
        voted_count = len(st.session_state.voted)
        participation = (voted_count / total_voters * 100) if total_voters else 0
        
        summary_data = {
            'Metric': ['Total Eligible Voters', 'Total Votes Cast', 'Participation Rate'],
            'Value': [total_voters, voted_count, f"{participation:.1f}%"]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
    return output.getvalue()

def display_results():
    """Display election results with charts"""
    # Show participation statistics
    total_voters = len(st.session_state.voter_df)
    voted_count = len(st.session_state.voted)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Eligible Voters", total_voters)
    col2.metric("Total Votes Cast", f"{voted_count} ({(voted_count / total_voters * 100) if total_voters else 0:.1f}%)")
    
    # Create visualizations for each position
    for position, candidates in st.session_state.votes.items():
        st.subheader(f"{position}")
        total = sum(candidates.values())
        
        if total == 0:
            st.info(f"No votes recorded for {position}")
            continue
            
        # Create bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        names = list(candidates.keys())
        values = list(candidates.values())
        percentages = [(v / total * 100) if total else 0 for v in values]
        
        bars = ax.bar(names, values, color=colors[:len(names)])
        
        # Add labels
        for i, (bar, value, percent) in enumerate(zip(bars, values, percentages)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
                   f"{value} ({percent:.1f}%)", 
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_ylabel('Votes')
        ax.set_title(f'{position} Results')
        plt.xticks(rotation=15, ha='right', fontsize=9)
        plt.tight_layout()
        
        st.pyplot(fig)
        plt.close(fig)  # Close to free memory

# --- Initialize Session State ---
if 'voter_df' not in st.session_state:
    st.session_state.voter_df = load_voter_data()
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'voted' not in st.session_state:
    st.session_state.voted = set()
if 'votes' not in st.session_state:
    st.session_state.votes = {
        'President': {'Prince John ANIGBO': 0, 'Covenant Olamigoke OLOWO': 0},
        'Vice President': {'Esther OGUNLEYE': 0, 'Hafsoh K. OGUNNIYI': 0},
        'General Secretary': {'Churchill OLISA': 0},
        'Assist. General Secretary': {'Frankcleave KASIMANWUNA': 0, 'Ajiserere ODUFISAN': 0, 'George IHEKWABA': 0},
        'Financial Secretary': {'F\'eyisayo OLATUNJI': 0},
        'Treasurer': {'Okikiimole AKINDUSOYE': 0, 'Pipolooluwa AYO-PONLE': 0},
        'PRO': {'Jocl ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
        'Sports Secretary': {'Nasirudeen Adeshina ALABI': 0, 'Ireoluwa OKE': 0},
        'Welfare Secretary': {'Oluwadunmininu IDOWU': 0, 'Simbiat O. ADUMADEYIN': 0, 'Olamiposi latcefat RAJI': 0},
        'Social Secretary': {'Oluwagbotemi Fatiu ADEBAYO': 0, 'Vivian AGWOILE': 0}
    }
if 'show_results' not in st.session_state:
    st.session_state.show_results = True
if 'admin_sidebar_visible' not in st.session_state:
    st.session_state.admin_sidebar_visible = False
# Removed sidebar_password_attempt as it's no longer needed

# --- App UI ---
st.title("BellsTech's Student Voting System")

# --- Admin Sidebar Access ---
# Only display sidebar if admin is authenticated
if st.session_state.get('is_admin', False):
    admin_sidebar = st.sidebar.container()
    
    # Toggle sidebar visibility for admin
    if not st.session_state.admin_sidebar_visible:
        if admin_sidebar.button("Show Admin Panel"):
            st.session_state.admin_sidebar_visible = True
            st.rerun()
    else:
        admin_sidebar.title("Results Management")
        
        # Load results button
        if admin_sidebar.button("🔄 Load Saved Results"):
            load_saved_results()

        # Save results option
        if admin_sidebar.button("💾 Save Results Now"):
            results_df = save_results()
            admin_sidebar.success("Results saved successfully to:")
            admin_sidebar.info("- election_results.json\n- election_results.csv\n- voted_students.csv")
            
            # Display a dataframe showing the current results
            admin_sidebar.dataframe(results_df)

        # Excel export button
        if admin_sidebar.button("📊 Export to Excel"):
            excel_data = export_excel()
            admin_sidebar.download_button(
                label="📥 Download Excel File",
                data=excel_data,
                file_name=f"election_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # Hide sidebar button
        if admin_sidebar.button("Hide Admin Panel"):
            st.session_state.admin_sidebar_visible = False
            st.rerun()

# --- Voting Time Check ---
now = datetime.now()
if now < VOTING_START:
    time_left = VOTING_START - now
    st.warning(f"🕒 Voting has not started yet. It begins in {str(time_left).split('.')[0]}")
elif now > VOTING_END:
    st.info("🏁 Voting period has ended.")
else:
    time_left = VOTING_END - now
    st.info(f"⏳ Time remaining: {str(time_left).split('.')[0]}")

# --- Tabs for navigation ---
tab1, tab2 = st.tabs(["Voting", "Results"])

with tab1:
    # Authentication section
    if not st.session_state.authenticated:
        st.header("Voter Authentication")
        mat_number = st.text_input("Matriculation Number:").strip()
        password = st.text_input("Password:", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                if not mat_number or not password:
                    st.error("Please enter both Matriculation Number and Password")
                else:
                    # Check if matriculation number exists
                    mat_exists = (st.session_state.voter_df['Mat Number'] == mat_number).any()
                    
                    if not mat_exists:
                        st.error("Invalid Matriculation Number")
                    else:
                        # Verify password
                        user_record = st.session_state.voter_df[st.session_state.voter_df['Mat Number'] == mat_number].iloc[0]
                        if user_record['Password'] != password:
                            st.error("Incorrect Password")
                        elif has_already_voted(mat_number):
                            st.error("You have already voted")
                        else:
                            st.session_state.authenticated = True
                            st.session_state.current_user = mat_number
                            st.rerun()
        
        with col2:
            if st.button("Admin Login"):
                admin_pass = st.text_input("Admin Password:", type="password")
                if admin_pass == "X9@2&!p":
                    st.session_state.authenticated = True
                    st.session_state.is_admin = True
                    st.session_state.admin_sidebar_visible = True
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")
    
    # Voting section
    else:
        user = st.session_state.get('current_user', '')
        
        if st.session_state.get('is_admin', False):
            st.success("Logged in as Administrator")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.is_admin = False
                st.session_state.admin_sidebar_visible = False
                st.rerun()
        
        elif has_already_voted(user):
            st.success("✅ You have already voted. Thank you!")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
        
        elif VOTING_START <= now <= VOTING_END:
            st.header("Cast Your Vote")
            
            # Voting form with no default values
            pres = st.radio("President:", ['Prince John ANIGBO', 'Covenant Olamigoke OLOWO'], index=None)
            vp = st.radio("Vice President:", ['Esther OGUNLEYE', 'Hafsoh K. OGUNNIYI'], index=None)
            gs = st.radio("General Secretary:", ['Churchill OLISA'], index=None)
            ags = st.radio("Assistant General Secretary:", ['Frankcleave KASIMANWUNA', 'Ajiserere ODUFISAN', 'George IHEKWABA'], index=None)
            fs = st.radio("Financial Secretary:", ['F\'eyisayo OLATUNJI'], index=None)
            tre = st.radio("Treasurer:", ['Okikiimole AKINDUSOYE', 'Pipolooluwa AYO-PONLE'], index=None)
            pro = st.radio("PRO:", ['Jocl ATUH', 'Steaadfast ILEOGBEN', 'Victor Folahanmi AKILO', 'Enoch OGUNTOYE'], index=None)
            sport = st.radio("Sports Secretary:", ['Nasirudeen Adeshina ALABI', 'Ireoluwa OKE'], index=None)
            welfare = st.radio("Welfare Secretary:", ['Oluwadunmininu IDOWU', 'Simbiat O. ADUMADEYIN', 'Olamiposi latcefat RAJI'], index=None)
            social = st.radio("Social Secretary:", ['Oluwagbotemi Fatiu ADEBAYO', 'Vivian AGWOILE'], index=None)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Vote"):
                    # Check if all positions have been voted for
                    if None in [pres, vp, gs, ags, fs, tre, pro, sport, welfare, social]:
                        st.error("Please vote for all positions before submitting")
                    else:
                        # Update votes for all positions
                        st.session_state.votes['President'][pres] += 1
                        st.session_state.votes['Vice President'][vp] += 1
                        st.session_state.votes['General Secretary'][gs] += 1
                        st.session_state.votes['Assist. General Secretary'][ags] += 1
                        st.session_state.votes['Financial Secretary'][fs] += 1
                        st.session_state.votes['Treasurer'][tre] += 1
                        st.session_state.votes['PRO'][pro] += 1
                        st.session_state.votes['Sports Secretary'][sport] += 1
                        st.session_state.votes['Welfare Secretary'][welfare] += 1
                        st.session_state.votes['Social Secretary'][social] += 1
                        
                        # Mark as voted
                        st.session_state.voted.add(user)
                        
                        # Auto-save results after each vote
                        save_results()
                        
                        st.success("✅ Vote submitted successfully!")
                        st.rerun()

            with col2:
                if st.button("Logout"):
                    st.session_state.authenticated = False
                    st.rerun()
        else:
            st.warning("Voting is currently closed.")

with tab2:
    st.header("Election Results")
    
    # Admin controls for results visibility
    if st.session_state.get('is_admin', False):
        st.session_state.show_results = st.checkbox("Show results to everyone", value=st.session_state.show_results)
    
    # Check conditions for displaying results
    user = st.session_state.get('current_user', '')
    show_condition = (
        now > VOTING_END or 
        st.session_state.get('is_admin', False) or
        (user in st.session_state.voted and st.session_state.show_results)
    )
    
    if show_condition:
        display_results()
    else:
        st.warning("Results are only available after voting or to administrators.")