import streamlit as st
import pandas as pd
from io import BytesIO
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# --- Voting Time Settings ---
VOTING_START = datetime(2025, 5, 23, 12, 0, 0)  # 12:00 PM
VOTING_END = datetime(2025, 5, 23, 16, 0, 0)    # 4:00 PM

# --- Auto-logout Settings ---
SESSION_TIMEOUT_MINUTES = 5  # Auto-logout after 5 minutes
AUTO_LOGOUT_AFTER_VOTING = True  # Auto-logout after voting

# --- Candidate Information (simplified - no pictures) ---
CANDIDATES_INFO = {
    'President': {
        'Prince John ANIGBO': 'Prince',
        'Covenant Olamigoke OLOWO': 'Olowo'
    },
    'Vice President': {
        'Esther OGUNLEYE': 'Esther',
        'Hafsoh K. OGUNNIYI': 'OGUNNIYI'
    },
    'General Secretary': {
        'Churchill OLISA': 'Winston'
    },
    'Assistant General Secretary': {
        'Frankcleave KASIMANWUNA': 'Frank',
        'Ajiserere ODUFISAN': 'Ajay',
        'George IHEKWABA': 'George'
    },
    'Financial Secretary': {
        'F\'eyisayo OLATUNJI': 'Feyisayo'
    },
    'Treasurer': {
        'Okikiimole AKINDUSOYE': 'Okiki'
    },
    'PRO': {
        'Joel ATUH': 'Joel',
        'Steaadfast ILEOGBEN': 'Steaadfast',
        'Victor Folahanmi AKILO': 'Reme',
        'Enoch OGUNTOYE': 'Toye'
    },
    'Sports Secretary': {
        'Nasirudeen Adeshina ALABI': 'Nas',
        'Ireoluwa OKE': ''
    },
    'Welfare Secretary': {
        'Oluwadunmininu IDOWU': 'Dunmi',
        'Simbiat O. ADUMADEYIN': 'BIBIRE',
        'Olamiposi latcefat RAJI': ''
    },
    'Social Secretary': {
        'Oluwagbotemi Fatiu ADEBAYO': '𝐃𝐉 Gecho',
        'Vivian AGWOILE': 'Vivian'
    }
}

# --- Email Configuration ---
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',
}

# --- Helper Functions ---
@st.cache_data
def clean_spaces(value):
    if isinstance(value, str):
        return re.sub(r'\s+', ' ', value.strip())
    return value

def create_candidate_selection(position, candidates, key_prefix):
    """Create simplified candidate selection without images"""
    st.subheader(f"{position}")
    
    # Create options with aliases
    options = []
    for candidate in candidates:
        alias = CANDIDATES_INFO.get(position, {}).get(candidate, '')
        display_name = candidate
        if alias and alias != candidate:
            display_name += f" ({alias})"
        options.append(display_name)
    
    # Simple radio selection
    selected = st.radio(
        f"Select your choice for {position}:",
        options,
        index=None,
        key=f"{key_prefix}_{position.replace(' ', '_').replace('.', '')}"
    )
    
    # Return the original candidate name (without alias)
    if selected:
        for i, option in enumerate(options):
            if option == selected:
                return candidates[i]
    return None

# --- Session Management Functions ---
def check_session_timeout():
    """Check if user session has timed out"""
    if not st.session_state.authenticated:
        return False
    
    if 'login_time' not in st.session_state:
        return False
    
    current_time = datetime.now()
    time_elapsed = current_time - st.session_state.login_time
    
    if time_elapsed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
        return True
    
    return False

def logout_user(reason=""):
    """Log out the current user and clear session data"""
    st.session_state.authenticated = False
    st.session_state.is_admin = False
    st.session_state.admin_sidebar_visible = False
    st.session_state.current_user = ""
    st.session_state.current_user_record = {}
    st.session_state.show_password_recovery = False
    
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    
    if reason:
        st.warning(f"You have been logged out: {reason}")
    
    st.rerun()

def get_session_time_remaining():
    """Get remaining session time in minutes"""
    if 'login_time' not in st.session_state:
        return 0
    
    elapsed = datetime.now() - st.session_state.login_time
    remaining = timedelta(minutes=SESSION_TIMEOUT_MINUTES) - elapsed
    
    if remaining.total_seconds() <= 0:
        return 0
    
    return int(remaining.total_seconds() / 60)

@st.cache_data
def load_voter_data():
    try:
        df = pd.read_csv("votersdetails.csv")
        df = df.applymap(clean_spaces)
        df['Mat Number'] = df['Mat Number'].astype(str)
        
        required_columns = ['Mat Number', 'Password', 'Email']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in votersdetails.csv: {', '.join(missing_columns)}")
            return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
        return df
    except FileNotFoundError:
        st.error("Error loading voter data. Please ensure 'votersdetails.csv' exists.")
        return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
    except Exception as e:
        st.error(f"Error loading voter data: {str(e)}")
        return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})

def send_password_email(email, password, name="Student"):
    """Send password to user's email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = email
        msg['Subject'] = "BellsTech Voting System - Password Recovery"
        
        body = f"""
Dear {name},

Your login credentials for the BellsTech Student Voting System:

Email: {email}
Password: {password}

Please use these credentials to log in and cast your vote.

Voting Period: {VOTING_START.strftime('%B %d, %Y at %I:%M %p')} - {VOTING_END.strftime('%B %d, %Y at %I:%M %p')}

Best regards,
BellsTech Election Committee
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def has_already_voted(identifier):
    """Check if user has voted using either mat number or email"""
    return str(identifier) in st.session_state.voted

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
    
    # Save as CSV for easy analysis
    results_df = pd.DataFrame(st.session_state.votes).T
    results_df.to_csv('election_results.csv')
    
    # Save list of voters who have voted
    voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted)})
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
        voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted), 'Status': 'Voted'})
        voted_df.to_excel(writer, sheet_name='Voted Students', index=False)
        
        # Summary sheet
        total_voters = len(st.session_state.voter_df)
        voted_count = len(st.session_state.voted) - 1
        participation = (voted_count / total_voters * 100) if total_voters else 0
        
        summary_data = {
            'Metric': ['Total Eligible Voters', 'Total Votes Cast', 'Participation Rate'],
            'Value': [total_voters, voted_count, f"{participation:.1f}%"]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
    return output.getvalue()

def display_results():
    """Display election results with simple charts"""
    total_voters = len(st.session_state.voter_df)
    voted_count = len(st.session_state.voted)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Eligible Voters", total_voters)
    
    # Create simple visualizations for each position
    for position, candidates in st.session_state.votes.items():
        st.subheader(f"{position}")
        total = sum(candidates.values())
        
        if total == 0:
            st.info(f"No votes recorded for {position}")
            continue
        
        # Simple bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        # Use aliases in chart display
        names = []
        for candidate in candidates.keys():
            alias = CANDIDATES_INFO.get(position, {}).get(candidate, '')
            display_name = candidate
            if alias and alias != candidate:
                display_name = f"{candidate}\n({alias})"
            names.append(display_name)
        
        values = list(candidates.values())
        percentages = [(v / total * 100) if total else 0 for v in values]
        
        bars = ax.bar(names, values, color=colors[:len(names)])
        
        # Add labels
        for bar, value, percent in zip(bars, values, percentages):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   f"{value}\n({percent:.1f}%)", 
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_ylabel('Votes')
        ax.set_title(f'{position} Results')
        plt.xticks(rotation=15, ha='right', fontsize=8)
        plt.tight_layout()
        
        st.pyplot(fig)
        plt.close(fig)

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    if st.session_state.voter_df.empty:
        return False, "No voter data available"
    
    email_exists = (st.session_state.voter_df['Email'].str.lower() == email.lower()).any()
    
    if not email_exists:
        return False, "Email not found in voter database"
    
    user_record = st.session_state.voter_df[st.session_state.voter_df['Email'].str.lower() == email.lower()].iloc[0]
    
    if user_record['Password'].lower() != password.lower():
        return False, "Incorrect password"
    
    if has_already_voted(email) or has_already_voted(user_record['Mat Number']):
        return False, "You have already voted"
    
    return True, user_record

def voting_section():
    """Voting section content"""
    if not st.session_state.authenticated:
        st.header("Voter Authentication")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Forgot Password?"):
                st.session_state.show_password_recovery = not st.session_state.show_password_recovery
                st.rerun()
        
        if st.session_state.show_password_recovery:
            # Password Recovery Section
            st.subheader("Password Recovery")
            st.info("Enter your email address to receive your password")
            
            recovery_email = st.text_input("Email Address:", key="recovery_email").strip().lower()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Send Password"):
                    if not recovery_email:
                        st.error("Please enter your email address")
                    else:
                        if st.session_state.voter_df.empty:
                            st.error("Voter database not available")
                        else:
                            user_match = st.session_state.voter_df[
                                st.session_state.voter_df['Email'].str.lower() == recovery_email
                            ]
                            
                            if user_match.empty:
                                st.error("Email not found in voter database")
                            else:
                                user_record = user_match.iloc[0]
                                name = user_record.get('Full Name', 'Student')
                                password = user_record['Password']
                                
                                if send_password_email(recovery_email, password, name):
                                    st.success("Password sent to your email address!")
                                else:
                                    st.error("Failed to send email. Please contact the administrator.")
                                    st.warning(f"Your password is: **{password}**")
            
            with col2:
                if st.button("Back to Login"):
                    st.session_state.show_password_recovery = False
                    st.rerun()
        
        else:
            # Login Section
            st.subheader("Login with Email")
            email = st.text_input("Email Address:").strip().lower()
            password = st.text_input("Password:", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login"):
                    if not email or not password:
                        st.error("Please enter both email and password")
                    else:
                        success, result = authenticate_user(email, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.current_user = email
                            st.session_state.current_user_record = result
                            st.session_state.login_time = datetime.now()
                            st.success(f"Welcome, {result.get('Full Name', 'Student')}!")
                            st.rerun()
                        else:
                            st.error(result)
            
            with col2:
                if st.button("Admin Login"):
                    admin_pass = st.text_input("Admin Password:", type="password", key="admin_pass")
                    if admin_pass == "X9@2&!p":
                        st.session_state.authenticated = True
                        st.session_state.is_admin = True
                        st.session_state.admin_sidebar_visible = True
                        st.session_state.login_time = datetime.now()
                        st.rerun()
                    elif admin_pass:
                        st.error("Invalid admin credentials")
    
    else:
        user = st.session_state.get('current_user', '')
        
        if st.session_state.get('is_admin', False):
            st.success("Logged in as Administrator")
            if st.button("Logout"):
                logout_user()
        
        elif has_already_voted(user):
            st.success("✅ You have already voted. Thank you!")
            
            if AUTO_LOGOUT_AFTER_VOTING:
                st.info("You will be automatically logged out in 3 seconds...")
                st.rerun()
            else:
                if st.button("Logout"):
                    logout_user()
        
        elif VOTING_START <= datetime.now() <= VOTING_END:
            st.header("Cast Your Vote")
            
            user_record = st.session_state.get('current_user_record', {})
            if user_record is not None and not user_record.empty:
                st.info(f"Voting as: {user_record.get('Full Name', 'Student')} ({user_record.get('Mat Number', 'N/A')})")
            
            # Simplified voting form
            pres = create_candidate_selection("President", 
                ['Prince John ANIGBO', 'Covenant Olamigoke OLOWO'], "vote")
            
            vp = create_candidate_selection("Vice President", 
                ['Esther OGUNLEYE', 'Hafsoh K. OGUNNIYI'], "vote")
            
            gs = create_candidate_selection("General Secretary", 
                ['Churchill OLISA'], "vote")
            
            ags = create_candidate_selection("Assistant General Secretary", 
                ['Frankcleave KASIMANWUNA', 'Ajiserere ODUFISAN', 'George IHEKWABA'], "vote")
            
            fs = create_candidate_selection("Financial Secretary", 
                ['F\'eyisayo OLATUNJI'], "vote")
            
            tre = create_candidate_selection("Treasurer", 
                ['Okikiimole AKINDUSOYE'], "vote")
            
            pro = create_candidate_selection("PRO", 
                ['Joel ATUH', 'Steaadfast ILEOGBEN', 'Victor Folahanmi AKILO', 'Enoch OGUNTOYE'], "vote")
            
            sport = create_candidate_selection("Sports Secretary", 
                ['Nasirudeen Adeshina ALABI', 'Ireoluwa OKE'], "vote")
            
            welfare = create_candidate_selection("Welfare Secretary", 
                ['Oluwadunmininu IDOWU', 'Simbiat O. ADUMADEYIN', 'Olamiposi latcefat RAJI'], "vote")
            
            social = create_candidate_selection("Social Secretary", 
                ['Oluwagbotemi Fatiu ADEBAYO', 'Vivian AGWOILE'], "vote")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Vote", type="primary"):
                    if None in [pres, vp, gs, ags, fs, tre, pro, sport, welfare, social]:
                        st.error("Please vote for all positions before submitting")
                    else:
                        # Update votes
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
                        user_record = st.session_state.get('current_user_record', {})
                        if user_record is not None and not user_record.empty:
                            st.session_state.voted.add(user_record.get('Mat Number', ''))
                        
                        save_results()
                        st.success("✅ Vote submitted successfully!")
                        
                        if AUTO_LOGOUT_AFTER_VOTING:
                            st.info("Thank you for voting! You will be automatically logged out...")
                            logout_user("Automatically logged out after voting")
                        else:
                            st.rerun()

            with col2:
                if st.button("Logout"):
                    logout_user()
        else:
            st.warning("Voting is currently closed.")

def results_section():
    """Results section content - Admin only"""
    st.header("Election Results - Admin View")
    st.info("🔒 Results are only visible to administrators")
    display_results()

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
        'Treasurer': {'Okikiimole AKINDUSOYE': 0},
        'PRO': {'Joel ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
        'Sports Secretary': {'Nasirudeen Adeshina ALABI': 0, 'Ireoluwa OKE': 0},
        'Welfare Secretary': {'Oluwadunmininu IDOWU': 0, 'Simbiat O. ADUMADEYIN': 0, 'Olamiposi latcefat RAJI': 0},
        'Social Secretary': {'Oluwagbotemi Fatiu ADEBAYO': 0, 'Vivian AGWOILE': 0}
    }
if 'admin_sidebar_visible' not in st.session_state:
    st.session_state.admin_sidebar_visible = False
if 'show_password_recovery' not in st.session_state:
    st.session_state.show_password_recovery = False

# --- Check for Session Timeout ---
if st.session_state.authenticated and check_session_timeout():
    logout_user("Session expired after 5 minutes of inactivity")

# --- App UI ---
st.title("BellsTech's Student Voting System")

# --- Session Status Display ---
if st.session_state.authenticated and not st.session_state.get('is_admin', False):
    remaining_time = get_session_time_remaining()
    if remaining_time > 0:
        st.info(f"⏱️ Session expires in {remaining_time} minute(s)")
        if remaining_time <= 1:
            st.warning("⚠️ Your session will expire soon!")
    else:
        logout_user("Session expired")

# --- Admin Sidebar Access ---
if st.session_state.get('is_admin', False):
    admin_sidebar = st.sidebar.container()
    
    if not st.session_state.admin_sidebar_visible:
        if admin_sidebar.button("Show Admin Panel"):
            st.session_state.admin_sidebar_visible = True
            st.rerun()
    else:
        admin_sidebar.title("Results Management")
        
        if admin_sidebar.button("🔄 Load Saved Results"):
            load_saved_results()

        if admin_sidebar.button("💾 Save Results Now"):
            results_df = save_results()
            admin_sidebar.success("Results saved successfully!")

        if admin_sidebar.button("📊 Export to Excel"):
            excel_data = export_excel()
            admin_sidebar.download_button(
                label="📥 Download Excel File",
                data=excel_data,
                file_name=f"election_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
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

# --- Main Application Logic ---
if st.session_state.get('is_admin', False):
    tab1, tab2 = st.tabs(["Voting", "Results"])
    
    with tab1:
        voting_section()
    
    with tab2:
        results_section()
else:
    voting_section()

# --- Setup Instructions ---
if st.session_state.voter_df.empty:
    with st.expander("⚠️ Setup Required - Click to view instructions"):
        st.markdown("""
        ### Quick Setup Instructions:
        
        1. **Create votersdetails.csv** with columns: `Mat Number`, `Password`, `Email`, `Full Name`
        2. **Configure email settings** in EMAIL_CONFIG section
        3. **For Gmail**: Enable 2FA and use app password
        
        Example CSV:
        ```
        Mat Number,Password,Email,Full Name
        STU001,pass123,student1@university.edu,John Doe
        ```
        """)