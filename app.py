import streamlit as st
from utils.calculator import calculate_sgpa, calculate_cgpa, suggest_sgpa, convert_grade
from utils.doc_exporter import export_sgpa_report, export_cgpa_report
from pathlib import Path

svg_icon = Path("assets/graduation-cap.svg").read_text(encoding="utf-8")
st.set_page_config(
    page_title="SemSnap",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Theme Variables ───────────────────────────────────────────────────────────
BG = "#111827"
BG2 = "#1f2937"
BG3 = "#374151"
BORDER = "#374151"
TEXT = "#f9fafb"
TEXT2 = "#9ca3af"
TEXT3 = "#d1d5db"

GREEN = "#10b981"
GREEN_HVR = "#059669"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif; }}

.stApp {{ background-color: {BG}; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* Remove top padding */
.block-container {{
    padding-top: 1rem !important;
}}
/* ── Hero ── */
.hero {{
    text-align: center;
    padding: 3rem 1rem 0.2rem 1rem;
}}
.hero h1 {{
    font-size: 3rem;
    font-weight: 800;
    color: {GREEN} !important;
    margin: 0;
}}
.hero p {{
    color: {TEXT2};
    font-size: 1.05rem;
    margin-top: 0.5rem;
}}

/* ── Section Label ── */
.section-label {{
    color: {GREEN} !important;
    font-size: 1.155rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-align: center;
    margin: 0.4rem 0 0.5rem 0;
}}

/* ── Global Text ── */
p, li {{ color: {TEXT} !important; }}
strong {{ color: {TEXT} !important; }}
label {{ color: {TEXT} !important; }}
h1, h2, h3, h4, h5, h6 {{ color: {TEXT} !important; }}
.stMarkdown p {{ color: {TEXT} !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: {BG2};
    border-radius: 12px;
    padding: 5px;
    border: 1px solid {BORDER};
    justify-content: center;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    color: {TEXT2} !important;
    font-weight: 600;
    padding: 10px 28px;
    font-size: 0.95rem;
}}
.stTabs [aria-selected="true"] {{
    background: {GREEN} !important;
    color: white !important;
}}
.stTabs [aria-selected="true"] p {{
    color: white !important;
}}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input {{
    background: {BG2} !important;
    border: 1.5px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-size: 0.95rem !important;
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: {GREEN} !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.15) !important;
}}
.stSelectbox > div > div {{
    background: {BG2} !important;
    border: 1.5px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}

/* ── Delete button — fix alignment ── */
.delete-btn {{
    display: flex;
    align-items: flex-end;
    padding-bottom: 6px;
}}

/* ── Buttons ── */
[data-testid="stButton"] {{
    display: flex !important;
    justify-content: center !important;
}}
[data-testid="stButton"] > button {{
    width: 240px !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    background: {GREEN} !important;
    color: white !important;
    margin-top: 0.75rem !important;
    transition: all 0.25s ease !important;
}}
[data-testid="stButton"] > button:hover {{
    background: {GREEN_HVR} !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.35) !important;
}}
[data-testid="stButton"] > button:disabled {{
    background: {BORDER} !important;
    color: {TEXT2} !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── Small delete button override ── */
button[kind="secondary"] {{
    width: auto !important;
    min-width: 0 !important;
    padding: 0.4rem 0.75rem !important;
    font-size: 0.8rem !important;
    margin-top: 0 !important;
    background: #374151 !important;
    color: #f87171 !important;
    border: 1px solid #f87171 !important;
    border-radius: 8px !important;
}}

/* ── Download Button ── */
[data-testid="stDownloadButton"] {{
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}}

[data-testid="stDownloadButton"] > button {{
    width: 280px !important;
    margin: 0 auto !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    background: #10b981 !important;
    color: white !important;
    border: none !important;
    transition: all 0.25s ease !important;
}}

[data-testid="stDownloadButton"] > button:hover {{
    background: #059669 !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.35) !important;
}}

/* ── Result Card ── */
.result-card {{
    background: {BG2};
    border: 2px solid {GREEN};
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}}
.result-card .result-label {{
    color: {GREEN} !important;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
.result-card .result-value {{
    color: {TEXT} !important;
    font-size: 3rem;
    font-weight: 800;
    margin-top: 4px;
}}
.result-card .result-sub {{
    color: {TEXT2} !important;
    font-size: 0.85rem;
    margin-top: 4px;
}}

/* ── Info Card ── */
.info-card {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    color: {TEXT} !important;
}}
.info-card b {{ color: {GREEN} !important; }}

/* ── Suggestion Box ── */
.suggestion-box {{
    background: {BG2};
    border: 1px solid {GREEN};
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    color: {TEXT} !important;
    font-size: 1rem;
    line-height: 1.75;
    text-align: center;
}}
.suggestion-box .sg-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {GREEN} !important;
}}

/* ── Converter Card ── */
.converter-result {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1.25rem;
    margin: 0.75rem 0;
}}
.converter-result .cr-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid {BORDER};
    color: {TEXT} !important;
}}
.converter-result .cr-row:last-child {{
    border-bottom: none;
}}
.converter-result .cr-label {{
    color: {TEXT2} !important;
    font-weight: 600;
    font-size: 0.85rem;
}}
.converter-result .cr-value {{
    color: {GREEN} !important;
    font-weight: 700;
    font-size: 0.95rem;
}}

/* ── Expanders ── */
div[data-testid="stExpander"] {{
    background: {BG2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
    overflow: hidden;
}}
div[data-testid="stExpander"]:hover {{
    border-color: {GREEN} !important;
}}
div[data-testid="stExpander"] summary {{
    background: {BG2} !important;
    color: {TEXT} !important;
    font-weight: 600 !important;
    padding: 1rem 1.25rem !important;
}}
div[data-testid="stExpander"] summary:hover {{
    background: {BG3} !important;
    color: {GREEN} !important;
}}
div[data-testid="stExpander"] summary p {{
    color: {TEXT} !important;
}}
div[data-testid="stExpander"] summary:hover p {{
    color: {GREEN} !important;
}}
div[data-testid="stExpander"] summary svg {{
    fill: {GREEN} !important;
}}
div[data-testid="stExpander"] > div:last-child {{
    background: {BG3} !important;
    padding: 1rem 1.25rem !important;
}}
div[data-testid="stExpander"] > div:last-child p {{
    color: {TEXT3} !important;
}}

/* ── Metric Row ── */
.metric-row {{
    display: flex;
    gap: 0.75rem;
    margin: 1rem 0;
}}
.metric-card {{
    flex: 1;
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
}}
.metric-card .num {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {GREEN} !important;
}}
.metric-card .lbl {{
    color: {TEXT2} !important;
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 2px;
}}

/* ── Divider ── */
hr {{ border-color: {BORDER} !important; }}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: {GREEN} !important; }}

/* ── Alert ── */
.stAlert p {{ color: {TEXT} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Grading Systems ───────────────────────────────────────────────────────────
GRADING_SYSTEMS = {
    "10 Point — O/A+/A/B+/B/C/F (Most Indian Universities)": {
        'O (10)': 10, 'A+ (9)': 9, 'A (8)': 8,
        'B+ (7)': 7, 'B (6)': 6, 'C (5)': 5, 'F (0)': 0
    },
    "10 Point — S/A/B/C/D/E/F (Some Indian Colleges)": {
        'S (10)': 10, 'A (9)': 9, 'B (8)': 8,
        'C (7)': 7, 'D (6)': 6, 'E (5)': 5, 'F (0)': 0
    },
    "10 Point — O/A/B/C/D/F (Simplified)": {
        'O (10)': 10, 'A (9)': 9, 'B (8)': 8,
        'C (7)': 7, 'D (6)': 6, 'F (0)': 0
    },
    "4 Point — A/B/C/D/F (US System)": {
        'A (4.0)': 4.0, 'A- (3.7)': 3.7, 'B+ (3.3)': 3.3,
        'B (3.0)': 3.0, 'B- (2.7)': 2.7, 'C+ (2.3)': 2.3,
        'C (2.0)': 2.0, 'C- (1.7)': 1.7, 'D+ (1.3)': 1.3,
        'D (1.0)': 1.0, 'F (0.0)': 0.0
    },
}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {svg_icon}
    <h1>SemSnap</h1>
    <h3>Precision for Every Semester`</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:0.15rem 0;'>", unsafe_allow_html=True)

# ── Grading System Selector ───────────────────────────────────────────────────
st.markdown('<div class="section-label">Select Your Grading System</div>',
            unsafe_allow_html=True)

selected_system = st.selectbox(
    "Grading System",
    list(GRADING_SYSTEMS.keys()),
    label_visibility="collapsed"
)

# Reset subjects if grading system changes
if "last_system" not in st.session_state:
    st.session_state["last_system"] = selected_system

if st.session_state["last_system"] != selected_system:
    st.session_state["last_system"] = selected_system
    st.session_state.pop("subjects", None)
    st.session_state.pop("sgpa_result", None)
    st.session_state.pop("sgpa_subjects", None)
    st.rerun()

grade_options = GRADING_SYSTEMS[selected_system]
scale = 4 if "4 Point" in selected_system else 10

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "SGPA", "CGPA", "Suggestions", "Converter"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — SGPA
# ════════════════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — SGPA
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(
        '<div class="section-label">SGPA Calculator</div>',
        unsafe_allow_html=True
    )

    if "subjects" not in st.session_state:
        st.session_state["subjects"] = [
            {
                "name": "",
                "credits": 3,
                "grade": list(grade_options.keys())[0]
            }
        ]

    semester_name = st.text_input(
        "Semester Name (optional)",
        placeholder="e.g. Semester 3"
    )

    subjects_to_delete = []

    for i, subject in enumerate(st.session_state["subjects"]):

        col1, col2, col3, col4 = st.columns([3, 2, 1.5, 0.5])

        # Subject Name
        with col1:
            st.markdown(
                f"<small style='color:{TEXT2}'>Subject Name</small>",
                unsafe_allow_html=True
            )

            st.session_state["subjects"][i]["name"] = st.text_input(
                f"Subject {i+1}",
                value=subject["name"],
                placeholder=f"Subject {i+1}",
                key=f"name_{i}",
                label_visibility="collapsed"
            )

        # Grade
        with col2:
            st.markdown(
                f"<small style='color:{TEXT2}'>Grade</small>",
                unsafe_allow_html=True
            )

            grade_keys = list(grade_options.keys())

            current_grade = subject.get(
                "grade",
                grade_keys[0]
            )

            safe_index = (
                grade_keys.index(current_grade)
                if current_grade in grade_keys
                else 0
            )

            st.session_state["subjects"][i]["grade"] = st.selectbox(
                "Grade",
                options=grade_keys,
                index=safe_index,
                key=f"grade_{i}",
                label_visibility="collapsed"
            )

        # Credits
        with col3:
            st.markdown(
                f"<small style='color:{TEXT2}'>Credits</small>",
                unsafe_allow_html=True
            )

            st.session_state["subjects"][i]["credits"] = st.number_input(
                "Credits",
                min_value=1,
                max_value=6,
                value=subject["credits"],
                key=f"credits_{i}",
                label_visibility="collapsed"
            )

        # Delete
        with col4:
            st.markdown(
                f"<small style='color:{TEXT2}'>Del</small>",
                unsafe_allow_html=True
            )

            if (
                st.button("✕", key=f"del_{i}")
                and len(st.session_state["subjects"]) > 1
            ):
                subjects_to_delete.append(i)

    for i in sorted(subjects_to_delete, reverse=True):
        st.session_state["subjects"].pop(i)

    if subjects_to_delete:
        st.rerun()

    st.markdown(" ")

    col_add, col_calc = st.columns(2)

    with col_add:
        if st.button("➕ Add Subject", key="add_subject"):
            st.session_state["subjects"].append(
                {
                    "name": "",
                    "credits": 3,
                    "grade": list(grade_options.keys())[0]
                }
            )
            st.rerun()

    with col_calc:
        if st.button("Calculate SGPA", key="calc_sgpa"):

            subjects_data = [
                {
                    "name": s["name"] or f"Subject {i+1}",
                    "credits": s["credits"],
                    "grade_point": grade_options[s["grade"]]
                }
                for i, s in enumerate(st.session_state["subjects"])
            ]

            sgpa = calculate_sgpa(subjects_data, scale)

            st.session_state["sgpa_result"] = sgpa
            st.session_state["sgpa_subjects"] = subjects_data
            st.session_state["sgpa_semester"] = (
                semester_name or "Semester"
            )

    if "sgpa_result" in st.session_state:

        sgpa = st.session_state["sgpa_result"]

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Your SGPA</div>
                <div class="result-value">{sgpa}</div>
                <div class="result-sub">
                    out of {scale}.0 •
                    {st.session_state["sgpa_semester"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Subject Breakdown"):

            for s in st.session_state["sgpa_subjects"]:

                st.markdown(
                    f"""
                    <div class="info-card">
                        <b>{s["name"]}</b> —
                        {s["credits"]} credits •
                        Grade Point: {s["grade_point"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        st.markdown(
            '<div class="section-label">Download Report</div>',
            unsafe_allow_html=True
        )

        st.markdown(" ")

        docx = export_sgpa_report(
            st.session_state["sgpa_subjects"],
            sgpa,
            scale,
            st.session_state["sgpa_semester"]
        )

        st.download_button(
            "⬇Download SGPA Report (DOCX)",
            data=docx,
            file_name=f"{st.session_state['sgpa_semester'].replace(' ', '_')}_SGPA.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — CGPA
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">CGPA Calculator</div>',
                unsafe_allow_html=True)

    if "semesters" not in st.session_state:
        st.session_state["semesters"] = [{"sgpa": 0.0, "credits": 20}]

    sems_to_delete = []
    for i, sem in enumerate(st.session_state["semesters"]):
        col1, col2, col3 = st.columns([2, 2, 0.5])
        with col1:
            st.markdown(
                f"<small style='color:{TEXT2}'>Semester {i+1} SGPA</small>", unsafe_allow_html=True)
            st.session_state["semesters"][i]["sgpa"] = st.number_input(
                f"Sem {i+1} SGPA",
                min_value=0.0, max_value=float(scale),
                value=float(sem["sgpa"]), step=0.01,
                key=f"sem_sgpa_{i}",
                label_visibility="collapsed"
            )
        with col2:
            st.markdown(
                f"<small style='color:{TEXT2}'>Total Credits</small>", unsafe_allow_html=True)
            st.session_state["semesters"][i]["credits"] = st.number_input(
                f"Sem {i+1} Credits",
                min_value=1, max_value=50,
                value=sem["credits"],
                key=f"sem_credits_{i}",
                label_visibility="collapsed"
            )
        with col3:
            st.markdown(
                f"<small style='color:{TEXT2}'>Del</small>", unsafe_allow_html=True)
            if st.button("✕", key=f"del_sem_{i}") and len(st.session_state["semesters"]) > 1:
                sems_to_delete.append(i)

    for i in sorted(sems_to_delete, reverse=True):
        st.session_state["semesters"].pop(i)
        st.rerun()

    st.markdown(" ")
    col_add2, col_calc2 = st.columns(2)
    with col_add2:
        if st.button("➕  Add Semester", key="add_sem"):
            st.session_state["semesters"].append({"sgpa": 0.0, "credits": 20})
            st.rerun()
    with col_calc2:
        if st.button("Calculate CGPA", key="calc_cgpa"):
            from utils.calculator import calculate_cgpa
            cgpa = calculate_cgpa(st.session_state["semesters"])
            st.session_state["cgpa_result"] = cgpa

    if "cgpa_result" in st.session_state:
        cgpa = st.session_state["cgpa_result"]
        total_credits = sum(s["credits"]
                            for s in st.session_state["semesters"])

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Your CGPA</div>
            <div class="result-value">{cgpa}</div>
            <div class="result-sub">out of {scale}.0 • {len(st.session_state['semesters'])} semesters • {total_credits} total credits</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="num">{len(st.session_state['semesters'])}</div>
                <div class="lbl">Semesters</div>
            </div>
            <div class="metric-card">
                <div class="num">{total_credits}</div>
                <div class="lbl">Total Credits</div>
            </div>
            <div class="metric-card">
                <div class="num">{cgpa}</div>
                <div class="lbl">CGPA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-label">Download Report</div>',
                    unsafe_allow_html=True)
        st.markdown(" ")
        docx = export_cgpa_report(st.session_state["semesters"], cgpa, scale)
        st.download_button(
            "⬇ Download CGPA Report (DOCX)",
            data=docx,
            file_name="CGPA_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SUGGESTIONS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Grade Suggestions</div>',
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; color:{TEXT2}'>Find out what SGPA you need next semester to hit your target CGPA</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        current_cgpa = st.number_input(
            "Current CGPA", min_value=0.0, max_value=float(scale),
            value=7.5 if scale == 10 else 3.0, step=0.01
        )
        completed_credits = st.number_input(
            "Total Credits Completed", min_value=1, max_value=500, value=80
        )
    with col2:
        target_cgpa = st.number_input(
            "Target CGPA", min_value=0.0, max_value=float(scale),
            value=8.0 if scale == 10 else 3.5, step=0.01
        )
        next_credits = st.number_input(
            "Credits in Next Semester", min_value=1, max_value=50, value=20
        )

    if st.button("Calculate Required SGPA", key="calc_suggestion"):
        from utils.calculator import suggest_sgpa
        needed = suggest_sgpa(current_cgpa, completed_credits,
                              target_cgpa, next_credits, scale)
        if needed is None:
            st.error(
                f"Target CGPA of {target_cgpa} is not achievable in one semester with {next_credits} credits.")
        else:
            st.markdown(f"""
            <div class="suggestion-box">
                <div style="color:{TEXT2}; font-size:0.85rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;">Required SGPA Next Semester</div>
                <div class="sg-value">{needed}</div>
                <div style="color:{TEXT2}; font-size:0.85rem; margin-top:6px;">out of {scale}.0 to reach a CGPA of {target_cgpa}</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — CONVERTER
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">Grade Converter</div>',
                unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; color:{TEXT2}'>Convert between Percentage, Grade Point, and Letter Grade</p>",
        unsafe_allow_html=True
    )

    convert_from = st.selectbox(
        "Convert from", ["Percentage", "Grade Point", "Letter Grade"]
    )

    if convert_from == "Percentage":
        val = st.number_input(
            "Enter Percentage", min_value=0.0, max_value=100.0, value=75.0, step=0.1
        )
        from_type = "percentage"
    elif convert_from == "Grade Point":
        val = st.number_input(
            "Enter Grade Point", min_value=0.0,
            max_value=float(scale),
            value=8.0 if scale == 10 else 3.0, step=0.1
        )
        from_type = "grade_point"
    else:
        val = st.text_input("Enter Letter Grade", value="A")
        from_type = "letter"

    if st.button("Convert", key="convert"):
        from utils.calculator import convert_grade
        result = convert_grade(val, from_type, scale)
        if result:
            st.markdown(f"""
            <div class="converter-result">
                <div class="cr-row">
                    <span class="cr-label">Percentage</span>
                    <span class="cr-value">{result['percentage']}%</span>
                </div>
                <div class="cr-row">
                    <span class="cr-label">Grade Point</span>
                    <span class="cr-value">{result['grade_point']}</span>
                </div>
                <div class="cr-row">
                    <span class="cr-label">Letter Grade</span>
                    <span class="cr-value">{result['letter']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Could not convert. Check your input value.")
