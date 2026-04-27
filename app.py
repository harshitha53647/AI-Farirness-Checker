import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_fairness_metrics(group_data):
    values = group_data.values

    max_val = values.max()
    min_val = values.min()

    # Demographic Parity Difference
    dpd = max_val - min_val

    # Disparate Impact Ratio
    if max_val != 0:
        dir_ratio = min_val / max_val
    else:
        dir_ratio = 0

    # Equal Opportunity (simple approximation)
    eo = 1 - dpd

    return {
        "DPD": dpd,
        "DIR": dir_ratio,
        "EO": eo
    }

st.markdown("""
<style>

/* Remove top spacing */
.block-container {
    padding-top: 1rem !important;
}

/* Hide header completely */
header[data-testid="stHeader"] {
    display: none;
}

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f3e5f5, #e1bee7);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Buttons styling */
.stButton > button {
    background-color: #7b1fa2;
    color: white;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: bold;
    border: none;
}

/* Hover effect */
.stButton > button:hover {
    background-color: #4a148c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Fairness Checker",layout="wide")

st.markdown("""
<style>
header[data-testid="stHeader"] {display:none;}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #f3e5f5, #e1bee7);
}
</style>
""", unsafe_allow_html=True)

# ---------------- NEW WELCOME STATE ----------------
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "welcome"


# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "users" not in st.session_state:
    st.session_state.users = {"admin": "FairAI@2026"}

# ---------------- WELCOME PAGE ----------------
def welcome_page():

    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100%;
    }

    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 0rem !important;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    .welcome-box {
        text-align: center;
        background: rgba(255,255,255,0.55);
        padding: 40px;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-box">
        <h1 style="color:#6a1b9a;">⚖️ Welcome to AI Fairness Analyzer</h1>
        <h4 style="color:#4a148c;">
        Detect Bias • Visualize Impact • Improve Fairness
        </h4>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("🚀 Get Started"):
            st.session_state.auth_page = "login"
            st.rerun()

#----------------- LOGIN PAGE ----------------
def login_page():

    st.markdown("""
    <style>
    html, body,
    [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
    }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([5,1])

    with col1:
        st.markdown("### ⚖️ AI Fairness Analyzer")

    with col2:
        if st.button("Sign Up", key="top_signup"):
            st.session_state.auth_page = "signup"
            st.rerun()

    st.markdown("### 🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="login_btn"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Forgot Password", key="forgot_btn"):
        st.session_state.auth_page = "forgot"
        st.rerun()

    # ---------------- SIGNUP PAGE ----------------
def signup_page():

    st.markdown("### 📝 Sign Up")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    import re

    if st.button("Register", key="register_btn"):

        if new_user == "" or new_pass == "":
            st.warning("Enter username and password")

        elif new_user in st.session_state.users:
            st.error("Username already exists")

        elif len(new_pass) < 8:
            st.error("Password must be at least 8 characters")

        elif not re.search("[A-Z]", new_pass):
            st.error("Password must contain at least 1 uppercase letter")

        elif not re.search("[a-z]", new_pass):
            st.error("Password must contain at least 1 lowercase letter")

        elif not re.search("[0-9]", new_pass):
            st.error("Password must contain at least 1 number")

        elif not re.search("[@#$%&*!]", new_pass):
            st.error("Password must contain at least 1 special character (@#$%&*!)")

        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created successfully!")
            st.session_state.auth_page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.auth_page = "login"
        st.rerun()

    # ---------------- FORGOT PASSWORD PAGE ----------------
def forgot_page():

    st.markdown("### 🔑 Reset Password")

    user = st.text_input("Enter Username")
    new_pass = st.text_input("New Password", type="password")

    import re

    if st.button("Reset Password", key="reset_btn"):

        if user == "" or new_pass == "":
            st.warning("Enter username and new password")

        elif user not in st.session_state.users:
            st.error("Username not found")

        elif len(new_pass) < 8:
            st.error("Password must be at least 8 characters")

        elif not re.search("[A-Z]", new_pass):
            st.error("Password must contain at least 1 uppercase letter")

        elif not re.search("[a-z]", new_pass):
            st.error("Password must contain at least 1 lowercase letter")

        elif not re.search("[0-9]", new_pass):
            st.error("Password must contain at least 1 number")

        elif not re.search("[@#$%&*!]", new_pass):
            st.error("Password must contain at least 1 special character (@#$%&*!)")

        else:
            st.session_state.users[user] = new_pass
            st.success("Password reset successful!")
            st.session_state.auth_page = "login"
            st.rerun()

    if st.button("Back to Login"):
        st.session_state.auth_page = "login"
        st.rerun()
# ---------------- UI ----------------
def main_app():

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    if "bias_checked" not in st.session_state:
        st.session_state.bias_checked = False

    st.sidebar.title("Navigate")

    if st.sidebar.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.sidebar.button("📄 Report"):
        st.session_state.page = "Report"
        st.rerun()

    if st.sidebar.button("ℹ️ About"):
        st.session_state.page = "About"
        st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", key="nav_logout"):
        st.session_state.logged_in = False
        st.session_state.auth_page = "login"
        st.session_state.page = "Dashboard"
        st.rerun()

    st.sidebar.markdown("""
    <style>

    /* Slightly light purple, but not too pale */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #e9ddf3, #dcc6ee);
    }

    /* Title */
    section[data-testid="stSidebar"] h1 {
        color: #5e2a91;
        font-size: 22px;
        font-weight: bold;
    }

    /* Buttons */
    section[data-testid="stSidebar"] button {
        background-color: #7b1fa2;
        color: white;
        border-radius: 12px;
        padding: 10px;
        font-weight: 600;
        border: none;
        margin-bottom: 10px;
        width: 100%;
    }

    /* Hover */
    section[data-testid="stSidebar"] button:hover {
        background-color: #5e2a91;
    }

    /* Divider */
    section[data-testid="stSidebar"] hr {
        border-color: #c7b0e3;
        opacity: 0.7;
    }

    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <style>

    /* Prevent sidebar scrolling */
    section[data-testid="stSidebar"] {
        overflow: hidden !important;
    }

    /* Make sidebar content fit full height */
    section[data-testid="stSidebar"] > div {
        height: 100vh;
        overflow: hidden !important;
    }

    /* Optional: keep buttons stacked nicely */
    section[data-testid="stSidebar"] button {
        flex-shrink: 0;
    }

    </style>
    """, unsafe_allow_html=True)
        
    if st.session_state.page == "Dashboard":

        st.title("📊 AI Fairness Dashboard")
        st.markdown("<h1>⚖️ AI Fairness Analyzer</h1>", unsafe_allow_html=True)
        st.markdown("### Detect Bias • Visualize Impact • Improve Fairness")

# ---------------- FILE UPLOAD ----------------
        file = st.file_uploader("📂 Upload CSV file", type=["csv"])

        if file:
            df = pd.read_csv(file)

            st.subheader("📊 Dataset Preview")
            st.dataframe(df.head())

        # ---------------- COLUMN SELECTION ----------------
            st.subheader("⚙️ Select Columns")
            # AUTO DETECT SENSITIVE COLUMN
            st.subheader("🤖 Auto Detect Sensitive Column")

            suggested = None
            keywords = ["gender", "sex", "age", "race"]

            for col in df.columns:
                for key in keywords:
                    if key in col.lower():
                        suggested = col

            if suggested:
                st.success(f"Suggested Sensitive Column: {suggested}")
            target = st.selectbox("Target Column (0/1)", df.columns)
            sensitive = st.selectbox("Sensitive Column (gender, etc)", df.columns)

            # ================= MULTI-SENSITIVE =================
            st.subheader("👥 Multi-Sensitive Analysis")

            multi_sensitive = st.multiselect(
                "Select Multiple Sensitive Columns",
                df.columns
            )
        # ---------------- BIAS CHECK ----------------
            if st.button("🔍 Check Bias"):
                st.session_state.bias_checked = True

            if st.session_state.get("bias_checked", False):
                # Convert target column safely
                df[target] = pd.to_numeric(df[target], errors='coerce')

                # Clean null values
                df_clean = df.dropna(subset=[target, sensitive])

                # STOP if empty
                if df_clean.empty:
                    st.error("No valid data after cleaning")
                    st.stop()

                # CREATE group_data FIRST
                group_data = df_clean.groupby(sensitive)[target].mean()

                # STOP if no groups
                if group_data.empty:
                    st.error("No group data found")
                    st.stop()

                # MULTI-SENSITIVE ANALYSIS
                if len(multi_sensitive) > 1:
                    combined = df[multi_sensitive].astype(str).agg("_".join, axis=1)
                    multi_group = df.groupby(combined)[target].mean()

                    st.subheader("👥 Intersectional Bias (Multi-Sensitive)")
                    st.write(multi_group)

                    # Better Multi-Sensitive Graph
                    fig_multi, ax_multi = plt.subplots(figsize=(12,7))

                    multi_group.sort_values().plot(
                        kind='barh',
                        ax=ax_multi
                    )

                    ax_multi.set_title("👥 Multi-Sensitive Bias Analysis", fontsize=16, fontweight='bold')
                    ax_multi.set_xlabel("Average Outcome", fontsize=12)
                    ax_multi.set_ylabel("Groups", fontsize=12)

                    ax_multi.tick_params(axis='y', labelsize=10)
                    ax_multi.grid(axis='x', linestyle='--', alpha=0.4)

                    plt.tight_layout()
                    st.pyplot(fig_multi)
                # ---------------- GRAPH ----------------
                st.subheader("📊 Bias Visualization")
                fig, ax = plt.subplots()
                group_data.plot(kind='bar', ax=ax)
                ax.set_ylabel("Average Outcome")
                ax.set_title("Outcome by Group")
                st.pyplot(fig)

                # ---------------- BIAS SCORE ----------------
                dpd = group_data.max() - group_data.min()

                # ================= FAIRNESS SCORE =================
                fairness_score_simple = (1 - dpd) * 100

                st.subheader("⚖️ Bias Score")
                # KPI METRICS
                metrics = calculate_fairness_metrics(group_data)

                # ================= UI CARDS  =================
                st.markdown("""
                <style>
                .metric-card {
                    background-color: rgba(255,255,255,0.75);
                    padding: 10px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 1px 1px 6px rgba(0,0,0,0.08);
                    margin-bottom: 10px;
                }

                .metric-title {
                    font-size: 18px;
                    color: #6a1b9a;
                    font-weight: bold;
                    margin-bottom: 8px;
                }

                .metric-value {
                    font-size: 34px;
                    font-weight: bold;
                    color: #4a148c;
                }
                </style>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-title'>⚖️ Bias</div>
                        <div class='metric-value'>{dpd:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-title'>🎯 Fairness</div>
                        <div class='metric-value'>{fairness_score_simple:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-title'>👥 Groups</div>
                        <div class='metric-value'>{len(group_data)}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # ================= UI CARD FOR FAIRNESS METRICS =================

                st.subheader("📊 Key Fairness Metrics")

                st.markdown("""
                <style>
                .metric-card {
                    background: linear-gradient(to right, #ffffff, #f3e5f5);
                    padding: 22px;
                    border-radius: 18px;
                    text-align: center;
                    height: 150px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
                    border: 1px solid #e1bee7;
                }

                .metric-title {
                    font-size: 18px;
                    font-weight: 600;
                    color: #6a1b9a;
                    margin-bottom: 10px;
                }

                .metric-value {
                    font-size: 34px;
                    font-weight: bold;
                    color: #4a148c;
                }
                </style>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">⚖️ DPD (Bias Gap)</div>
                        <div class="metric-value">{metrics['DPD']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">📉 Disparate Impact</div>
                        <div class="metric-value">{metrics['DIR']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">🎯 Equal Opportunity</div>
                        <div class="metric-value">{metrics['EO']:.3f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ---------------- INTERPRETATION ----------------
                if dpd > 0.2:
                    st.error("🔴 High Bias Detected")
                elif dpd > 0.1:
                    st.warning("🟡 Moderate Bias Detected")
                else:
                    st.success("🟢 Low / No Bias")

                # ---------------- SUGGESTIONS ----------------
                st.subheader("💡 Suggestions")

                if dpd > 0.1:
                    st.write("- Balance the dataset across groups")
                    st.write("- Remove sensitive attributes (like gender)")
                    st.write("- Collect more diverse data")
                    st.write("- Use fairness-aware ML models")
                else:
                    st.write("Dataset looks fairly balanced")

                # ================= BEFORE VS AFTER =================
                st.subheader("🛠️ Before vs After Bias Comparison")

                # ================= SAFE BEFORE + AFTER =================

                if file is not None:
        # ---------- CLEAN DATA ----------
                    df[target] = pd.to_numeric(df[target], errors='coerce')
                    df_clean = df.dropna(subset=[target,sensitive])

            # ---------- BEFORE ----------
                if df_clean.empty:
                    st.stop()
                before_group = df_clean.groupby(sensitive)[target].mean()
                if before_group.empty:
                
                    st.stop()
                before_bias = before_group.max() - before_group.min()

                lowest_group = before_group.idxmin()
                st.warning(f"⚠️ Most affected group: {lowest_group}")

            # ---------- AFTER FIX ----------
                df_fixed = df.copy()
                df_fixed[target] = df_fixed[target].astype(float)

            # convert safely
                df_fixed[target] = pd.to_numeric(df_fixed[target], errors='coerce')

                group_means = df.groupby(sensitive)[target].mean()
                overall_mean = df[target].mean()

                for group in group_means.index:
                    diff = overall_mean - group_means[group]
                    mask = df_fixed[sensitive] == group
                    df_fixed.loc[mask, target] = df_fixed.loc[mask, target].astype(float) + diff

                df_fixed[target] = df_fixed[target].clip(0, 1)

            # ---------- AFTER ----------
                after_group = df_fixed.groupby(sensitive)[target].mean()
                if after_group.empty:
                    st.error("❌ Error in bias correction step")
                    st.stop()
                after_bias = after_group.max() - after_group.min()

                fairness_score = (1 - after_bias) * 100

                st.subheader("🎯 Fairness Score")
                # ================= FAIRNESS SCORE CARD =================
                st.markdown("""
                <style>
                .fair-card {
                    background: linear-gradient(135deg, #7b1fa2, #ba68c8);
                    padding: 18px;
                    border-radius: 16px;
                    text-align: center;
                    color: white;
                    box-shadow: 0px 5px 12px rgba(0,0,0,0.12);
                    margin-top: 0px;
                    margin-bottom: 10px;
                    width: 240px;
                    margin-left: 0px;
                    margin-right: auto;
                }
                .fair-title {
                    font-size: 16px;
                    font-weight: bold;
                }
                .fair-score {
                    font-size: 28px;
                    font-weight: 800;
                    margin-top: 6px;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="fair-card">
                    <div class="fair-title">🎯Fairness Score</div>
                    <div class="fair-score">{fairness_score_simple:.1f}/100</div>
                </div>
                """, unsafe_allow_html=True)
            # ---------- SAFETY CHECK ----------
                if pd.isna(before_bias) or pd.isna(after_bias):
                    st.error("⚠️ Data issue: Check your columns")
                    st.stop()

            # ================= BEFORE / AFTER UI CARDS =================
                st.subheader("⚖️ Bias Comparison")

                st.markdown("""
                <style>
                .small-card {
                    background: linear-gradient(to right, #ffffff, #f3e5f5);
                    padding: 12px;
                    border-radius: 12px;
                    text-align: center;
                    width: 180px;
                    margin: auto;
                    margin-bottom: 10px;

                    /* Strong beautiful shadow */
                    box-shadow: 0px 8px 20px rgba(0,0,0,0.18);

                    /* Smooth hover effect */
                    transition: 0.3s ease-in-out;
                }

                .small-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0px 12px 28px rgba(0,0,0,0.25);
                }

                .small-card h3 {
                    font-size: 16px;
                    margin-bottom: 5px;
                    color: #555;
                }

                .small-card h2 {
                    font-size: 24px;
                    margin: 0;
                }
                </style>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"""
                    <div class="small-card">
                        <h3>Before Bias</h3>
                        <h2 style='color:red;'>{before_bias:.3f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="small-card">
                        <h3>After Bias</h3>
                        <h2 style='color:green;'>{after_bias:.3f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                # ---------- GRAPHS ----------
                fig_bar, ax_bar = plt.subplots()

                df_compare = pd.DataFrame({
                    "Before": before_group,
                    "After": after_group
                })

                df_compare.plot(kind='bar', ax=ax_bar)

                ax_bar.set_title("Before vs After Bias")
                ax_bar.set_ylabel("Average Outcome")

                # ✅ SAVE THIS (MAIN CHART)
                fig_bar.savefig("comparison_bar.png", dpi=150, bbox_inches='tight')

                st.pyplot(fig_bar)

            # --------Line Chart Comparision--------
                st.subheader("📈 Bias Comparison Trend")

                comparison_df = pd.DataFrame({
                    "Before": before_group,
                    "After": after_group
                })

                # ✅ CREATE ONE CHART
                fig_line, ax_line = plt.subplots()
                comparison_df.plot(ax=ax_line)

                ax_line.set_title("Bias Trend")
                ax_line.set_ylabel("Average Outcome")

                # ✅ SAVE FOR REPORT + PDF
                fig_line.savefig("line_chart.png", dpi=150, bbox_inches='tight')

                # ✅ SHOW IN DASHBOARD
                st.pyplot(fig_line)

                # ================= PIE CHART =================
                st.subheader("🥧 Distribution Before vs After")

                col1, col2 = st.columns(2)

                # BEFORE PIE
                fig3, ax3 = plt.subplots()
                before_group.plot(kind='pie', autopct='%1.1f%%', ax=ax3)
                ax3.set_ylabel("")
                ax3.set_title("Before Distribution")

                # AFTER PIE
                fig4, ax4 = plt.subplots()
                after_group.plot(kind='pie', autopct='%1.1f%%', ax=ax4)
                ax4.set_ylabel("")
                ax4.set_title("After Distribution")

                fig3.savefig("before_pie.png", dpi=150, bbox_inches='tight')
                fig4.savefig("after_pie.png", dpi=150, bbox_inches='tight')

                with col1:
                    st.pyplot(fig3)

                with col2:
                    st.pyplot(fig4)

                # ================= TRADEOFF GRAPH =================
                st.subheader("⚖️ Accuracy vs Fairness Tradeoff")

                # Simulated accuracy (since no ML model)
                accuracy_before = 0.85
                accuracy_after = accuracy_before - (before_bias - after_bias) * 0.2

                tradeoff_df = pd.DataFrame({
                    "Model": ["Before Fix", "After Fix"],
                    "Accuracy": [accuracy_before, accuracy_after],
                    "Fairness": [1 - before_bias, 1 - after_bias]
                })

                fig_trade, ax_trade = plt.subplots()

                ax_trade.plot(tradeoff_df["Model"], tradeoff_df["Accuracy"], marker='o', label="Accuracy")
                ax_trade.plot(tradeoff_df["Model"], tradeoff_df["Fairness"], marker='o', label="Fairness")

                ax_trade.set_title("Accuracy vs Fairness Tradeoff")
                ax_trade.legend()

                st.pyplot(fig_trade)

                # ---------- IMPROVEMENT ----------
                improvement = before_bias - after_bias

                if improvement > 0:
                    st.success(f"📉 Bias reduced by {improvement:.3f}")
                else:
                    st.warning("⚠️ No improvement detected")

                # ================= CHATBOT =================
                st.subheader("🤖 AI Fairness Chat Assistant")

                question = st.text_input(
                    "Ask anything about dataset / fairness / bias",
                    placeholder="Example: Why is fairness score low?"
                )

                if st.button("Ask AI", key="ask_ai_btn"):

                    if question.strip() == "":
                        st.warning("Please enter a question")

                    else:
                        q = question.lower()
                        answer = ""
                        # ================= GOOGLE GEMINI SECTION =================
                        st.subheader("🤖 Google Gemini AI Assistant")


                        st.write("Use Gemini for fairness explanations, recommendations, and AI guidance.")


                        st.link_button("Ask Gemini", "https://gemini.google.com")


                        # ================= FAIRNESS QUESTIONS =================
                        if "why is fairness score low" in q or "low fairness" in q:
                            answer = f"""
                        Fairness score is low because the bias gap (DPD) is {metrics['DPD']:.3f}.

                        This means some sensitive groups receive lower outcomes than others.
                        Try balancing the dataset or using fairness-aware methods.
                        """
                        elif "why is fairness score high" in q or "why fairness score high" in q:

                            if fairness_score_simple >= 90:
                                answer = f"""
                        Fairness score is high ({fairness_score_simple:.2f}%) because the bias gap (DPD) is very low at {metrics['DPD']:.3f}.

                        This means sensitive groups are receiving nearly equal outcomes, indicating a fair and balanced dataset.
                        """
                            elif fairness_score_simple >= 75:
                                answer = f"""
                        Fairness score is relatively good ({fairness_score_simple:.2f}%) because group outcome differences are limited.

                        The bias gap (DPD) is {metrics['DPD']:.3f}, showing only moderate imbalance.
                        """
                            else:
                                answer = f"""
                        Fairness score is {fairness_score_simple:.2f}%, which is not considered high.

                        There is still noticeable group disparity with DPD = {metrics['DPD']:.3f}.
                        """
                        # LEAST AFFECTED GROUP
                        elif "least affected group" in q or "best group" in q or "highest performing group" in q:

                            high_group = group_data.idxmax()
                            high_value = group_data.max()

                            answer = f"""
                        Least affected / best performing group is {high_group}.

                        This group has the highest average outcome of {high_value:.3f}, meaning it experienced the most favorable results.
                        """
                        elif "most affected group" in q:
                            answer = f"Most affected group: {group_data.idxmin()}"
                        
                        # HOW FAIRNESS SCORE IS CALCULATED
                        elif "how is fairness score calculated" in q or "calculate fairness score" in q:

                            answer = f"""
                        Fairness Score is calculated using:

                        Fairness Score = (1 - Bias Gap) × 100

                        Where Bias Gap = DPD = Max Group Outcome - Min Group Outcome

                        For your dataset:

                        DPD = {metrics['DPD']:.3f}

                        Fairness Score = (1 - {metrics['DPD']:.3f}) × 100 = {fairness_score_simple:.2f}%
                        """

                        # HOW TO IMPROVE FAIRNESS SCORE
                        elif "how to improve fairness score" in q or "improve fairness score" in q:

                            answer = """
                        To improve fairness score:

                        1. Balance the dataset across all groups
                        2. Add more underrepresented group data
                        3. Remove proxy sensitive features
                        4. Use fairness-aware machine learning models
                        5. Tune model thresholds equally
                        6. Monitor fairness regularly after training
                        """

                        elif "fairness score" in q:
                            answer = f"Fairness Score: {fairness_score_simple:.2f}%"

                        elif "what is dpd" in q or "define dpd" in q or "meaning of dpd" in q:

                            answer = f"""
                        DPD stands for Demographic Parity Difference.

                        It measures the difference between the highest and lowest group outcomes.

                        Formula:
                        DPD = Max Group Outcome - Min Group Outcome

                        For your dataset:
                        DPD = {metrics['DPD']:.3f}

                        Lower DPD is better because it means groups are treated more equally.
                        """
                        elif "what is demographic parity difference" in q:

                            answer = f"""
                        Demographic Parity Difference (DPD) measures fairness by comparing outcomes across sensitive groups.

                        A smaller value means fairer results.
                        Your current DPD is {metrics['DPD']:.3f}.
                        """

                        elif "why high bias is detected" in q or "why is high bias detected" in q or "why high bias detected" in q:

                            if metrics["DPD"] > 0.2:
                                answer = f"""
                        High Bias is detected because the Demographic Parity Difference (DPD) is {metrics['DPD']:.3f}, which is above the high-bias threshold (0.20).

                        This means there is a large outcome gap between sensitive groups.
                        Some groups are receiving significantly lower outcomes than others.
                        """
                            else:
                                answer = f"Currently DPD is {metrics['DPD']:.3f}, so High Bias is not detected."

                        elif "why moderate bias is detected" in q or "why is moderate bias detected" in q or "why moderate bias detected" in q:

                            if metrics["DPD"] > 0.1 and metrics["DPD"] <= 0.2:
                                answer = f"""
                        Moderate Bias is detected because the DPD is {metrics['DPD']:.3f}.

                        There is noticeable imbalance between groups, but not severe enough to be classified as High Bias.
                        """
                            else:
                                answer = f"Currently DPD is {metrics['DPD']:.3f}, so Moderate Bias is not detected."

                        elif "why low bias is detected" in q or "why is low bias detected" in q or "why low bias detected" in q:

                            if metrics["DPD"] <= 0.1:
                                answer = f"""
                        Low Bias is detected because the DPD is only {metrics['DPD']:.3f}.

                        This means the outcome gap between sensitive groups is small, so the dataset appears relatively fair.
                        """
                            else:
                                answer = f"Currently DPD is {metrics['DPD']:.3f}, so Low Bias is not detected."

                        elif "bias score" in q or "dpd" in q:
                            answer = f"Bias Gap (DPD): {metrics['DPD']:.3f}"

                        elif "disparate impact" in q or "dir" in q:
                            answer = f"Disparate Impact Ratio: {metrics['DIR']:.3f}"

                        elif "equal opportunity" in q:
                            answer = f"Equal Opportunity: {metrics['EO']:.3f}"

                        elif "best group" in q or "highest group" in q:
                            answer = f"Best performing group: {group_data.idxmax()}"

                        elif "suggest mitigation" in q or "improve fairness" in q:
                            answer = """
                1. Balance the dataset  
                2. Remove proxy sensitive features  
                3. Use fairness-aware models  
                4. Collect diverse data
                """

                        # ================= DATASET QUESTIONS =================
                        elif "column" in q:
                            total_cols = len(df.columns)
                            col_names = ", ".join(df.columns)

                            answer = f"""
                        Total columns: {total_cols}

                        Column Names: {col_names}
                        """
                        elif "row" in q or "row names" in q:

                            total_rows = len(df)

                            if total_rows <= 30:
                                row_names = ", ".join(map(str, df.index.tolist()))
                            else:
                                row_names = ", ".join(map(str, df.index.tolist()[:20])) + " ..."

                            answer = f"""
                        Total Number of Rows: {total_rows}

                        Row Names:
                        {row_names}
                        """

                        elif "missing" in q:
                            answer = df.isnull().sum().to_string()

                        else:
                            answer = "Please ask about fairness score, bias, groups, columns, rows, or mitigation."

                        # ✅ SHOW ANSWER
                        st.success(answer)

                # ===== STORE FOR REPORT PAGE =====
                st.session_state.before_bias = before_bias
                st.session_state.after_bias = after_bias
                st.session_state.fairness_score = fairness_score
                st.session_state.before_group = before_group
                st.session_state.after_group = after_group

            #===========Report Page===========
    elif st.session_state.page == "Report":

        st.markdown("""
        <style>

        [data-testid="stAppViewContainer"] {
            padding-top: 0rem !important;
        }

        .block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }

        header {
            visibility: hidden;
        }

        </style>
        """, unsafe_allow_html=True)

        st.title("📄 Bias Analysis Report")

        from datetime import datetime
        st.write("🕒 Generated on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if "after_group" not in st.session_state:
            st.warning("⚠️ Run analysis first in Dashboard")
            st.stop()

        if "before_bias" in st.session_state:

            st.write("Before Bias:", st.session_state.before_bias)  
            st.write("After Bias:", st.session_state.after_bias)  
            st.write("Fairness Score:", st.session_state.fairness_score)  

                    #--------BIAS INTERPRETATION--------  
            st.subheader("🧠 Bias Interpretation")  

            after_bias = st.session_state.after_bias  

            if after_bias > 0.2:  
                st.error("🔴 High bias detected after correction")  
            elif after_bias > 0.1:  
                st.warning("🟡 Moderate bias remains")  
            else:  
                st.success("🟢 Model is fair after correction")  

                    #--------IMPROVEMENT SUMMARY--------  
            st.subheader("📉 Improvement Summary")  

            improvement = st.session_state.before_bias - st.session_state.after_bias  

            if improvement > 0:  
                st.success(f"Bias reduced by {improvement:.3f}")  
            else:  
                st.warning("⚠️ No improvement detected")  

                    # Optional: percentage (looks more professional)  
            percent = (improvement / st.session_state.before_bias) * 100  
            st.write(f"📊 Improvement Percentage: {percent:.2f}%")  

                    #---------percentage improved---------  
            if st.session_state.before_bias != 0:  
                percent = (improvement / st.session_state.before_bias) * 100  
                        
            else:  
                st.write("📊 Improvement Percentage: N/A")  

                    #--------MOST & LEAST AFFECTED GROUPS--------  
            st.subheader("👥 Group Analysis")  

            st.write("Most affected group:", st.session_state.before_group.idxmin())  
            st.write("Least affected group:", st.session_state.before_group.idxmax())  

                    #--------RECOMMENDATIONS--------  
            st.subheader("💡 Recommendations")  


            after_bias = st.session_state.after_bias  

            if after_bias > 0.2:  
                st.write("- Collect more balanced data across groups")  
                st.write("- Remove or limit sensitive attributes (e.g., gender)")  
                st.write("- Apply fairness-aware machine learning algorithms")  
                st.write("- Perform bias monitoring regularly")  

            elif after_bias > 0.1:  
                st.write("- Slight imbalance detected, consider improving dataset diversity")  
                st.write("- Monitor model performance across groups")  

            else:  
                st.write("✅ Dataset is fairly balanced. Continue monitoring over time.")     

                    #--------GRAPHS--------  
            from PIL import Image  
            import os  

            st.subheader("📊 Bias Comparison (Bar Chart)")  

            if not os.path.exists("comparison_bar.png"):  
                st.warning("⚠️ Please run analysis in Dashboard first")  
                st.stop()  

            img = Image.open("comparison_bar.png")  
            st.image(img)  

            st.image("line_chart.png")  

            st.subheader("🥧 Distribution Comparison")  

            col1, col2 = st.columns(2)  

            # BEFORE PIE  
            fig1, ax1 = plt.subplots()  
            st.session_state.before_group.plot(kind='pie', autopct='%1.1f%%', ax=ax1)  
            ax1.set_title("Before")  
            ax1.set_ylabel("")  

            # AFTER PIE  
            fig2, ax2 = plt.subplots()  
            st.session_state.after_group.plot(kind='pie', autopct='%1.1f%%', ax=ax2)  
            ax2.set_title("After")  
            ax2.set_ylabel("")  

            with col1:  
                st.pyplot(fig1)  

            with col2:  
                st.pyplot(fig2)  

            st.subheader("🧾 Final Summary")  

            before = st.session_state.before_bias  
            after = st.session_state.after_bias  
            fairness = st.session_state.fairness_score  

            improvement = before - after  

            if before != 0:  
                percent = (improvement / before) * 100  
            else:  
                percent = 0  

            most_affected = st.session_state.before_group.idxmin()  
            least_affected = st.session_state.before_group.idxmax()  

            if after > 0.2:  
                conclusion = "High bias still remains."  
            elif after > 0.1:  
                conclusion = "Moderate bias remains."  
            else:  
                conclusion = "Low bias detected. Model is fairer now."  

            recommendation = "Continue regular fairness monitoring and use balanced datasets."  

            st.markdown(f"""  
            ### 📌 Final Report Summary  

            - Initial Bias Score: **{before:.3f}**  
            - Final Bias Score: **{after:.3f}**  
            - Fairness Score: **{fairness:.1f}/100**  
            - Bias Improvement: **{percent:.2f}%**  
            - Most Affected Group: **{most_affected}**  
            - Least Affected Group: **{least_affected}**  
            - Overall Result: **{conclusion}**  
            - Recommendation: **{recommendation}**  
            """)  

            # ===== DOWNLOAD BUTTON =====  
            report = f"""  
            AI FAIRNESS REPORT  

            Before Bias: {before:.3f}  
            After Bias: {after:.3f}  
            Fairness Score: {fairness:.1f}/100  

            Improvement: {percent:.2f}%  

            Most Affected Group: {most_affected}  
            Least Affected Group: {least_affected}  

            Overall Result: {conclusion}  

            Recommendation:  
            {recommendation}  

            Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
            """  
            # ---------------- PDF GENERATION ----------------  
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak  
            from reportlab.lib.styles import getSampleStyleSheet  
            from datetime import datetime  

            doc = SimpleDocTemplate("report.pdf")  
            styles = getSampleStyleSheet()  

            elements = []  

            # ---------------- TITLE ----------------  
            elements.append(Paragraph("AI FAIRNESS REPORT", styles["Title"]))  
            elements.append(Spacer(1, 10))  

            # ---------------- TIMESTAMP ----------------  
            elements.append(Paragraph(  
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",  
                styles["Normal"]  
            ))  
            elements.append(Spacer(1, 10))  

            # ---------------- VALUES ----------------  
            elements.append(Paragraph(  
                f"Before Bias: {before:.3f}", styles["Normal"]  
            ))  
            elements.append(Paragraph(  
                f"After Bias: {after:.3f}", styles["Normal"]  
            ))  
            elements.append(Paragraph(  
                f"Fairness Score: {fairness:.1f}/100", styles["Normal"]  
            ))  
            elements.append(Spacer(1, 10))  

            # ---------------- INTERPRETATION ----------------  
            after_bias = st.session_state.after_bias  

            if after_bias > 0.2:  
                interpretation = "High bias detected"  
            elif after_bias > 0.1:  
                interpretation = "Moderate bias detected"  
            else:  
                interpretation = "Low or no bias"  

            elements.append(Paragraph(f"Interpretation: {interpretation}", styles["Normal"]))  
            elements.append(Spacer(1, 10))  

            # ---------------- IMPROVEMENT ----------------  
            improvement = st.session_state.before_bias - st.session_state.after_bias  

            elements.append(Paragraph(  
                f"Bias Improvement: {improvement}", styles["Normal"]  
            ))  

            if st.session_state.before_bias != 0:  
                percent = (improvement / st.session_state.before_bias) * 100  
                elements.append(Paragraph(  
                    f"Improvement Percentage: {percent:.2f}%", styles["Normal"]  
                ))  

            elements.append(Spacer(1, 10))  

            # ---------------- GROUP ANALYSIS ----------------  
            elements.append(Paragraph(  
                f"Most affected group: {st.session_state.before_group.idxmin()}",  
                styles["Normal"]  
            ))  
            elements.append(Paragraph(  
                f"Least affected group: {st.session_state.before_group.idxmax()}",  
                styles["Normal"]  
            ))  
            elements.append(Spacer(1, 10))  

            # ---------------- RECOMMENDATIONS ----------------  
            elements.append(Paragraph("Recommendations:", styles["Heading2"]))  

            if after_bias > 0.1:  
                elements.append(Paragraph("- Balance dataset across groups", styles["Normal"]))  
                elements.append(Paragraph("- Remove sensitive attributes", styles["Normal"]))  
            else:  
                elements.append(Paragraph("Dataset is fairly balanced", styles["Normal"]))  

            elements.append(Spacer(1, 20))  

            # ---------------- CHARTS ----------------  
            
            # ---------- BAR CHARTS ----------  
            elements.append(Paragraph("Bias Comparison (Bar Chart)", styles["Heading3"]))  
            elements.append(Image("comparison_bar.png", width=400, height=300))  
            elements.append(Spacer(1, 20))  

            # ---------- LINE CHART ----------  
            elements.append(Paragraph("Bias Trend (Line Chart)", styles["Heading3"]))  
            elements.append(Image("line_chart.png", width=400, height=300))  
            elements.append(PageBreak())  

            # ---------- PIE CHARTS ----------  
            elements.append(Paragraph("Before Distribution (Pie Chart)", styles["Heading3"]))  
            elements.append(Image("before_pie.png", width=400, height=300))  
            elements.append(Spacer(1, 20))  

            elements.append(Paragraph("After Distribution (Pie Chart)", styles["Heading3"]))  
            elements.append(Image("after_pie.png", width=400, height=300))  

            # ================= FINAL SUMMARY =================  
            before = st.session_state.before_bias  
            after = st.session_state.after_bias  

            improvement = before - after  

            if before != 0:  
                percent = (improvement / before) * 100  
            else:  
                percent = 0  

            most_affected = st.session_state.before_group.idxmin()  

            # conclusion  
            if after > 0.2:  
                conclusion = "The model still shows high bias and needs improvement."  
            elif after > 0.1:  
                conclusion = "The model shows moderate bias; improvements recommended."  
            else:  
                conclusion = "The model is fairly balanced with low bias."  

            elements.append(Spacer(1, 20))  
            elements.append(Paragraph("FINAL SUMMARY", styles["Heading2"]))  
            elements.append(Paragraph(f"Initial Bias: {before:.3f}", styles["Normal"]))  
            elements.append(Paragraph(f"Final Bias: {after:.3f}", styles["Normal"]))  
            elements.append(Paragraph(f"Fairness Score: {fairness:.1f}/100", styles["Normal"]))  
            elements.append(Paragraph(f"Improvement: {percent:.2f}%", styles["Normal"]))  
            elements.append(Paragraph(f"Most Affected Group: {most_affected}", styles["Normal"]))  
            elements.append(Paragraph(f"Least Affected Group: {least_affected}", styles["Normal"]))  
            elements.append(Paragraph(f"Result: {conclusion}", styles["Normal"]))  
            elements.append(Paragraph(f"Recommendation: {recommendation}", styles["Normal"]))  
            # ---------------- BUILD PDF ----------------  
            doc.build(elements)  

            # ---------------- DOWNLOAD ----------------  
            with open("report.pdf", "rb") as file:  
                st.download_button("📄 Download Full PDF Report", file, "report.pdf")

    elif st.session_state.page == "About":

            st.title("ℹ️ About This Project")

            st.markdown("""
            ## ⚖️ AI Fairness Analyzer

            AI Fairness Analyzer is an intelligent web application designed to identify, analyze, and reduce bias in AI datasets and machine learning systems.

            In today's world, AI is used in hiring, healthcare, banking, education, and many decision-making systems. If datasets contain bias, AI models may produce unfair outcomes. This project helps solve that challenge by measuring fairness and suggesting improvements.

            ---

            ## 🚀 Core Features

            ✅ Upload CSV datasets easily  
            ✅ Detect bias across sensitive groups  
            ✅ Calculate fairness metrics  
            ✅ Multi-sensitive attribute analysis  
            ✅ Before vs After bias correction  
            ✅ Fairness Score generation  
            ✅ Accuracy vs Fairness Tradeoff graph  
            ✅ Visual dashboards with charts  
            ✅ PDF Report generation  
            ✅ Download complete analysis report  

            ---

            ## 📊 Fairness Metrics Used

            🔹 Demographic Parity Difference (DPD)  
            Measures gap between highest and lowest group outcomes.

            🔹 Disparate Impact Ratio (DIR)  
            Measures whether one group receives favorable outcomes less often.

            🔹 Equal Opportunity (EO)  
            Measures fairness in opportunities across groups.

            ---

            ## 🎯 Project Objective

            The goal of this project is to help organizations build:

            ✔ Transparent AI Systems  
            ✔ Ethical Decision Making  
            ✔ Fair Hiring Models  
            ✔ Inclusive Machine Learning Solutions  
            ✔ Responsible AI Applications  

            ---

            ## 🛠 Technologies Used

            - Python  
            - Streamlit  
            - Pandas  
            - Matplotlib  
            - ReportLab  
            - Data Analytics Concepts  

            ---

            ## 🌍 Real World Use Cases

            🏦 Loan Approval Systems  
            🏥 Healthcare Predictions  
            💼 Recruitment Screening  
            🎓 College Admissions  
            👮 Risk Assessment Systems  

            ---

            ## 👩‍💻 Developed For

            This project is created for hackathons, academic innovation, and responsible AI demonstrations.

            ---

            ## 💡 Future Enhancements

            🔮 Live model auditing  
            🔮 Explainable AI (SHAP)  
            🔮 Real-time dashboard monitoring  
            🔮 Cloud deployment  
            🔮 Team collaboration tools  

            ---

            ## ❤️ Final Note

            Fair AI is not just better technology — it is better society.
            """)


if not st.session_state.logged_in:

    if st.session_state.auth_page == "welcome":
        welcome_page()

    elif st.session_state.auth_page == "login":
        login_page()

    elif st.session_state.auth_page == "signup":
        signup_page()

    elif st.session_state.auth_page == "forgot":
        forgot_page()

else:
    main_app()
