# # import streamlit as st
# # import pandas as pd
# # from io import BytesIO
# # import re
# # from datetime import datetime
# # import matplotlib.pyplot as plt
# # import os
# # import json
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart


# # # --- Voting Time Settings ---
# # VOTING_START = datetime(2025, 5, 23, 9, 0, 0)  # 9:00 AM
# # VOTING_END = datetime(2025, 5, 23, 13, 0, 0)   # 12:00 PM

# # # --- Email Configuration (Update these with your email settings) ---
# # EMAIL_CONFIG = {
# #     'smtp_server': 'smtp.gmail.com',  # Change to your streSMTP server
# #     'smtp_port': 587,
# #     'sender_email': 'your_email@gmail.com',  # Change to your email
# #     'sender_password': 'your_app_password',  # Use app password for Gmail
# # }

# # # --- Helper Functions ---
# # def clean_spaces(value):
# #     if isinstance(value, str):
# #         return re.sub(r'\s+', ' ', value.strip())
# #     return value

# # def load_voter_data():
# #     try:
# #         df = pd.read_csv("votersdetails.csv")
# #         df = df.applymap(clean_spaces)
# #         df['Mat Number'] = df['Mat Number'].astype(str)
# #         # Ensure required columns exist
# #         required_columns = ['Mat Number', 'Password', 'Email']
# #         missing_columns = [col for col in required_columns if col not in df.columns]
# #         if missing_columns:
# #             st.error(f"Missing columns in votersdetails.csv: {', '.join(missing_columns)}")
# #             st.info("Please ensure your CSV has columns: Mat Number, Password, Email, and optionally Full Name")
# #             return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
# #         return df
# #     except FileNotFoundError:
# #         st.error("Error loading voter data. Please ensure 'votersdetails.csv' exists.")
# #         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
# #     except Exception as e:
# #         st.error(f"Error loading voter data: {str(e)}")
# #         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})

# # def send_password_email(email, password, name="Student"):
# #     """Send password to user's email"""
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = EMAIL_CONFIG['sender_email']
# #         msg['To'] = email
# #         msg['Subject'] = "BellsTech Voting System - Password Recovery"
        
# #         body = f"""
# # Dear {name},

# # Your login credentials for the BellsTech Student Voting System:

# # Email: {email}
# # Password: {password}

# # Please use these credentials to log in and cast your vote.

# # Voting Period: {VOTING_START.strftime('%B %d, %Y at %I:%M %p')} - {VOTING_END.strftime('%B %d, %Y at %I:%M %p')}

# # Best regards,
# # BellsTech Election Committee
# #         """
        
# #         msg.attach(MIMEText(body, 'plain'))
        
# #         server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
# #         server.starttls()
# #         server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
# #         text = msg.as_string()
# #         server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
# #         server.quit()
# #         return True
# #     except Exception as e:
# #         st.error(f"Failed to send email: {str(e)}")
# #         return False

# # def has_already_voted(identifier):
# #     """Check if user has voted using either mat number or email"""
# #     return str(identifier) in st.session_state.voted

# # def load_saved_results():
# #     """Load previously saved election results if they exist"""
# #     if os.path.exists('election_results.json'):
# #         with open('election_results.json', 'r') as f:
# #             data = json.load(f)
# #             st.session_state.votes = data['votes']
# #             st.session_state.voted = set(data['voted'])
# #             st.success("Previously saved results loaded successfully.")

# # def save_results():
# #     """Save current election results to file"""
# #     data = {
# #         'votes': st.session_state.votes,
# #         'voted': list(st.session_state.voted),
# #         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #     }
    
# #     with open('election_results.json', 'w') as f:
# #         json.dump(data, f, indent=2)
    
# #     # Also save as CSV for easy analysis
# #     results_df = pd.DataFrame(st.session_state.votes).T
# #     results_df.to_csv('election_results.csv')
    
# #     # Save list of voters who have voted
# #     voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted)})
# #     voted_df.to_csv('voted_students.csv', index=False)
    
# #     return results_df

# # def export_excel():
# #     """Export results to Excel file"""
# #     output = BytesIO()
    
# #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #         # Results sheet
# #         results_df = pd.DataFrame(st.session_state.votes).T
# #         results_df.to_excel(writer, sheet_name='Results')
        
# #         # Participation sheet
# #         voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted), 'Status': 'Voted'})
# #         voted_df.to_excel(writer, sheet_name='Voted Students', index=False)
        
# #         # Summary sheet
# #         total_voters = len(st.session_state.voter_df)
# #         voted_count = len(st.session_state.voted)
# #         participation = (voted_count / total_voters * 100) if total_voters else 0
        
# #         summary_data = {
# #             'Metric': ['Total Eligible Voters', 'Total Votes Cast', 'Participation Rate'],
# #             'Value': [total_voters, voted_count, f"{participation:.1f}%"]
# #         }
# #         pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
# #     return output.getvalue()

# # def display_results():
# #     """Display election results with charts"""
# #     # Show participation statistics
# #     total_voters = len(st.session_state.voter_df)
# #     voted_count = len(st.session_state.voted)
    
# #     col1, col2 = st.columns(2)
# #     col1.metric("Total Eligible Voters", total_voters)
# #     col2.metric("Total Votes Cast", f"{voted_count} ({(voted_count / total_voters * 100) if total_voters else 0:.1f}%)")
    
# #     # Create visualizations for each position
# #     for position, candidates in st.session_state.votes.items():
# #         st.subheader(f"{position}")
# #         total = sum(candidates.values())
        
# #         if total == 0:
# #             st.info(f"No votes recorded for {position}")
# #             continue
            
# #         # Create bar chart
# #         fig, ax = plt.subplots(figsize=(8, 4))
# #         colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
# #         names = list(candidates.keys())
# #         values = list(candidates.values())
# #         percentages = [(v / total * 100) if total else 0 for v in values]
        
# #         bars = ax.bar(names, values, color=colors[:len(names)])
        
# #         # Add labels
# #         for i, (bar, value, percent) in enumerate(zip(bars, values, percentages)):
# #             ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
# #                    f"{value} ({percent:.1f}%)", 
# #                    ha='center', va='bottom', fontsize=9)
        
# #         ax.set_ylabel('Votes')
# #         ax.set_title(f'{position} Results')
# #         plt.xticks(rotation=15, ha='right', fontsize=9)
# #         plt.tight_layout()
        
# #         st.pyplot(fig)
# #         plt.close(fig)  # Close to free memory

# # def authenticate_user(email, password):
# #     """Authenticate user with email and password"""
# #     if st.session_state.voter_df.empty:
# #         return False, "No voter data available"
    
# #     # Check if email exists
# #     email_exists = (st.session_state.voter_df['Email'].str.lower() == email.lower()).any()
    
# #     if not email_exists:
# #         return False, "Email not found in voter database"
    
# #     # Get user record
# #     user_record = st.session_state.voter_df[st.session_state.voter_df['Email'].str.lower() == email.lower()].iloc[0]
    
# #     # Verify password
# #     if user_record['Password'] != password:
# #         return False, "Incorrect password"
    
# #     # Check if already voted
# #     if has_already_voted(email) or has_already_voted(user_record['Mat Number']):
# #         return False, "You have already voted"
    
# #     return True, user_record

# # # --- Initialize Session State ---
# # if 'voter_df' not in st.session_state:
# #     st.session_state.voter_df = load_voter_data()
# # if 'authenticated' not in st.session_state:
# #     st.session_state.authenticated = False
# # if 'voted' not in st.session_state:
# #     st.session_state.voted = set()
# # if 'votes' not in st.session_state:
# #     st.session_state.votes = {
# #         'President': {'Prince John ANIGBO': 0, 'Covenant Olamigoke OLOWO': 0},
# #         'Vice President': {'Esther OGUNLEYE': 0, 'Hafsoh K. OGUNNIYI': 0},
# #         'General Secretary': {'Churchill OLISA': 0},
# #         'Assist. General Secretary': {'Frankcleave KASIMANWUNA': 0, 'Ajiserere ODUFISAN': 0, 'George IHEKWABA': 0},
# #         'Financial Secretary': {'F\'eyisayo OLATUNJI': 0},
# #         'Treasurer': {'Okikiimole AKINDUSOYE': 0, 'Pipolooluwa AYO-PONLE': 0},
# #         'PRO': {'Jocl ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
# #         'Sports Secretary': {'Nasirudeen Adeshina ALABI': 0, 'Ireoluwa OKE': 0},
# #         'Welfare Secretary': {'Oluwadunmininu IDOWU': 0, 'Simbiat O. ADUMADEYIN': 0, 'Olamiposi latcefat RAJI': 0},
# #         'Social Secretary': {'Oluwagbotemi Fatiu ADEBAYO': 0, 'Vivian AGWOILE': 0}
# #     }
# # if 'show_results' not in st.session_state:
# #     st.session_state.show_results = True
# # if 'admin_sidebar_visible' not in st.session_state:
# #     st.session_state.admin_sidebar_visible = False
# # if 'show_password_recovery' not in st.session_state:
# #     st.session_state.show_password_recovery = False

# # # --- App UI ---
# # st.title("BellsTech's Student Voting System")

# # # --- Admin Sidebar Access ---
# # if st.session_state.get('is_admin', False):
# #     admin_sidebar = st.sidebar.container()
    
# #     if not st.session_state.admin_sidebar_visible:
# #         if admin_sidebar.button("Show Admin Panel"):
# #             st.session_state.admin_sidebar_visible = True
# #             st.rerun()
# #     else:
# #         admin_sidebar.title("Results Management")
        
# #         # Load results button
# #         if admin_sidebar.button("🔄 Load Saved Results"):
# #             load_saved_results()

# #         # Save results option
# #         if admin_sidebar.button("💾 Save Results Now"):
# #             results_df = save_results()
# #             admin_sidebar.success("Results saved successfully to:")
# #             admin_sidebar.info("- election_results.json\n- election_results.csv\n- voted_students.csv")
# #             admin_sidebar.dataframe(results_df)

# #         # Excel export button
# #         if admin_sidebar.button("📊 Export to Excel"):
# #             excel_data = export_excel()
# #             admin_sidebar.download_button(
# #                 label="📥 Download Excel File",
# #                 data=excel_data,
# #                 file_name=f"election_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
# #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #             )
        
# #         # Hide sidebar button
# #         if admin_sidebar.button("Hide Admin Panel"):
# #             st.session_state.admin_sidebar_visible = False
# #             st.rerun()

# # # --- Voting Time Check ---
# # now = datetime.now()
# # if now < VOTING_START:
# #     time_left = VOTING_START - now
# #     st.warning(f"🕒 Voting has not started yet. It begins in {str(time_left).split('.')[0]}")
# # elif now > VOTING_END:
# #     st.info("🏁 Voting period has ended.")
# # else:
# #     time_left = VOTING_END - now
# #     st.info(f"⏳ Time remaining: {str(time_left).split('.')[0]}")

# # # --- Tabs for navigation ---
# # tab1, tab2 = st.tabs(["Voting", "Results"])

# # with tab1:
# #     # Authentication section
# #     if not st.session_state.authenticated:
# #         st.header("Voter Authentication")
        
# #         # Toggle between login and password recovery
# #         col1, col2 = st.columns([3, 1])
# #         with col2:
# #             if st.button("Forgot Password?"):
# #                 st.session_state.show_password_recovery = not st.session_state.show_password_recovery
# #                 st.rerun()
        
# #         if st.session_state.show_password_recovery:
# #             # Password Recovery Section
# #             st.subheader("Password Recovery")
# #             st.info("Enter your email address to receive your password")
            
# #             recovery_email = st.text_input("Email Address:", key="recovery_email").strip().lower()
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Send Password"):
# #                     if not recovery_email:
# #                         st.error("Please enter your email address")
# #                     else:
# #                         # Check if email exists in database
# #                         if st.session_state.voter_df.empty:
# #                             st.error("Voter database not available")
# #                         else:
# #                             user_match = st.session_state.voter_df[
# #                                 st.session_state.voter_df['Email'].str.lower() == recovery_email
# #                             ]
                            
# #                             if user_match.empty:
# #                                 st.error("Email not found in voter database")
# #                             else:
# #                                 user_record = user_match.iloc[0]
# #                                 name = user_record.get('Full Name', 'Student')
# #                                 password = user_record['Password']
                                
# #                                 # Try to send email
# #                                 if send_password_email(recovery_email, password, name):
# #                                     st.success("Password sent to your email address!")
# #                                     st.info("Please check your email and return to login")
# #                                 else:
# #                                     st.error("Failed to send email. Please contact the administrator.")
# #                                     # Show password directly if email fails
# #                                     st.warning(f"Your password is: **{password}**")
            
# #             with col2:
# #                 if st.button("Back to Login"):
# #                     st.session_state.show_password_recovery = False
# #                     st.rerun()
        
# #         else:
# #             # Login Section
# #             st.subheader("Login with Email")
# #             email = st.text_input("Email Address:").strip().lower()
# #             password = st.text_input("Password:", type="password")
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Login"):
# #                     if not email or not password:
# #                         st.error("Please enter both email and password")
# #                     else:
# #                         success, result = authenticate_user(email, password)
# #                         if success:
# #                             st.session_state.authenticated = True
# #                             st.session_state.current_user = email
# #                             st.session_state.current_user_record = result
# #                             st.success(f"Welcome, {result.get('Full Name', 'Student')}!")
# #                             st.rerun()
# #                         else:
# #                             st.error(result)
            
# #             with col2:
# #                 if st.button("Admin Login"):
# #                     admin_pass = st.text_input("Admin Password:", type="password", key="admin_pass")
# #                     if admin_pass == "X9@2&!p":
# #                         st.session_state.authenticated = True
# #                         st.session_state.is_admin = True
# #                         st.session_state.admin_sidebar_visible = True
# #                         st.rerun()
# #                     elif admin_pass:  # Only show error if password was entered
# #                         st.error("Invalid admin credentials")
    
# #     # Voting section
# #     else:
# #         user = st.session_state.get('current_user', '')
        
# #         if st.session_state.get('is_admin', False):
# #             st.success("Logged in as Administrator")
# #             if st.button("Logout"):
# #                 st.session_state.authenticated = False
# #                 st.session_state.is_admin = False
# #                 st.session_state.admin_sidebar_visible = False
# #                 st.rerun()
        
# #         elif has_already_voted(user):
# #             st.success("✅ You have already voted. Thank you!")
# #             if st.button("Logout"):
# #                 st.session_state.authenticated = False
# #                 st.rerun()
        
# #         elif VOTING_START <= now <= VOTING_END:
# #             st.header("Cast Your Vote")
            
# #             # Show user info
# #             user_record = st.session_state.get('current_user_record', {})
# #             if user_record is not None and not user_record.empty:
# #                 st.info(f"Voting as: {user_record.get('Full Name', 'Student')} ({user_record.get('Mat Number', 'N/A')})")
            
# #             # Voting form with no default values
# #             pres = st.radio("President:", ['Prince John ANIGBO', 'Covenant Olamigoke OLOWO'], index=None)
# #             vp = st.radio("Vice President:", ['Esther OGUNLEYE', 'Hafsoh K. OGUNNIYI'], index=None)
# #             gs = st.radio("General Secretary:", ['Churchill OLISA'], index=None)
# #             ags = st.radio("Assistant General Secretary:", ['Frankcleave KASIMANWUNA', 'Ajiserere ODUFISAN', 'George IHEKWABA'], index=None)
# #             fs = st.radio("Financial Secretary:", ['F\'eyisayo OLATUNJI'], index=None)
# #             tre = st.radio("Treasurer:", ['Pipolooluwa AYO-PONLE'], index=None)
# #             pro = st.radio("PRO:", ['Jocl ATUH', 'Steaadfast ILEOGBEN', 'Victor Folahanmi AKILO', 'Enoch OGUNTOYE'], index=None)
# #             sport = st.radio("Sports Secretary:", ['Nasirudeen Adeshina ALABI', 'Ireoluwa OKE'], index=None)
# #             welfare = st.radio("Welfare Secretary:", ['Oluwadunmininu IDOWU', 'Simbiat O. ADUMADEYIN', 'Olamiposi latcefat RAJI'], index=None)
# #             social = st.radio("Social Secretary:", ['Oluwagbotemi Fatiu ADEBAYO', 'Vivian AGWOILE'], index=None)

# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Submit Vote"):
# #                     # Check if all positions have been voted for
# #                     if None in [pres, vp, gs, ags, fs, tre, pro, sport, welfare, social]:
# #                         st.error("Please vote for all positions before submitting")
# #                     else:
# #                         # Update votes for all positions
# #                         st.session_state.votes['President'][pres] += 1
# #                         st.session_state.votes['Vice President'][vp] += 1
# #                         st.session_state.votes['General Secretary'][gs] += 1
# #                         st.session_state.votes['Assist. General Secretary'][ags] += 1
# #                         st.session_state.votes['Financial Secretary'][fs] += 1
# #                         st.session_state.votes['Treasurer'][tre] += 1
# #                         st.session_state.votes['PRO'][pro] += 1
# #                         st.session_state.votes['Sports Secretary'][sport] += 1
# #                         st.session_state.votes['Welfare Secretary'][welfare] += 1
# #                         st.session_state.votes['Social Secretary'][social] += 1
                        
# #                         # Mark as voted (use both email and mat number to prevent duplicate voting)
# #                         st.session_state.voted.add(user)  # email
# #                         user_record = st.session_state.get('current_user_record', {})
# #                         if user_record is not None and not user_record.empty:
# #                             st.session_state.voted.add(user_record.get('Mat Number', ''))
                        
# #                         # Auto-save results after each vote
# #                         save_results()
                        
# #                         st.success("✅ Vote submitted successfully!")
# #                         st.rerun()

# #             with col2:
# #                 if st.button("Logout"):
# #                     st.session_state.authenticated = False
# #                     st.rerun()
# #         else:
# #             st.warning("Voting is currently closed.")

# # with tab2:
# #     st.header("Election Results")
    
# #     # Admin controls for results visibility
# #     if st.session_state.get('is_admin', False):
# #         st.session_state.show_results = st.checkbox("Show results to everyone", value=st.session_state.show_results)
    
# #     # Check conditions for displaying results
# #     user = st.session_state.get('current_user', '')
# #     show_condition = (
# #         now > VOTING_END or 
# #         st.session_state.get('is_admin', False) or
# #         (user in st.session_state.voted and st.session_state.show_results)
# #     )
    
# #     if show_condition:
# #         display_results()
# #     else:
# #         st.warning("Results are only available after voting or to administrators.")

# # # --- Instructions for Setup ---
# # if st.session_state.voter_df.empty:
# #     st.error("⚠️ Setup Required")
# #     st.markdown("""
# #     ### Setup Instructions:
    
# #     1. **Create votersdetails.csv** with the following columns:
# #        - `Mat Number`: Student matriculation number
# #        - `Password`: Student password
# #        - `Email`: Student email address
# #        - `Full Name`: Student full name (optional)
    
# #     2. **Configure Email Settings** (in EMAIL_CONFIG):
# #        - Update `sender_email` with your email
# #        - Update `sender_password` with your app password
# #        - Update `smtp_server` if not using Gmail
    
# #     3. **For Gmail users:**
# #        - Enable 2-factor authentication
# #        - Generate an app password for this application
# #        - Use the app password, not your regular password
    
# #     Example CSV format:
# #     ```
# #     Mat Number,Password,Email,Full Name
# #     STU001,pass123,student1@university.edu,John Doe
# #     STU002,pass456,student2@university.edu,Jane Smith
# #     ```
# #     """)

# # import streamlit as st
# # import pandas as pd
# # from io import BytesIO
# # import re
# # from datetime import datetime, timedelta
# # import matplotlib.pyplot as plt
# # import os
# # import json
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import time


# # # --- Voting Time Settings ---
# # VOTING_START = datetime(2025, 5, 23, 10, 0, 0)  # 9:00 AM
# # VOTING_END = datetime(2025, 5, 23, 2, 0, 0)   # 12:00 PM

# # # --- Auto-logout Settings ---
# # SESSION_TIMEOUT_MINUTES = 5  # Auto-logout after 5 minutes
# # AUTO_LOGOUT_AFTER_VOTING = True  # Auto-logout after voting

# # # --- Email Configuration (Update these with your email settings) ---
# # EMAIL_CONFIG = {
# #     'smtp_server': 'smtp.gmail.com',  # Change to your streSMTP server
# #     'smtp_port': 587,
# #     'sender_email': 'your_email@gmail.com',  # Change to your email
# #     'sender_password': 'your_app_password',  # Use app password for Gmail
# # }

# # # --- Session Management Functions ---
# # def check_session_timeout():
# #     """Check if user session has timed out"""
# #     if not st.session_state.authenticated:
# #         return False
    
# #     if 'login_time' not in st.session_state:
# #         return False
    
# #     # Calculate time elapsed since login
# #     current_time = datetime.now()
# #     time_elapsed = current_time - st.session_state.login_time
    
# #     # Check if session has expired (5 minutes)
# #     if time_elapsed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
# #         return True
    
# #     return False

# # def logout_user(reason=""):
# #     """Log out the current user and clear session data"""
# #     st.session_state.authenticated = False
# #     st.session_state.is_admin = False
# #     st.session_state.admin_sidebar_visible = False
# #     st.session_state.current_user = ""
# #     st.session_state.current_user_record = {}
# #     st.session_state.show_password_recovery = False
    
# #     # Clear login time
# #     if 'login_time' in st.session_state:
# #         del st.session_state.login_time
    
# #     if reason:
# #         st.warning(f"You have been logged out: {reason}")
    
# #     st.rerun()

# # def update_last_activity():
# #     """Update the last activity time"""
# #     st.session_state.last_activity = datetime.now()

# # def get_session_time_remaining():
# #     """Get remaining session time in minutes"""
# #     if 'login_time' not in st.session_state:
# #         return 0
    
# #     elapsed = datetime.now() - st.session_state.login_time
# #     remaining = timedelta(minutes=SESSION_TIMEOUT_MINUTES) - elapsed
    
# #     if remaining.total_seconds() <= 0:
# #         return 0
    
# #     return int(remaining.total_seconds() / 60)

# # # --- Helper Functions ---
# # def clean_spaces(value):
# #     if isinstance(value, str):
# #         return re.sub(r'\s+', ' ', value.strip())
# #     return value

# # def load_voter_data():
# #     try:
# #         df = pd.read_csv("votersdetails.csv")
# #         df = df.applymap(clean_spaces)
# #         df['Mat Number'] = df['Mat Number'].astype(str)
# #         # Ensure required columns exist
# #         required_columns = ['Mat Number', 'Password', 'Email']
# #         missing_columns = [col for col in required_columns if col not in df.columns]
# #         if missing_columns:
# #             st.error(f"Missing columns in votersdetails.csv: {', '.join(missing_columns)}")
# #             st.info("Please ensure your CSV has columns: Mat Number, Password, Email, and optionally Full Name")
# #             return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
# #         return df
# #     except FileNotFoundError:
# #         st.error("Error loading voter data. Please ensure 'votersdetails.csv' exists.")
# #         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
# #     except Exception as e:
# #         st.error(f"Error loading voter data: {str(e)}")
# #         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})

# # def send_password_email(email, password, name="Student"):
# #     """Send password to user's email"""
# #     try:
# #         msg = MIMEMultipart()
# #         msg['From'] = EMAIL_CONFIG['sender_email']
# #         msg['To'] = email
# #         msg['Subject'] = "BellsTech Voting System - Password Recovery"
        
# #         body = f"""
# # Dear {name},

# # Your login credentials for the BellsTech Student Voting System:

# # Email: {email}
# # Password: {password}

# # Please use these credentials to log in and cast your vote.

# # Voting Period: {VOTING_START.strftime('%B %d, %Y at %I:%M %p')} - {VOTING_END.strftime('%B %d, %Y at %I:%M %p')}

# # Best regards,
# # BellsTech Election Committee
# #         """
        
# #         msg.attach(MIMEText(body, 'plain'))
        
# #         server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
# #         server.starttls()
# #         server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
# #         text = msg.as_string()
# #         server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
# #         server.quit()
# #         return True
# #     except Exception as e:
# #         st.error(f"Failed to send email: {str(e)}")
# #         return False

# # def has_already_voted(identifier):
# #     """Check if user has voted using either mat number or email"""
# #     return str(identifier) in st.session_state.voted

# # def load_saved_results():
# #     """Load previously saved election results if they exist"""
# #     if os.path.exists('election_results.json'):
# #         with open('election_results.json', 'r') as f:
# #             data = json.load(f)
# #             st.session_state.votes = data['votes']
# #             st.session_state.voted = set(data['voted'])
# #             st.success("Previously saved results loaded successfully.")

# # def save_results():
# #     """Save current election results to file"""
# #     data = {
# #         'votes': st.session_state.votes,
# #         'voted': list(st.session_state.voted),
# #         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #     }
    
# #     with open('election_results.json', 'w') as f:
# #         json.dump(data, f, indent=2)
    
# #     # Also save as CSV for easy analysis
# #     results_df = pd.DataFrame(st.session_state.votes).T
# #     results_df.to_csv('election_results.csv')
    
# #     # Save list of voters who have voted
# #     voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted)})
# #     voted_df.to_csv('voted_students.csv', index=False)
    
# #     return results_df

# # def export_excel():
# #     """Export results to Excel file"""
# #     output = BytesIO()
    
# #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #         # Results sheet
# #         results_df = pd.DataFrame(st.session_state.votes).T
# #         results_df.to_excel(writer, sheet_name='Results')
        
# #         # Participation sheet
# #         voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted), 'Status': 'Voted'})
# #         voted_df.to_excel(writer, sheet_name='Voted Students', index=False)
        
# #         # Summary sheet
# #         total_voters = len(st.session_state.voter_df)
# #         voted_count = len(st.session_state.voted)
# #         participation = (voted_count / total_voters * 100) if total_voters else 0
        
# #         summary_data = {
# #             'Metric': ['Total Eligible Voters', 'Total Votes Cast', 'Participation Rate'],
# #             'Value': [total_voters, voted_count, f"{participation:.1f}%"]
# #         }
# #         pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
# #     return output.getvalue()

# # def display_results():
# #     """Display election results with charts"""
# #     # Show participation statistics
# #     total_voters = len(st.session_state.voter_df)
# #     voted_count = len(st.session_state.voted)
    
# #     col1, col2 = st.columns(2)
# #     col1.metric("Total Eligible Voters", total_voters)
# #     col2.metric("Total Votes Cast", f"{voted_count} ({(voted_count / total_voters * 100) if total_voters else 0:.1f}%)")
    
# #     # Create visualizations for each position
# #     for position, candidates in st.session_state.votes.items():
# #         st.subheader(f"{position}")
# #         total = sum(candidates.values())
        
# #         if total == 0:
# #             st.info(f"No votes recorded for {position}")
# #             continue
            
# #         # Create bar chart
# #         fig, ax = plt.subplots(figsize=(8, 4))
# #         colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
# #         names = list(candidates.keys())
# #         values = list(candidates.values())
# #         percentages = [(v / total * 100) if total else 0 for v in values]
        
# #         bars = ax.bar(names, values, color=colors[:len(names)])
        
# #         # Add labels
# #         for i, (bar, value, percent) in enumerate(zip(bars, values, percentages)):
# #             ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
# #                    f"{value} ({percent:.1f}%)", 
# #                    ha='center', va='bottom', fontsize=9)
        
# #         ax.set_ylabel('Votes')
# #         ax.set_title(f'{position} Results')
# #         plt.xticks(rotation=15, ha='right', fontsize=9)
# #         plt.tight_layout()
        
# #         st.pyplot(fig)
# #         plt.close(fig)  # Close to free memory

# # def authenticate_user(email, password):
# #     """Authenticate user with email and password"""
# #     if st.session_state.voter_df.empty:
# #         return False, "No voter data available"
    
# #     # Check if email exists
# #     email_exists = (st.session_state.voter_df['Email'].str.lower() == email.lower()).any()
    
# #     if not email_exists:
# #         return False, "Email not found in voter database"
    
# #     # Get user record
# #     user_record = st.session_state.voter_df[st.session_state.voter_df['Email'].str.lower() == email.lower()].iloc[0]
    
# #     # Verify password
# #     if user_record['Password'] != password:
# #         return False, "Incorrect password"
    
# #     # Check if already voted
# #     if has_already_voted(email) or has_already_voted(user_record['Mat Number']):
# #         return False, "You have already voted"
    
# #     return True, user_record

# # # --- Initialize Session State ---
# # if 'voter_df' not in st.session_state:
# #     st.session_state.voter_df = load_voter_data()
# # if 'authenticated' not in st.session_state:
# #     st.session_state.authenticated = False
# # if 'voted' not in st.session_state:
# #     st.session_state.voted = set()
# # if 'votes' not in st.session_state:
# #     st.session_state.votes = {
# #         'President': {'Prince John ANIGBO': 0, 'Covenant Olamigoke OLOWO': 0},
# #         'Vice President': {'Esther OGUNLEYE': 0, 'Hafsoh K. OGUNNIYI': 0},
# #         'General Secretary': {'Churchill OLISA': 0},
# #         'Assist. General Secretary': {'Frankcleave KASIMANWUNA': 0, 'Ajiserere ODUFISAN': 0, 'George IHEKWABA': 0},
# #         'Financial Secretary': {'F\'eyisayo OLATUNJI': 0},
# #         'Treasurer': {'Okikiimole AKINDUSOYE': 0, 'Pipolooluwa AYO-PONLE': 0},
# #         'PRO': {'Jocl ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
# #         'Sports Secretary': {'Nasirudeen Adeshina ALABI': 0, 'Ireoluwa OKE': 0},
# #         'Welfare Secretary': {'Oluwadunmininu IDOWU': 0, 'Simbiat O. ADUMADEYIN': 0, 'Olamiposi latcefat RAJI': 0},
# #         'Social Secretary': {'Oluwagbotemi Fatiu ADEBAYO': 0, 'Vivian AGWOILE': 0}
# #     }
# # if 'show_results' not in st.session_state:
# #     st.session_state.show_results = True
# # if 'admin_sidebar_visible' not in st.session_state:
# #     st.session_state.admin_sidebar_visible = False
# # if 'show_password_recovery' not in st.session_state:
# #     st.session_state.show_password_recovery = False

# # # --- Check for Session Timeout ---
# # if st.session_state.authenticated and check_session_timeout():
# #     logout_user("Session expired after 5 minutes of inactivity")

# # # --- App UI ---
# # st.title("BellsTech's Student Voting System")

# # # --- Session Status Display ---
# # if st.session_state.authenticated and not st.session_state.get('is_admin', False):
# #     remaining_time = get_session_time_remaining()
# #     if remaining_time > 0:
# #         st.info(f"⏱️ Session expires in {remaining_time} minute(s)")
        
# #         # Auto-refresh to check session timeout
# #         if remaining_time <= 1:  # Warning when less than 1 minute left
# #             st.warning("⚠️ Your session will expire soon!")
# #     else:
# #         logout_user("Session expired")

# # # --- Admin Sidebar Access ---
# # if st.session_state.get('is_admin', False):
# #     admin_sidebar = st.sidebar.container()
    
# #     if not st.session_state.admin_sidebar_visible:
# #         if admin_sidebar.button("Show Admin Panel"):
# #             st.session_state.admin_sidebar_visible = True
# #             st.rerun()
# #     else:
# #         admin_sidebar.title("Results Management")
        
# #         # Load results button
# #         if admin_sidebar.button("🔄 Load Saved Results"):
# #             load_saved_results()

# #         # Save results option
# #         if admin_sidebar.button("💾 Save Results Now"):
# #             results_df = save_results()
# #             admin_sidebar.success("Results saved successfully to:")
# #             admin_sidebar.info("- election_results.json\n- election_results.csv\n- voted_students.csv")
# #             admin_sidebar.dataframe(results_df)

# #         # Excel export button
# #         if admin_sidebar.button("📊 Export to Excel"):
# #             excel_data = export_excel()
# #             admin_sidebar.download_button(
# #                 label="📥 Download Excel File",
# #                 data=excel_data,
# #                 file_name=f"election_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
# #                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #             )
        
# #         # Hide sidebar button
# #         if admin_sidebar.button("Hide Admin Panel"):
# #             st.session_state.admin_sidebar_visible = False
# #             st.rerun()

# # # --- Voting Time Check ---
# # now = datetime.now()
# # if now < VOTING_START:
# #     time_left = VOTING_START - now
# #     st.warning(f"🕒 Voting has not started yet. It begins in {str(time_left).split('.')[0]}")
# # elif now > VOTING_END:
# #     st.info("🏁 Voting period has ended.")
# # else:
# #     time_left = VOTING_END - now
# #     st.info(f"⏳ Time remaining: {str(time_left).split('.')[0]}")

# # # --- Tabs for navigation ---
# # tab1, tab2 = st.tabs(["Voting", "Results"])

# # with tab1:
# #     # Authentication section
# #     if not st.session_state.authenticated:
# #         st.header("Voter Authentication")
        
# #         # Toggle between login and password recovery
# #         col1, col2 = st.columns([3, 1])
# #         with col2:
# #             if st.button("Forgot Password?"):
# #                 st.session_state.show_password_recovery = not st.session_state.show_password_recovery
# #                 st.rerun()
        
# #         if st.session_state.show_password_recovery:
# #             # Password Recovery Section
# #             st.subheader("Password Recovery")
# #             st.info("Enter your email address to receive your password")
            
# #             recovery_email = st.text_input("Email Address:", key="recovery_email").strip().lower()
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Send Password"):
# #                     if not recovery_email:
# #                         st.error("Please enter your email address")
# #                     else:
# #                         # Check if email exists in database
# #                         if st.session_state.voter_df.empty:
# #                             st.error("Voter database not available")
# #                         else:
# #                             user_match = st.session_state.voter_df[
# #                                 st.session_state.voter_df['Email'].str.lower() == recovery_email
# #                             ]
                            
# #                             if user_match.empty:
# #                                 st.error("Email not found in voter database")
# #                             else:
# #                                 user_record = user_match.iloc[0]
# #                                 name = user_record.get('Full Name', 'Student')
# #                                 password = user_record['Password']
                                
# #                                 # Try to send email
# #                                 if send_password_email(recovery_email, password, name):
# #                                     st.success("Password sent to your email address!")
# #                                     st.info("Please check your email and return to login")
# #                                 else:
                                    
# #                                     # Show password directly if email fails
# #                                     st.warning(f"Your password is: **{password}**")
# #                                     st.error("Go to lecture hall 1 if you can not retrieve your password.")
            
# #             with col2:
# #                 if st.button("Back to Login"):
# #                     st.session_state.show_password_recovery = False
# #                     st.rerun()
        
# #         else:
# #             # Login Section
# #             st.subheader("Login with Email")
# #             email = st.text_input("Email Address:").strip().lower()
# #             password = st.text_input("Password:", type="password")
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Login"):
# #                     if not email or not password:
# #                         st.error("Please enter both email and password")
# #                     else:
# #                         success, result = authenticate_user(email, password)
# #                         if success:
# #                             st.session_state.authenticated = True
# #                             st.session_state.current_user = email
# #                             st.session_state.current_user_record = result
# #                             st.session_state.login_time = datetime.now()  # Set login time
# #                             st.success(f"Welcome, {result.get('Full Name', 'Student')}!")
# #                             st.rerun()
# #                         else:
# #                             st.error(result)
            
# #             with col2:
# #                 if st.button("Admin Login"):
# #                     admin_pass = st.text_input("Admin Password:", type="password", key="admin_pass")
# #                     if admin_pass == "X9@2&!p":
# #                         st.session_state.authenticated = True
# #                         st.session_state.is_admin = True
# #                         st.session_state.admin_sidebar_visible = True
# #                         st.session_state.login_time = datetime.now()  # Set login time for admin
# #                         st.rerun()
# #                     elif admin_pass:  # Only show error if password was entered
# #                         st.error("Invalid admin credentials")
    
# #     # Voting section
# #     else:
# #         user = st.session_state.get('current_user', '')
        
# #         if st.session_state.get('is_admin', False):
# #             st.success("Logged in as Administrator")
# #             if st.button("Logout"):
# #                 logout_user()
        
# #         elif has_already_voted(user):
# #             st.success("✅ You have already voted. Thank you!")
            
# #             # Auto-logout after voting if enabled
# #             if AUTO_LOGOUT_AFTER_VOTING:
# #                 st.info("You will be automatically logged out in 3 seconds...")
# #                 time.sleep(3)
# #                 logout_user("Automatically logged out after voting")
# #             else:
# #                 if st.button("Logout"):
# #                     logout_user()
        
# #         elif VOTING_START <= now <= VOTING_END:
# #             st.header("Cast Your Vote")
            
# #             # Show user info
# #             user_record = st.session_state.get('current_user_record', {})
# #             if user_record is not None and not user_record.empty:
# #                 st.info(f"Voting as: {user_record.get('Full Name', 'Student')} ({user_record.get('Mat Number', 'N/A')})")
            
# #             # Voting form with no default values
# #             pres = st.radio("President:", ['Prince John ANIGBO', 'Covenant Olamigoke OLOWO'], index=None)
# #             vp = st.radio("Vice President:", ['Esther OGUNLEYE', 'Hafsoh K. OGUNNIYI'], index=None)
# #             gs = st.radio("General Secretary:", ['Churchill OLISA'], index=None)
# #             ags = st.radio("Assistant General Secretary:", ['Frankcleave KASIMANWUNA', 'Ajiserere ODUFISAN', 'George IHEKWABA'], index=None)
# #             fs = st.radio("Financial Secretary:", ['F\'eyisayo OLATUNJI'], index=None)
# #             tre = st.radio("Treasurer:", ['Okikiimole AKINDUSOYE', 'Pipolooluwa AYO-PONLE'], index=None)
# #             pro = st.radio("PRO:", ['Jocl ATUH', 'Steaadfast ILEOGBEN', 'Victor Folahanmi AKILO', 'Enoch OGUNTOYE'], index=None)
# #             sport = st.radio("Sports Secretary:", ['Nasirudeen Adeshina ALABI', 'Ireoluwa OKE'], index=None)
# #             welfare = st.radio("Welfare Secretary:", ['Oluwadunmininu IDOWU', 'Simbiat O. ADUMADEYIN', 'Olamiposi latcefat RAJI'], index=None)
# #             social = st.radio("Social Secretary:", ['Oluwagbotemi Fatiu ADEBAYO', 'Vivian AGWOILE'], index=None)

# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button("Submit Vote"):
# #                     # Check if all positions have been voted for
# #                     if None in [pres, vp, gs, ags, fs, tre, pro, sport, welfare, social]:
# #                         st.error("Please vote for all positions before submitting")
# #                     else:
# #                         # Update votes for all positions
# #                         st.session_state.votes['President'][pres] += 1
# #                         st.session_state.votes['Vice President'][vp] += 1
# #                         st.session_state.votes['General Secretary'][gs] += 1
# #                         st.session_state.votes['Assist. General Secretary'][ags] += 1
# #                         st.session_state.votes['Financial Secretary'][fs] += 1
# #                         st.session_state.votes['Treasurer'][tre] += 1
# #                         st.session_state.votes['PRO'][pro] += 1
# #                         st.session_state.votes['Sports Secretary'][sport] += 1
# #                         st.session_state.votes['Welfare Secretary'][welfare] += 1
# #                         st.session_state.votes['Social Secretary'][social] += 1
                        
# #                         # Mark as voted (use both email and mat number to prevent duplicate voting)
# #                         st.session_state.voted.add(user)  # email
# #                         user_record = st.session_state.get('current_user_record', {})
# #                         if user_record is not None and not user_record.empty:
# #                             st.session_state.voted.add(user_record.get('Mat Number', ''))
                        
# #                         # Auto-save results after each vote
# #                         save_results()
                        
# #                         st.success("✅ Vote submitted successfully!")
                        
# #                         # Auto-logout after voting if enabled
# #                         if AUTO_LOGOUT_AFTER_VOTING:
# #                             st.info("Thank you for voting! You will be automatically logged out in 3 seconds...")
# #                             time.sleep(3)
# #                             logout_user("Automatically logged out after voting")
# #                         else:
# #                             st.rerun()

# #             with col2:
# #                 if st.button("Logout"):
# #                     logout_user()
# #         else:
# #             st.warning("Voting is currently closed.")

# # with tab2:
# #     st.header("Election Results")
    
# #     # Admin controls for results visibility
# #     if st.session_state.get('is_admin', False):
# #         st.session_state.show_results = st.checkbox("Show results to everyone", value=st.session_state.show_results)
    
# #     # Check conditions for displaying results
# #     user = st.session_state.get('current_user', '')
# #     show_condition = (
# #         now > VOTING_END or 
# #         st.session_state.get('is_admin', False) or
# #         (user in st.session_state.voted and st.session_state.show_results)
# #     )
    
# #     if show_condition:
# #         display_results()
# #     else:
# #         st.warning("Results are only available after voting or to administrators.")

# # # --- Instructions for Setup ---
# # if st.session_state.voter_df.empty:
# #     st.error("⚠️ Setup Required")
# #     st.markdown("""
# #     ### Setup Instructions:
    
# #     1. **Create votersdetails.csv** with the following columns:
# #        - `Mat Number`: Student matriculation number
# #        - `Password`: Student password
# #        - `Email`: Student email address
# #        - `Full Name`: Student full name (optional)
    
# #     2. **Configure Email Settings** (in EMAIL_CONFIG):
# #        - Update `sender_email` with your email
# #        - Update `sender_password` with your app password
# #        - Update `smtp_server` if not using Gmail
    
# #     3. **For Gmail users:**
# #        - Enable 2-factor authentication
# #        - Generate an app password for this application
# #        - Use the app password, not your regular password
    
# #     4. **Auto-logout Settings:**
# #        - Users are automatically logged out after 5 minutes of login
# #        - Users are automatically logged out immediately after voting
# #        - Session timeout and auto-logout can be configured at the top of the script
    
# #     Example CSV format:
# #     ```
# #     Mat Number,Password,Email,Full Name
# #     STU001,pass123,student1@university.edu,John Doe
# #     STU002,pass456,student2@university.edu,Jane Smith
# #     ```
# #     """)

# # # --- Auto-refresh for session management ---
# # if st.session_state.authenticated:
# #     # Add a small delay to allow for proper session timeout checking
# #     time.sleep(0.1)


# import streamlit as st
# import pandas as pd
# from io import BytesIO
# import re
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
# import os
# import json
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import time


# # --- Voting Time Settings ---
# VOTING_START = datetime(2025, 5, 20, 9, 0, 0)  # 9:00 AM
# VOTING_END = datetime(2025, 5, 23, 13, 0, 0)   # 12:00 PM

# # --- Auto-logout Settings ---
# SESSION_TIMEOUT_MINUTES = 5  # Auto-logout after 5 minutes
# AUTO_LOGOUT_AFTER_VOTING = True  # Auto-logout after voting

# # --- Email Configuration (Update these with your email settings) ---
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.gmail.com',  # Change to your SMTP server
#     'smtp_port': 587,
#     'sender_email': 'your_email@gmail.com',  # Change to your email
#     'sender_password': 'your_app_password',  # Use app password for Gmail
# }

# # --- Session Management Functions ---
# def check_session_timeout():
#     """Check if user session has timed out"""
#     if not st.session_state.authenticated:
#         return False
    
#     if 'login_time' not in st.session_state:
#         return False
    
#     # Calculate time elapsed since login
#     current_time = datetime.now()
#     time_elapsed = current_time - st.session_state.login_time
    
#     # Check if session has expired (5 minutes)
#     if time_elapsed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
#         return True
    
#     return False

# def logout_user(reason=""):
#     """Log out the current user and clear session data"""
#     st.session_state.authenticated = False
#     st.session_state.is_admin = False
#     st.session_state.admin_sidebar_visible = False
#     st.session_state.current_user = ""
#     st.session_state.current_user_record = {}
#     st.session_state.show_password_recovery = False
    
#     # Clear login time
#     if 'login_time' in st.session_state:
#         del st.session_state.login_time
    
#     if reason:
#         st.warning(f"You have been logged out: {reason}")
    
#     st.rerun()

# def update_last_activity():
#     """Update the last activity time"""
#     st.session_state.last_activity = datetime.now()

# def get_session_time_remaining():
#     """Get remaining session time in minutes"""
#     if 'login_time' not in st.session_state:
#         return 0
    
#     elapsed = datetime.now() - st.session_state.login_time
#     remaining = timedelta(minutes=SESSION_TIMEOUT_MINUTES) - elapsed
    
#     if remaining.total_seconds() <= 0:
#         return 0
    
#     return int(remaining.total_seconds() / 60)

# # --- Helper Functions ---
# def clean_spaces(value):
#     if isinstance(value, str):
#         return re.sub(r'\s+', ' ', value.strip())
#     return value

# def load_voter_data():
#     try:
#         df = pd.read_csv("votersdetails.csv")
#         df = df.applymap(clean_spaces)
#         df['Mat Number'] = df['Mat Number'].astype(str)
#         # Ensure required columns exist
#         required_columns = ['Mat Number', 'Password', 'Email']
#         missing_columns = [col for col in required_columns if col not in df.columns]
#         if missing_columns:
#             st.error(f"Missing columns in votersdetails.csv: {', '.join(missing_columns)}")
#             st.info("Please ensure your CSV has columns: Mat Number, Password, Email, and optionally Full Name")
#             return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
#         return df
#     except FileNotFoundError:
#         st.error("Error loading voter data. Please ensure 'votersdetails.csv' exists.")
#         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})
#     except Exception as e:
#         st.error(f"Error loading voter data: {str(e)}")
#         return pd.DataFrame({"Mat Number": [], "Password": [], "Email": [], "Full Name": []})

# def send_password_email(email, password, name="Student"):
#     """Send password to user's email"""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = EMAIL_CONFIG['sender_email']
#         msg['To'] = email
#         msg['Subject'] = "BellsTech Voting System - Password Recovery"
        
#         body = f"""
# Dear {name},

# Your login credentials for the BellsTech Student Voting System:

# Email: {email}
# Password: {password}

# Please use these credentials to log in and cast your vote.

# Voting Period: {VOTING_START.strftime('%B %d, %Y at %I:%M %p')} - {VOTING_END.strftime('%B %d, %Y at %I:%M %p')}

# Best regards,
# BellsTech Election Committee
#         """
        
#         msg.attach(MIMEText(body, 'plain'))
        
#         server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
#         server.starttls()
#         server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
#         text = msg.as_string()
#         server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
#         server.quit()
#         return True
#     except Exception as e:
#         st.error(f"Failed to send email: {str(e)}")
#         return False

# def has_already_voted(identifier):
#     """Check if user has voted using either mat number or email"""
#     return str(identifier) in st.session_state.voted

# def load_saved_results():
#     """Load previously saved election results if they exist"""
#     if os.path.exists('election_results.json'):
#         with open('election_results.json', 'r') as f:
#             data = json.load(f)
#             st.session_state.votes = data['votes']
#             st.session_state.voted = set(data['voted'])
#             st.success("Previously saved results loaded successfully.")

# def save_results():
#     """Save current election results to file"""
#     data = {
#         'votes': st.session_state.votes,
#         'voted': list(st.session_state.voted),
#         'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     }
    
#     with open('election_results.json', 'w') as f:
#         json.dump(data, f, indent=2)
    
#     # Also save as CSV for easy analysis
#     results_df = pd.DataFrame(st.session_state.votes).T
#     results_df.to_csv('election_results.csv')
    
#     # Save list of voters who have voted
#     voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted)})
#     voted_df.to_csv('voted_students.csv', index=False)
    
#     return results_df

# def export_excel():
#     """Export results to Excel file"""
#     output = BytesIO()
    
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         # Results sheet
#         results_df = pd.DataFrame(st.session_state.votes).T
#         results_df.to_excel(writer, sheet_name='Results')
        
#         # Participation sheet
#         voted_df = pd.DataFrame({'Identifier': list(st.session_state.voted), 'Status': 'Voted'})
#         voted_df.to_excel(writer, sheet_name='Voted Students', index=False)
        
#         # Summary sheet
#         total_voters = len(st.session_state.voter_df)
#         voted_count = len(st.session_state.voted)
#         participation = (voted_count / total_voters * 100) if total_voters else 0
        
#         summary_data = {
#             'Metric': ['Total Eligible Voters', 'Total Votes Cast', 'Participation Rate'],
#             'Value': [total_voters, voted_count, f"{participation:.1f}%"]
#         }
#         pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
#     return output.getvalue()

# def display_results():
#     """Display election results with charts"""
#     # Show participation statistics
#     total_voters = len(st.session_state.voter_df)
#     voted_count = len(st.session_state.voted)
    
#     col1, col2 = st.columns(2)
#     col1.metric("Total Eligible Voters", total_voters)
#     col2.metric("Total Votes Cast", f"{voted_count} ({(voted_count / total_voters * 100) if total_voters else 0:.1f}%)")
    
#     # Create visualizations for each position
#     for position, candidates in st.session_state.votes.items():
#         st.subheader(f"{position}")
#         total = sum(candidates.values())
        
#         if total == 0:
#             st.info(f"No votes recorded for {position}")
#             continue
            
#         # Create bar chart
#         fig, ax = plt.subplots(figsize=(8, 4))
#         colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
#         names = list(candidates.keys())
#         values = list(candidates.values())
#         percentages = [(v / total * 100) if total else 0 for v in values]
        
#         bars = ax.bar(names, values, color=colors[:len(names)])
        
#         # Add labels
#         for i, (bar, value, percent) in enumerate(zip(bars, values, percentages)):
#             ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
#                    f"{value} ({percent:.1f}%)", 
#                    ha='center', va='bottom', fontsize=9)
        
#         ax.set_ylabel('Votes')
#         ax.set_title(f'{position} Results')
#         plt.xticks(rotation=15, ha='right', fontsize=9)
#         plt.tight_layout()
        
#         st.pyplot(fig)
#         plt.close(fig)  # Close to free memory

# def authenticate_user(email, password):
#     """Authenticate user with email and password"""
#     if st.session_state.voter_df.empty:
#         return False, "No voter data available"
    
#     # Check if email exists
#     email_exists = (st.session_state.voter_df['Email'].str.lower() == email.lower()).any()
    
#     if not email_exists:
#         return False, "Email not found in voter database"
    
#     # Get user record
#     user_record = st.session_state.voter_df[st.session_state.voter_df['Email'].str.lower() == email.lower()].iloc[0]
    
#     # Verify password
#     if user_record['Password'] != password:
#         return False, "Incorrect password"
    
#     # Check if already voted
#     if has_already_voted(email) or has_already_voted(user_record['Mat Number']):
#         return False, "You have already voted"
    
#     return True, user_record

# def voting_section():
#     """Voting section content"""
#     # Authentication section
#     if not st.session_state.authenticated:
#         st.header("Voter Authentication")
        
#         # Toggle between login and password recovery
#         col1, col2 = st.columns([3, 1])
#         with col2:
#             if st.button("Forgot Password?"):
#                 st.session_state.show_password_recovery = not st.session_state.show_password_recovery
#                 st.rerun()
        
#         if st.session_state.show_password_recovery:
#             # Password Recovery Section
#             st.subheader("Password Recovery")
#             st.info("Enter your email address to receive your password")
            
#             recovery_email = st.text_input("Email Address:", key="recovery_email").strip().lower()
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("Send Password"):
#                     if not recovery_email:
#                         st.error("Please enter your email address")
#                     else:
#                         # Check if email exists in database
#                         if st.session_state.voter_df.empty:
#                             st.error("Voter database not available")
#                         else:
#                             user_match = st.session_state.voter_df[
#                                 st.session_state.voter_df['Email'].str.lower() == recovery_email
#                             ]
                            
#                             if user_match.empty:
#                                 st.error("Email not found in voter database")
#                             else:
#                                 user_record = user_match.iloc[0]
#                                 name = user_record.get('Full Name', 'Student')
#                                 password = user_record['Password']
                                
#                                 # Try to send email
#                                 if send_password_email(recovery_email, password, name):
#                                     st.success("Password sent to your email address!")
#                                     st.info("Please check your email and return to login")
#                                 else:
#                                     st.error("Failed to send email. Please contact the administrator.")
#                                     # Show password directly if email fails
#                                     st.warning(f"Your password is: **{password}**")
            
#             with col2:
#                 if st.button("Back to Login"):
#                     st.session_state.show_password_recovery = False
#                     st.rerun()
        
#         else:
#             # Login Section
#             st.subheader("Login with Email")
#             email = st.text_input("Email Address:").strip().lower()
#             password = st.text_input("Password:", type="password")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("Login"):
#                     if not email or not password:
#                         st.error("Please enter both email and password")
#                     else:
#                         success, result = authenticate_user(email, password)
#                         if success:
#                             st.session_state.authenticated = True
#                             st.session_state.current_user = email
#                             st.session_state.current_user_record = result
#                             st.session_state.login_time = datetime.now()  # Set login time
#                             st.success(f"Welcome, {result.get('Full Name', 'Student')}!")
#                             st.rerun()
#                         else:
#                             st.error(result)
            
#             with col2:
#                 if st.button("Admin Login"):
#                     admin_pass = st.text_input("Admin Password:", type="password", key="admin_pass")
#                     if admin_pass == "X9@2&!p":
#                         st.session_state.authenticated = True
#                         st.session_state.is_admin = True
#                         st.session_state.admin_sidebar_visible = True
#                         st.session_state.login_time = datetime.now()  # Set login time for admin
#                         st.rerun()
#                     elif admin_pass:  # Only show error if password was entered
#                         st.error("Invalid admin credentials")
    
#     # Voting section
#     else:
#         user = st.session_state.get('current_user', '')
        
#         if st.session_state.get('is_admin', False):
#             st.success("Logged in as Administrator")
#             if st.button("Logout"):
#                 logout_user()
        
#         elif has_already_voted(user):
#             st.success("✅ You have already voted. Thank you!")
            
#             # Auto-logout after voting if enabled
#             if AUTO_LOGOUT_AFTER_VOTING:
#                 st.info("You will be automatically logged out in 3 seconds...")
#                 time.sleep(3)
#                 logout_user("Automatically logged out after voting")
#             else:
#                 if st.button("Logout"):
#                     logout_user()
        
#         elif VOTING_START <= datetime.now() <= VOTING_END:
#             st.header("Cast Your Vote")
            
#             # Show user info
#             user_record = st.session_state.get('current_user_record', {})
#             if user_record is not None and not user_record.empty:
#                 st.info(f"Voting as: {user_record.get('Full Name', 'Student')} ({user_record.get('Mat Number', 'N/A')})")
            
#             # Voting form with no default values
#             pres = st.radio("President:", ['Prince John ANIGBO', 'Covenant Olamigoke OLOWO'], index=None)
#             vp = st.radio("Vice President:", ['Esther OGUNLEYE', 'Hafsoh K. OGUNNIYI'], index=None)
#             gs = st.radio("General Secretary:", ['Churchill OLISA'], index=None)
#             ags = st.radio("Assistant General Secretary:", ['Frankcleave KASIMANWUNA', 'Ajiserere ODUFISAN', 'George IHEKWABA'], index=None)
#             fs = st.radio("Financial Secretary:", ['F\'eyisayo OLATUNJI'], index=None)
#             tre = st.radio("Treasurer:", ['Okikiimole AKINDUSOYE', 'Pipolooluwa AYO-PONLE'], index=None)
#             pro = st.radio("PRO:", ['Jocl ATUH', 'Steaadfast ILEOGBEN', 'Victor Folahanmi AKILO', 'Enoch OGUNTOYE'], index=None)
#             sport = st.radio("Sports Secretary:", ['Nasirudeen Adeshina ALABI', 'Ireoluwa OKE'], index=None)
#             welfare = st.radio("Welfare Secretary:", ['Oluwadunmininu IDOWU', 'Simbiat O. ADUMADEYIN', 'Olamiposi latcefat RAJI'], index=None)
#             social = st.radio("Social Secretary:", ['Oluwagbotemi Fatiu ADEBAYO', 'Vivian AGWOILE'], index=None)

#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("Submit Vote"):
#                     # Check if all positions have been voted for
#                     if None in [pres, vp, gs, ags, fs, tre, pro, sport, welfare, social]:
#                         st.error("Please vote for all positions before submitting")
#                     else:
#                         # Update votes for all positions
#                         st.session_state.votes['President'][pres] += 1
#                         st.session_state.votes['Vice President'][vp] += 1
#                         st.session_state.votes['General Secretary'][gs] += 1
#                         st.session_state.votes['Assist. General Secretary'][ags] += 1
#                         st.session_state.votes['Financial Secretary'][fs] += 1
#                         st.session_state.votes['Treasurer'][tre] += 1
#                         st.session_state.votes['PRO'][pro] += 1
#                         st.session_state.votes['Sports Secretary'][sport] += 1
#                         st.session_state.votes['Welfare Secretary'][welfare] += 1
#                         st.session_state.votes['Social Secretary'][social] += 1
                        
#                         # Mark as voted (use both email and mat number to prevent duplicate voting)
#                         st.session_state.voted.add(user)  # email
#                         user_record = st.session_state.get('current_user_record', {})
#                         if user_record is not None and not user_record.empty:
#                             st.session_state.voted.add(user_record.get('Mat Number', ''))
                        
#                         # Auto-save results after each vote
#                         save_results()
                        
#                         st.success("✅ Vote submitted successfully!")
                        
#                         # Auto-logout after voting if enabled
#                         if AUTO_LOGOUT_AFTER_VOTING:
#                             st.info("Thank you for voting! You will be automatically logged out in 3 seconds...")
#                             time.sleep(3)
#                             logout_user("Automatically logged out after voting")
#                         else:
#                             st.rerun()

#             with col2:
#                 if st.button("Logout"):
#                     logout_user()
#         else:
#             st.warning("Voting is currently closed.")

# def results_section():
#     """Results section content - Admin only"""
#     st.header("Election Results - Admin View")
#     st.info("🔒 Results are only visible to administrators")
#     display_results()

# # --- Initialize Session State ---
# if 'voter_df' not in st.session_state:
#     st.session_state.voter_df = load_voter_data()
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'voted' not in st.session_state:
#     st.session_state.voted = set()
# if 'votes' not in st.session_state:
#     st.session_state.votes = {
#         'President': {'Prince John ANIGBO': 0, 'Covenant Olamigoke OLOWO': 0},
#         'Vice President': {'Esther OGUNLEYE': 0, 'Hafsoh K. OGUNNIYI': 0},
#         'General Secretary': {'Churchill OLISA': 0},
#         'Assist. General Secretary': {'Frankcleave KASIMANWUNA': 0, 'Ajiserere ODUFISAN': 0, 'George IHEKWABA': 0},
#         'Financial Secretary': {'F\'eyisayo OLATUNJI': 0},
#         'Treasurer': {'Okikiimole AKINDUSOYE': 0, 'Pipolooluwa AYO-PONLE': 0},
#         'PRO': {'Jocl ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
#         'Sports Secretary': {'Nasirudeen Adeshina ALABI': 0, 'Ireoluwa OKE': 0},
#         'Welfare Secretary': {'Oluwadunmininu IDOWU': 0, 'Simbiat O. ADUMADEYIN': 0, 'Olamiposi latcefat RAJI': 0},
#         'Social Secretary': {'Oluwagbotemi Fatiu ADEBAYO': 0, 'Vivian AGWOILE': 0}
#     }
# if 'admin_sidebar_visible' not in st.session_state:
#     st.session_state.admin_sidebar_visible = False
# if 'show_password_recovery' not in st.session_state:
#     st.session_state.show_password_recovery = False

# # --- Check for Session Timeout ---
# if st.session_state.authenticated and check_session_timeout():
#     logout_user("Session expired after 5 minutes of inactivity")

# # --- App UI ---
# st.title("BellsTech's Student Voting System")

# # --- Session Status Display ---
# if st.session_state.authenticated and not st.session_state.get('is_admin', False):
#     remaining_time = get_session_time_remaining()
#     if remaining_time > 0:
#         st.info(f"⏱️ Session expires in {remaining_time} minute(s)")
        
#         # Auto-refresh to check session timeout
#         if remaining_time <= 1:  # Warning when less than 1 minute left
#             st.warning("⚠️ Your session will expire soon!")
#     else:
#         logout_user("Session expired")

# # --- Admin Sidebar Access ---
# if st.session_state.get('is_admin', False):
#     admin_sidebar = st.sidebar.container()
    
#     if not st.session_state.admin_sidebar_visible:
#         if admin_sidebar.button("Show Admin Panel"):
#             st.session_state.admin_sidebar_visible = True
#             st.rerun()
#     else:
#         admin_sidebar.title("Results Management")
        
#         # Load results button
#         if admin_sidebar.button("🔄 Load Saved Results"):
#             load_saved_results()

#         # Save results option
#         if admin_sidebar.button("💾 Save Results Now"):
#             results_df = save_results()
#             admin_sidebar.success("Results saved successfully to:")
#             admin_sidebar.info("- election_results.json\n- election_results.csv\n- voted_students.csv")
#             admin_sidebar.dataframe(results_df)

#         # Excel export button
#         if admin_sidebar.button("📊 Export to Excel"):
#             excel_data = export_excel()
#             admin_sidebar.download_button(
#                 label="📥 Download Excel File",
#                 data=excel_data,
#                 file_name=f"election_results_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )
        
#         # Hide sidebar button
#         if admin_sidebar.button("Hide Admin Panel"):
#             st.session_state.admin_sidebar_visible = False
#             st.rerun()

# # --- Voting Time Check ---
# now = datetime.now()
# if now < VOTING_START:
#     time_left = VOTING_START - now
#     st.warning(f"🕒 Voting has not started yet. It begins in {str(time_left).split('.')[0]}")
# elif now > VOTING_END:
#     st.info("🏁 Voting period has ended.")
# else:
#     time_left = VOTING_END - now
#     st.info(f"⏳ Time remaining: {str(time_left).split('.')[0]}")

# # --- Main Application Logic ---
# if st.session_state.get('is_admin', False):
#     # Admin sees both tabs
#     tab1, tab2 = st.tabs(["Voting", "Results"])
    
#     with tab1:
#         voting_section()
    
#     with tab2:
#         results_section()
# else:
#     # Regular users only see voting section
#     voting_section()

# # --- Instructions for Setup ---
# if st.session_state.voter_df.empty:
#     st.error("⚠️ Setup Required")
#     st.markdown("""
#     ### Setup Instructions:
    
#     1. **Create votersdetails.csv** with the following columns:
#        - `Mat Number`: Student matriculation number
#        - `Password`: Student password
#        - `Email`: Student email address
#        - `Full Name`: Student full name (optional)
    
#     2. **Configure Email Settings** (in EMAIL_CONFIG):
#        - Update `sender_email` with your email
#        - Update `sender_password` with your app password
#        - Update `smtp_server` if not using Gmail
    
#     3. **For Gmail users:**
#        - Enable 2-factor authentication
#        - Generate an app password for this application
#        - Use the app password, not your regular password
    
#     4. **Auto-logout Settings:**
#        - Users are automatically logged out after 5 minutes of login
#        - Users are automatically logged out immediately after voting
#        - Session timeout and auto-logout can be configured at the top of the script
    
#     5. **Admin Access:**
#        - Only administrators can view election results
#        - Regular students cannot see the Results tab
#        - Results are completely hidden from non-admin users
    
#     Example CSV format:
#     ```
#     Mat Number,Password,Email,Full Name
#     STU001,pass123,student1@university.edu,John Doe
#     STU002,pass456,student2@university.edu,Jane Smith
#     ```
#     """)

# # --- Auto-refresh for session management ---
# if st.session_state.authenticated:
#     # Add a small delay to allow for proper session timeout checking
#     time.sleep(0.1)

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
import time


# --- Voting Time Settings ---
VOTING_START = datetime(2025, 5, 23, 9, 30, 0)  # 9:00 AM
VOTING_END = datetime(2025, 5, 23, 14, 30, 0)   # 12:00 PM

# --- Auto-logout Settings ---
SESSION_TIMEOUT_MINUTES = 5  # Auto-logout after 5 minutes
AUTO_LOGOUT_AFTER_VOTING = True  # Auto-logout after voting

# --- Email Configuration (Update these with your email settings) ---
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change to your SMTP server
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',  # Change to your email
    'sender_password': 'your_app_password',  # Use app password for Gmail
}

# --- Session Management Functions ---
def check_session_timeout():
    """Check if user session has timed out"""
    if not st.session_state.authenticated:
        return False
    
    if 'login_time' not in st.session_state:
        return False
    
    # Calculate time elapsed since login
    current_time = datetime.now()
    time_elapsed = current_time - st.session_state.login_time
    
    # Check if session has expired (5 minutes)
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
    
    # Clear login time
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    
    if reason:
        st.warning(f"You have been logged out: {reason}")
    
    st.rerun()

def update_last_activity():
    """Update the last activity time"""
    st.session_state.last_activity = datetime.now()

def get_session_time_remaining():
    """Get remaining session time in minutes"""
    if 'login_time' not in st.session_state:
        return 0
    
    elapsed = datetime.now() - st.session_state.login_time
    remaining = timedelta(minutes=SESSION_TIMEOUT_MINUTES) - elapsed
    
    if remaining.total_seconds() <= 0:
        return 0
    
    return int(remaining.total_seconds() / 60)

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
        # Ensure required columns exist
        required_columns = ['Mat Number', 'Password', 'Email']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns in votersdetails.csv: {', '.join(missing_columns)}")
            st.info("Please ensure your CSV has columns: Mat Number, Password, Email, and optionally Full Name")
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
    
    # Also save as CSV for easy analysis
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
    #col2.metric("Total Votes Cast", f"{voted_count} ({(voted_count / total_voters * 100) if total_voters else 0:.1f}%)")
    
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

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    if st.session_state.voter_df.empty:
        return False, "No voter data available"
    
    # Check if email exists
    email_exists = (st.session_state.voter_df['Email'].str.lower() == email.lower()).any()
    
    if not email_exists:
        return False, "Email not found in voter database"
    
    # Get user record
    user_record = st.session_state.voter_df[st.session_state.voter_df['Email'].str.lower() == email.lower()].iloc[0]
    
    # Verify password
    if user_record['Password'] != password:
        return False, "Incorrect password"
    
    # Check if already voted
    if has_already_voted(email) or has_already_voted(user_record['Mat Number']):
        return False, "You have already voted"
    
    return True, user_record

def voting_section():
    """Voting section content"""
    # Authentication section
    if not st.session_state.authenticated:
        st.header("Voter Authentication")
        
        # Toggle between login and password recovery
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
                        # Check if email exists in database
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
                                
                                # Try to send email
                                if send_password_email(recovery_email, password, name):
                                    st.success("Password sent to your email address!")
                                    st.info("Please check your email and return to login")
                                else:
                                    st.error("Failed to send email. Please contact the administrator.")
                                    # Show password directly if email fails
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
                            st.session_state.login_time = datetime.now()  # Set login time
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
                        st.session_state.login_time = datetime.now()  # Set login time for admin
                        st.rerun()
                    elif admin_pass:  # Only show error if password was entered
                        st.error("Invalid admin credentials")
    
    # Voting section
    else:
        user = st.session_state.get('current_user', '')
        
        if st.session_state.get('is_admin', False):
            st.success("Logged in as Administrator")
            if st.button("Logout"):
                logout_user()
        
        elif has_already_voted(user):
            st.success("✅ You have already voted. Thank you!")
            
            # Auto-logout after voting if enabled
            if AUTO_LOGOUT_AFTER_VOTING:
                st.info("You will be automatically logged out in 3 seconds...")
                time.sleep(3)
                logout_user("Automatically logged out after voting")
            else:
                if st.button("Logout"):
                    logout_user()
        
        elif VOTING_START <= datetime.now() <= VOTING_END:
            st.header("Cast Your Vote")
            
            # Show user info
            user_record = st.session_state.get('current_user_record', {})
            if user_record is not None and not user_record.empty:
                st.info(f"Voting as: {user_record.get('Full Name', 'Student')} ({user_record.get('Mat Number', 'N/A')})")
            
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
                        
                        # Mark as voted (use both email and mat number to prevent duplicate voting)
                        st.session_state.voted.add(user)  # email
                        user_record = st.session_state.get('current_user_record', {})
                        if user_record is not None and not user_record.empty:
                            st.session_state.voted.add(user_record.get('Mat Number', ''))
                        
                        # Auto-save results after each vote
                        save_results()
                        
                        st.success("✅ Vote submitted successfully!")
                        
                        # Auto-logout after voting if enabled
                        if AUTO_LOGOUT_AFTER_VOTING:
                            st.info("Thank you for voting! You will be automatically logged out in 3 seconds...")
                            time.sleep(3)
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
        'Treasurer': {'Okikiimole AKINDUSOYE': 0, 'Pipolooluwa AYO-PONLE': 0},
        'PRO': {'Jocl ATUH': 0, 'Steaadfast ILEOGBEN': 0, 'Victor Folahanmi AKILO': 0, 'Enoch OGUNTOYE': 0},
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
        
        # Auto-refresh to check session timeout
        if remaining_time <= 1:  # Warning when less than 1 minute left
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
        
        # Load results button
        if admin_sidebar.button("🔄 Load Saved Results"):
            load_saved_results()

        # Save results option
        if admin_sidebar.button("💾 Save Results Now"):
            results_df = save_results()
            admin_sidebar.success("Results saved successfully to:")
            admin_sidebar.info("- election_results.json\n- election_results.csv\n- voted_students.csv")
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

# --- Main Application Logic ---
if st.session_state.get('is_admin', False):
    # Admin sees both tabs
    tab1, tab2 = st.tabs(["Voting", "Results"])
    
    with tab1:
        voting_section()
    
    with tab2:
        results_section()
else:
    # Regular users only see voting section
    voting_section()

# --- Instructions for Setup ---
if st.session_state.voter_df.empty:
    st.error("⚠️ Setup Required")
    st.markdown("""
    ### Setup Instructions:
    
    1. **Create votersdetails.csv** with the following columns:
       - `Mat Number`: Student matriculation number
       - `Password`: Student password
       - `Email`: Student email address
       - `Full Name`: Student full name (optional)
    
    2. **Configure Email Settings** (in EMAIL_CONFIG):
       - Update `sender_email` with your email
       - Update `sender_password` with your app password
       - Update `smtp_server` if not using Gmail
    
    3. **For Gmail users:**
       - Enable 2-factor authentication
       - Generate an app password for this application
       - Use the app password, not your regular password
    
    4. **Auto-logout Settings:**
       - Users are automatically logged out after 5 minutes of login
       - Users are automatically logged out immediately after voting
       - Session timeout and auto-logout can be configured at the top of the script
    
    5. **Admin Access:**
       - Only administrators can view election results
       - Regular students cannot see the Results tab
       - Results are completely hidden from non-admin users
    
    Example CSV format:
    ```
    Mat Number,Password,Email,Full Name
    STU001,pass123,student1@university.edu,John Doe
    STU002,pass456,student2@university.edu,Jane Smith
    ```
    """)

# --- Auto-refresh for session management ---
if st.session_state.authenticated:
    # Add a small delay to allow for proper session timeout checking
    time.sleep(0.1)