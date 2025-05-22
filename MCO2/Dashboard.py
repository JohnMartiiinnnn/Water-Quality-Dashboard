import streamlit as st
import base64
import datetime
import os
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
bfar_df = pd.read_csv('MCO2/BFAR.csv')  # Placeholder filename
philvolcs_df = pd.read_csv('MCO2/PHILVOLCS.csv')  # Placeholder filename

# Combine datasets for correlation analysis (assuming 'Date' column exists)
try:
    combined_df = pd.merge(bfar_df, philvolcs_df, on='Date', how='inner')
except KeyError:
    # If no 'Date' column, concatenate numeric columns
    numeric_bfar = bfar_df.select_dtypes(include=['float64', 'int64'])
    numeric_philvolcs = philvolcs_df.select_dtypes(include=['float64', 'int64'])
    combined_df = pd.concat([numeric_bfar, numeric_philvolcs], axis=1)

# ==== CONFIGURATION (Developer Customizable) ====
DEVELOPER_COLUMN_SPACING_PX = 25

# --- Folder names for Carousels ---
DISTRIBUTIONS_FOLDER = "MCO2/distributions"
MODEL_EVAL_FOLDER = "MCO2/model_eval"

AUTO_ADVANCE_INTERVAL = 3  # seconds for auto-advance

st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==== LOAD AND ENCODE HEADER IMAGE ====
try:
    with open("MCO2/taal_lake.png", "rb") as img_file:
        banner_img_base64 = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    st.error("Error: 'taal_lake.png' not found. Please ensure the image file is present.")
    banner_img_base64 = None

# ==== LOAD AND ENCODE FONT ====
try:
    with open("MCO2/Montserrat-Bold.ttf", "rb") as f:
        font_base64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    st.warning("Warning: 'Montserrat-Bold.ttf' font not found. Using default sans-serif font.")
    font_base64 = None

# ==== CUSTOM FONT STYLE ====
font_style = ""
if font_base64:
    font_style = f"""
    @font-face {{
        font-family: 'Montserrat';
        src: url("data:font/ttf;base64,{font_base64}") format('truetype');
    }}
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .section-header, .custom-label,
    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] p,
    .stButton button, .streamlit-expanderHeader p, .streamlit-expanderContent div {{
        font-family: 'Montserrat', sans-serif !important;
    }}
    """
else:
    font_style = """
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .section-header, .custom-label,
    .stTabs [data-baseweb="tab"], .stTabs [data-baseweb="tab"] p,
    .stButton button, .streamlit-expanderHeader p, .streamlit-expanderContent div {{
        font-family: sans-serif;
    }}
    """

# ==== IMAGE LOADING AND SESSION STATE FOR CAROUSELS ====
distribution_image_files = []
distributions_folder_exists = os.path.exists(DISTRIBUTIONS_FOLDER)
distribution_image_paths = []
if distributions_folder_exists:
    distribution_image_files = [f for f in os.listdir(DISTRIBUTIONS_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    distribution_image_files.sort()
    distribution_image_paths = [os.path.join(DISTRIBUTIONS_FOLDER, f) for f in distribution_image_files]

model_eval_image_files = []
model_eval_folder_exists = os.path.exists(MODEL_EVAL_FOLDER)
model_eval_image_paths = []
if model_eval_folder_exists:
    model_eval_image_files = [f for f in os.listdir(MODEL_EVAL_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    model_eval_image_files.sort()
    model_eval_image_paths = [os.path.join(MODEL_EVAL_FOLDER, f) for f in model_eval_image_files]

if 'distribution_image_paths' not in st.session_state:
    st.session_state.distribution_image_paths = distribution_image_paths
    st.session_state.current_distribution_index = 0
    st.session_state.last_auto_advance_distribution_time = time.time()

if 'model_eval_image_paths' not in st.session_state:
    st.session_state.model_eval_image_paths = model_eval_image_paths
    st.session_state.current_model_eval_index = 0
    st.session_state.last_auto_advance_model_eval_time = time.time()

# --- Auto-advance Logic ---
current_time = time.time()
if st.session_state.distribution_image_paths:
    if current_time - st.session_state.last_auto_advance_distribution_time > AUTO_ADVANCE_INTERVAL:
        st.session_state.current_distribution_index = (st.session_state.current_distribution_index + 1) % len(st.session_state.distribution_image_paths)
        st.session_state.last_auto_advance_distribution_time = current_time

if st.session_state.model_eval_image_paths:
    if current_time - st.session_state.last_auto_advance_model_eval_time > AUTO_ADVANCE_INTERVAL:
        st.session_state.current_model_eval_index = (st.session_state.current_model_eval_index + 1) % len(st.session_state.model_eval_image_paths)
        st.session_state.last_auto_advance_model_eval_time = current_time

# --- Manual Navigation Handlers ---
def next_distribution_image():
    if st.session_state.distribution_image_paths:
        st.session_state.current_distribution_index = (st.session_state.current_distribution_index + 1) % len(st.session_state.distribution_image_paths)
        st.session_state.last_auto_advance_distribution_time = time.time()

def prev_distribution_image():
    if st.session_state.distribution_image_paths:
        st.session_state.current_distribution_index = (st.session_state.current_distribution_index - 1) % len(st.session_state.distribution_image_paths)
        st.session_state.last_auto_advance_distribution_time = time.time()

def next_model_eval_image():
    if st.session_state.model_eval_image_paths:
        st.session_state.current_model_eval_index = (st.session_state.current_model_eval_index + 1) % len(st.session_state.model_eval_image_paths)
        st.session_state.last_auto_advance_model_eval_time = time.time()

def prev_model_eval_image():
    if st.session_state.model_eval_image_paths:
        st.session_state.current_model_eval_index = (st.session_state.current_model_eval_index - 1) % len(st.session_state.model_eval_image_paths)
        st.session_state.last_auto_advance_model_eval_time = time.time()

# Inject CSS styles
st.markdown(f"""
<style>
    {font_style}
    .block-container {{
        padding: 0rem 3rem !important;
        max-width: 90% !important;
    }}
    .banner-container {{
        width: 100%;
        text-align: center;
        padding-top: 30px;
        margin-bottom: 10px;
    }}
    .banner-container img {{
        width: 70%;
        height: auto;
        border-radius: 8px;
    }}
    .section-header {{
        font-size: 18px;
        color: #FFFFFF;
        margin-top: 0px;
        text-align: center;
        background-color: #123458;
        margin-bottom: 10px;
        font-weight: 600;
        padding: 3px;
        border-radius: 8px;
    }}
    .column-wrapper > div {{
        padding-right: {DEVELOPER_COLUMN_SPACING_PX}px !important;
    }}
    .column-wrapper > div:last-child {{
        padding-right: 0px !important;
    }}
    .stTabs [data-baseweb="tab-panel"] h2 {{
        color: #003366;
        font-size: 24px;
        margin-top: 0px;
        margin-bottom: 0px;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #547792;
        color: #000000;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
        justify-content: center;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 10px;
        white-space: pre-wrap;
        background-color: #DBE2EF;
        border-radius: 8px 8px 0px 0px;
    }}
    .stTabs [data-baseweb="tab-list"] button {{
        padding: 20px 20px;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: #3F72AF !important;
        height: 3px;
    }}
    .stTabs [data-baseweb="tab-panel"] {{
        padding: 30px 0px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #123458;
        color: #ffffff !important;
        height: 40px;
    }}
</style>
""", unsafe_allow_html=True)

# ==== DISPLAY BANNER IMAGE ====
if banner_img_base64:
    st.markdown(f"""
    <div class="banner-container" id="banner">
        <img src="data:image/png;base64,{banner_img_base64}" class="banner-img" alt="Taal Lake Banner"/>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(
        "<div class='banner-container' id='banner' style='min-height: 80px; background-color: #eee; display: flex; align-items: center; justify-content: center;'><p style='color: #555;'>Banner Image Area (Image not found)</p></div>",
        unsafe_allow_html=True)

# ==== MAIN CONTENT AREA ====
tab1, tab2, tab3, tab4, tab_recommendations = st.tabs([
    "🏠 Homepage",
    "📁 Dataset Information",
    "📈 Exploratory Data Analysis",
    "🔮 Prediction",
    "📝 Recommendations"
])

# --- Tab 1: Homepage ---
with tab1:
    st.markdown("""
        <h3 style='color: #25316D; font-size: 40px; text-align: center; margin-top: 0px;'>
        Welcome to Taal Lake Water Quality Dashboard!
        </h3>
        """, unsafe_allow_html=True)

    col1, col3, col2 = st.columns([8, 0.1, 4])

    with col2:
        st.markdown("""
        <h2 style='color: #25316D; font-size: 18px; text-align: left;'>
        About Taal Lake
        </h2>
        """, unsafe_allow_html=True)
        st.image("MCO2/Taal-volcano-map.jpg", caption="Image from: ShelterBox USA")
        st.markdown("""
        <div style='text-align: justify;'>
        Taal Lake, located in Batangas, Philippines, is a freshwater volcanic lake 
        within a caldera formed by prehistoric eruptions. The lake's ecosystem is 
        uniquely influenced by volcanic activity and environmental factors, making 
        it a crucial site for water quality monitoring. Understanding parameters 
        such as pH, dissolved oxygen, and pollutant levels helps protect aquatic 
        life, support local fisheries, and maintain safe water standards for nearby 
        communities. This study leverages data mining and machine learning to 
        predict water quality trends and support sustainable lake management.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <h3 style='color: #25316D; font-size: 18px; text-align: left; margin-top: 5px;'>
            About the Course and Activity
            </h3>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center;'>
        In partial fulfillment of:
        **CPEN 106 - ELECTIVES 2: BIG DATA ANALYTICS**
        <div style='text-align: justify;'>
        **Data Mining and Data Visualization for Water Quality Prediction in Taal Lake**
        This laboratory activity applies data mining and visualization techniques to predict 
        water quality parameters in Taal Lake using real-world datasets. Students collected, 
        preprocessed, analyzed, and modeled data to forecast pH, dissolved oxygen, and pollutant 
        levels. Machine learning models such as CNN, LSTM, and Hybrid CNN-LSTM were explored 
        alongside interactive Python-based visualizations.
        **Objectives:**
        - Extract insights from environmental datasets using data mining.
        - Develop predictive models for water quality.
        - Compare CNN, LSTM, and hybrid ensemble models.
        - Visualize water quality trends and patterns.
        - Interpret environmental and volcanic impacts on water.
        - Predict Water Quality Index (WQI) and pollutant levels for actionable insights.
        **Learning Outcomes:**
        - Collect relevant water and environmental datasets.
        - Perform preprocessing and exploratory analysis.
        - Build machine learning models for prediction.
        - Compare ensemble models (CNN, LSTM, Hybrid CNN-LSTM).
        - Create interactive visualizations.
        - Provide recommendations based on WQI and pollutant data.
        """, unsafe_allow_html=True)

        st.markdown("""
            <h3 style='color: #25316D; font-size: 18px; text-align: left; margin-top: 5px;'>
            About the Developers
            </h3>
            """, unsafe_allow_html=True)
        st.markdown("**BS CPE 3-1**")
        st.markdown("**Group 2**")
        st.image("MCO2/dave.jpg", width=100)
        st.markdown("""
            **BULASO, DAVE PATRICK I.**  
            Phone: +63XXXXXXXXXX  
            Email: main.davepatrick.bulaso@cvsu.edu.ph  
            """)
        st.image("MCO2/alexa.jpg", width=100)
        st.markdown("""
            **DENNA, ALEXA YVONNE V.**  
            Phone: +639184719122    
            Email: main.alexayvonne.denna@cvsu.edu.ph
            """)
        st.image("MCO2/martin.png", width=100)
        st.markdown("""
            **EJERCITADO, JOHN MARTIN P.**  
            Phone: +639262333664             
            Email: main.johnmartin.ejercitado@cvsu.edu.ph 
            """)
        st.image("MCO2/gian.jpg", width=100)
        st.markdown("""
            **ESPINO, GIAN JERICHO Z.**  
            Phone: +639108733830    
            Email: main.gianjericho.espino@cvsu.edu.ph
            """)
        st.image("MCO2/harley.jpg", width=100)
        st.markdown("""
            **INCIONG, HARLEY EVANGEL J.**  
            Phone: +639516120316    
            Email: main.harleyevangel.inciong@cvsu.edu.ph
            """)

    with col1:
        st.header("Featured Visualizations")

        st.markdown("""
            <h3 style='color: #112D4E; font-size: 20px; text-align: left; margin-top: 0px;'>
            Correlation Heatmap
            </h3>
            """, unsafe_allow_html=True)

        # Interactive Correlation Heatmap
        numeric_columns = combined_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_columns = st.multiselect(
            "Select parameters for correlation heatmap",
            options=numeric_columns,
            default=numeric_columns[:min(5, len(numeric_columns))]  # Default to first 5 columns or fewer
        )
        if selected_columns:
            correlation_matrix = combined_df[selected_columns].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title('Correlation Heatmap')
            st.pyplot(plt)
            plt.clf()  # Clear the figure to prevent overlap
            st.markdown("<div style='color: #555; margin-top: 5px; text-align: center;'>Overall Feature Correlation</div>", unsafe_allow_html=True)
        else:
            st.warning("Please select at least one parameter to display the correlation heatmap.")

        st.markdown("---")

        st.markdown("""
            <h3 style='color: #112D4E; font-size: 20px; text-align: left; margin-top: 0px;'>
            Water Quality Index
            </h3>
            """, unsafe_allow_html=True)
        try:
            with open("MCO2/WQI.png", "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'>
                    <img src='data:image/png;base64,{encoded}' style='width: 80%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px;' />
                    <div style='color: #555; margin-top: 5px;'>Water Quality Index</div>
                </div>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Error: Image 'WQI.png' not found.")
        except Exception as e:
            st.error(f"Error displaying image: {e}")

        st.markdown("---")

        def image_to_base64(image_path):
            with open(image_path, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{b64_string}"

        st.markdown("""
            <h3 style='color: #112D4E; font-size: 20px; text-align: left; margin-top: 0px;'>
            Distributions
            </h3>
            """, unsafe_allow_html=True)
        if not distributions_folder_exists:
            st.error(f"The folder '{DISTRIBUTIONS_FOLDER}' was not found. Cannot display distribution visualizations.")
        elif not st.session_state.distribution_image_paths:
            st.warning(f"No image files (.png, .jpg, .jpeg) found in the '{DISTRIBUTIONS_FOLDER}' folder.")
        else:
            current_image_path = st.session_state.distribution_image_paths[st.session_state.current_distribution_index]
            image_caption = os.path.basename(current_image_path).replace("_", " ").rsplit('.', 1)[0]
            img_base64 = image_to_base64(current_image_path)
            st.markdown(
                f"""
                <div style='padding: 20px; text-align: center;'>
                    <img src='{img_base64}' style='max-width: 80%; height: auto; border-radius: 10px;' />
                </div>
                """, unsafe_allow_html=True)
            col_prev_dist, col_status_dist, col_next_dist = st.columns([1, 2, 1])
            with col_prev_dist:
                st.button("Previous", on_click=prev_distribution_image, use_container_width=True,
                          disabled=(len(st.session_state.distribution_image_paths) <= 1), key="prev_dist_btn")
            with col_status_dist:
                st.markdown(
                    f"<p style='text-align:center; margin-top: 10px;'>Image {st.session_state.current_distribution_index + 1} of {len(st.session_state.distribution_image_paths)}</p>",
                    unsafe_allow_html=True)
            with col_next_dist:
                st.button("Next", on_click=next_distribution_image, use_container_width=True,
                          disabled=(len(st.session_state.distribution_image_paths) <= 1), key="next_dist_btn")

        st.markdown("---")

        st.markdown("""
            <h3 style='color: #112D4E; font-size: 20px; text-align: left; margin-top: 0px;'>
            Predictive Model Evaluation
            </h3>
            """, unsafe_allow_html=True)
        if not model_eval_folder_exists:
            st.error(f"The folder '{MODEL_EVAL_FOLDER}' was not found. Cannot display model evaluation visualizations.")
        elif not st.session_state.model_eval_image_paths:
            st.warning(f"No image files (.png, .jpg, .jpeg) found in the '{MODEL_EVAL_FOLDER}' folder.")
        else:
            current_image_path = st.session_state.model_eval_image_paths[st.session_state.current_model_eval_index]
            image_caption = os.path.basename(current_image_path).replace("_", " ").rsplit('.', 1)[0]
            img_base64 = image_to_base64(current_image_path)
            st.markdown(
                f"""
                <div style='padding: 20px; text-align: center;'>
                    <img src='{img_base64}' style='max-width: 55%; height: auto; border-radius: 10px;' />
                </div>
                """, unsafe_allow_html=True)
            col_prev_eval, col_status_eval, col_next_eval = st.columns([1, 2, 1])
            with col_prev_eval:
                st.button("Previous", on_click=prev_model_eval_image, use_container_width=True, disabled=(len(st.session_state.model_eval_image_paths) <= 1), key="prev_eval_btn")
            with col_status_eval:
                st.markdown(f"<p style='text-align:center; margin-top: 00px;'>Image {st.session_state.current_model_eval_index + 1} of {len(st.session_state.model_eval_image_paths)}</p>", unsafe_allow_html=True)
            with col_next_eval:
                st.button("Next", on_click=next_model_eval_image, use_container_width=True, disabled=(len(st.session_state.model_eval_image_paths) <= 1), key="next_eval_btn")

        try:
            with open("MCO2/taal_lake.jpg", "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            st.markdown("---")
            st.markdown(
                f"""
                <div style='text-align: center; margin-top: 10px; margin-bottom: 20px;'>
                    <img src='data:image/png;base64,{encoded}' style='width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px;' />
                    <div style='color: #555; margin-top: 5px;'>Image from: The Shoestring Diaries</div>
                </div>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Error: Image 'taal_lake.jpg' not found.")
        except Exception as e:
            st.error(f"Error displaying image: {e}")

# --- Tab 2: Dataset Information ---
with tab2:
    st.header("Dataset Overview")
    st.markdown(
        "<div class='custom-label' style='margin-bottom: 0px;'>Get a quick summary of the raw datasets before analysis.</div>",
        unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-bottom: 20px; margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
    <b>Welcome to the Dataset Overview Tab!</b>  
    This section provides a summary of the raw datasets used in the analysis. Here, you can check the size of each dataset, see which parameters have missing values, and preview sample records. Understanding this information is important before moving to deeper analysis and modeling, as it highlights the quality and completeness of the data collected from <b>BFAR</b> (for water quality) and <b>PHIVOLCS</b> (for volcanic activity).
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("MCO2/BFAR.png", width=100)
        st.subheader("BFAR Dataset (Water Quality)")
        st.markdown(f"**Shape:** {bfar_df.shape[0]} rows × {bfar_df.shape[1]} columns")
        bfar_missing = bfar_df.isnull().sum()
        bfar_missing_top3 = bfar_missing.sort_values(ascending=False).head(3)
        st.markdown("**Top 3 Parameters with Missing Values:**")
        for param, count in bfar_missing_top3.items():
            st.markdown(f"- **{param}**: {count} missing values")
        st.markdown(f"**Total Missing Cells:** {bfar_missing.sum()} cells")
        st.markdown("**Preview:**")
        st.dataframe(bfar_df.head(20), height=300)
    with col2:
        st.image("MCO2/PHILVOLCS.png", width=100)
        st.subheader("PHIVOLCS Dataset (Volcanic Activity)")
        st.markdown(f"**Shape:** {philvolcs_df.shape[0]} rows × {philvolcs_df.shape[1]} columns")
        philvolcs_missing = philvolcs_df.isnull().sum()
        philvolcs_missing_top3 = philvolcs_missing.sort_values(ascending=False).head(3)
        st.markdown("**Top 3 Parameters with Missing Values:**")
        for param, count in philvolcs_missing_top3.items():
            st.markdown(f"- **{param}**: {count} missing values")
        st.markdown(f"**Total Missing Cells:** {philvolcs_missing.sum()} cells")
        st.markdown("**Preview:**")
        st.dataframe(philvolcs_df.head(20), height=300)
    st.markdown("""
        <div style='margin-bottom: 10px; margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
        The dataset used was gathered from the Bureau of Fisheries and Aquatic Resources (BFAR) Region IV-A, containing the water quality data of Taal Lake collected from the years 2013 to 2023. This dataset includes water quality parameters including water temperature, pH level, ammonia-N, nitrite-N, phosphate, and dissolved oxygen. In addition, it provides weather-related factors such as weather conditions, wind direction, and air temperature. An additional dataset was obtained from the Philippine Institute of Volcanology and Seismology (PHIVOLCS), which contains volcanic parameters recorded from 2022 to 2025. These parameters consist of the number of eruptions, seismic activity, acidity levels, temperature, sulfur dioxide emissions, volcanic plumes, and ground deformation. 
        </div>
        """, unsafe_allow_html=True)

# --- Tab 3: Exploratory Data Analysis (EDA) ---
with tab3:
    st.header("Exploratory Data Analysis")
    st.markdown("""
    <div style='margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
    <b>Welcome to the Exploratory Data Analysis (EDA) Tab!</b>  
    Here, we take a closer look at the key patterns, trends, and relationships within the dataset. By visualizing the distribution of water quality parameters, weather conditions, and seismic activity, this section helps uncover important insights about Taal Lake's environment. The charts and summaries below are designed to make complex data easier to understand, supporting better monitoring and decision-making.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="column-wrapper">', unsafe_allow_html=True)
    col1, space, col2 = st.columns([2, 0.1, 2])
    with col1:
        st.markdown("<div class='section-header'>Distribution of Data by Month</div>", unsafe_allow_html=True)
        def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        try:
            img_path = "MCO2/eda/dpm.png"
            img_base64 = get_base64_of_bin_file(img_path)
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src='data:image/png;base64,{img_base64}' style='margin-top:75px; margin-bottom:75px;width:100%; height:auto;'>
                </div>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Error: Trend image 'eda/dpm.png' not found.")
        except Exception as e:
            st.error(f"Error displaying trend image: {e}")
        with st.expander("View Description"):
            st.markdown("""
            <div style='margin-top: 20px; font-size: 16px; text-align: justify; color: #333333;'>
            <b>Analysis:</b> The distribution of data after cleaning reveals a more consistent and reliable pattern across 
            the months. By removing duplicates, missing values, and outliers, the dataset now reflects the true underlying 
            trends in Taal Lake's water quality parameters. Notably, the cleaned data shows clear seasonal variations, with 
            certain months exhibiting higher or lower concentrations depending on environmental and volcanic activity. The 
            removal of noise and errors has enhanced the visibility of these patterns, allowing for more accurate analysis 
            and prediction. 
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Seismicity Over Time</div>", unsafe_allow_html=True)
        try:
            img_path = "MCO2/eda/seis.png"
            img_base64 = get_base64_of_bin_file(img_path)
            st.markdown(f"""
                <div style='text-align: center;'>
                    <img src='data:image/png;base64,{img_base64}' style='margin-bottom: 76px; width:100%; height:auto;'>
                </div>
                """, unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Error: Seismicity image 'seis.png' not found.")
        except Exception as e:
            st.error(f"Error displaying seismicity image: {e}")
        with st.expander("View Description"):
            st.markdown("""
                <div style='margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
                <b>Analysis:</b> The chart displays several clear spikes in seismic activity during 2022 and 2023.
                <ul>
                    <li>The highest peaks are visible in early 2022 and early 2023, marking significant volcanic or tectonic movements.</li>
                    <li>Between these peaks, seismic activity stays low, indicating stable periods.</li>
                    <li>A slight increase towards late 2023 may suggest early signs of underground changes.</li>
                    <li>Overall, the pattern shows that seismicity in Taal Lake occurs in bursts rather than following a steady trend.</li>
                </ul>
                This is typical in volcanic lakes where both tectonic shifts and magma activity influence seismic behavior.
                </div>
                """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='section-header'>Correlation Heatmap</div>", unsafe_allow_html=True)
        numeric_columns = combined_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_columns = st.multiselect(
            "Select parameters for correlation heatmap",
            options=numeric_columns,
            default=numeric_columns[:min(5, len(numeric_columns))],
            key="heatmap_eda"  # Unique key for EDA tab
        )
        if selected_columns:
            correlation_matrix = combined_df[selected_columns].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title('Correlation Heatmap')
            st.pyplot(plt)
            plt.clf()
        else:
            st.warning("Please select at least one parameter to display the correlation heatmap.")
        with st.expander("View Description"):
            st.markdown("""
            <div style='margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
            <b>Analysis:</b> This heatmap shows how different water quality factors in Taal Lake are connected:
            <ul>
                <li><b>pH and Phosphate</b> are closely linked — when phosphate levels go up, pH tends to rise too.</li>
                <li>Over time, as the <b>years pass</b> and the <b>temperature increases</b>, the <b>pH drops</b>, meaning the lake is becoming a little more acidic.</li>
                <li><b>Phosphate and Acidity</b> also go hand in hand, meaning higher nutrients can raise acidity levels.</li>
                <li>The <b>temperature</b> has been rising over the years, which matches warming trends seen in the data.</li>
                <li><b>Seismic activity</b> doesn’t show a strong direct connection with the water quality in this chart, which suggests the effects are more complex.</li>
            </ul>
            In short, this chart tells us that <b>temperature and nutrients</b> are big drivers of changes in <b>pH and acidity</b> — key signs of the lake’s health.
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div class='section-header'> Weather Distribution</div>", unsafe_allow_html=True)
        try:
            st.image("MCO2/eda/wd.png")
        except FileNotFoundError:
            st.error(f"Error: Image 'eda/wd.png' not found.")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
        with st.expander("View Description"):
            st.markdown("""
            <div style='margin-top: 10px; font-size: 16px; text-align: justify; color: #333333;'>
            <b>Analysis:</b> This chart shows the common weather conditions in the area:
            <ul>
                <li><b>Sunny</b> days happen the most, meaning there is plenty of sunlight throughout the year.</li>
                <li><b>Cloudy</b> and <b>partly cloudy</b> days are also frequent, showing mixed weather patterns.</li>
                <li><b>Rainy</b> days, like those with rainshowers, are rare, meaning rain doesn’t happen very often.</li>
            </ul>
            Knowing this is helpful because <b>weather affects the lake</b>. More sun can warm up the water, while even rare rain can bring in things that change the water quality.
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section-header'> Parameter Distribution</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 2])
    with col1:
        try:
            st.image("MCO2/eda/pardis.png", use_container_width=True)
        except FileNotFoundError:
            st.error("Error: Image 'eda/pardis.png' not found.")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    with col2:
        with st.expander("View Description"):
            st.markdown("""
                This distribution plot shows the spread of water quality parameters after data cleaning. 
                Outliers have been reduced, and trends are now clearer, reflecting more accurate 
                environmental patterns in Taal Lake. This cleaned dataset helps ensure the reliability 
                of further modeling and predictions.
            """)
with tab3:
    st.markdown("<div class='section-header'> Boxplots</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 2])
    with col1:
        try:
            st.image("MCO2/eda/box.png", use_container_width=True)
        except FileNotFoundError:
            st.error("Error: Image 'eda/box.png' not found.")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    with col2:
        with st.expander("View Description"):
            st.markdown("""
                This distribution plot shows the spread of water quality parameters after data cleaning. 
                Outliers have been reduced, and trends are now clearer, reflecting more accurate 
                environmental patterns in Taal Lake. This cleaned dataset helps ensure the reliability 
                of further modeling and predictions.
            """)

# --- Tab 4: Prediction ---
with tab4:
    st.header("Model Prediction")
    st.markdown(
        "<div class='custom-label'>This section presents model predictions and performance comparisons.</div>",
        unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top: 10px; margin-bottom: 20px; font-size: 16px; text-align: justify; color: #333333;'>
    <b>Welcome to the Prediction Tab!</b>  
    In this section, we showcase the models used to predict <b>pH levels</b> in Taal Lake, based on environmental and volcanic activity data. Here, you can compare the performance of different machine learning models — including <b>LSTM</b>, <b>CNN</b>, and a <b>Hybrid CNN-LSTM</b> model. The evaluation results, accuracy scores, and prediction charts will help you see which model offers the best performance for monitoring and forecasting water quality. This comparison provides valuable insights for selecting the most effective approach for future predictions.
    </div>
    """, unsafe_allow_html=True)

def show_image(filepath, caption, width_percent=80):
    try:
        with open(filepath, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style='text-align: center; margin-top: 20px; margin-bottom: 20px;'>
                <img src='data:image/png;base64,{encoded}' style='width: {width_percent}%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px;' />
                <div style='color: #555; margin-top: 5px;'>{caption}</div>
            </div>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: Image '{filepath}' not found.")
    except Exception as e:
        st.error(f"Error displaying image: {e}")

with tab4:
    st.markdown("<div class='section-header'> Model Loss Comparison</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: justify; margin-top: 0px; width: 100%;'>
            This figure shows the training and validation loss curves for all three models. 
            It helps visualize how quickly and effectively each model learned over epochs and whether overfitting or underfitting occurred.
        </div>
        """, unsafe_allow_html=True)
    show_image("MCO2/prediction/loss.png", "CNN Model Loss", width_percent=80)
    st.markdown("<div class='section-header'> Actual vs Predicted Model Comparison</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 4])
    with col1:
        show_image("MCO2/prediction/actpred1.png", "Actual vs Predicted pH (All Models)", width_percent=90)
    with col2:
        st.markdown("""
        <div style='text-align: justify; margin-top: 20px; width: 100%;'>
            This code evaluates and visualizes the prediction performance of three deep learning models: CNN, LSTM, and a Hybrid CNN-LSTM, in estimating pH levels from water quality data.
            <br><br>
            It first obtains predicted pH values from each model using a test dataset and consolidates them with the actual values into a DataFrame.
            <br><br>
            Using Seaborn, it then generates a scatter plot that compares actual versus predicted pH values, allowing for a visual assessment of each model's accuracy and consistency.
            <br><br>
            The scatter plot uses distinct colors for each model to highlight differences in prediction behavior.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div class='section-header'> Individual Model Predictions</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: justify; margin-top: 0px; margin-bottom: 0px; width: 100%;'>
            This scatter plot visualizes the relationship between actual pH values and those predicted by the three models, allowing easy identification of prediction accuracy and outliers.
        </div>
        """, unsafe_allow_html=True)
    show_image("MCO2/prediction/actpred.png", "Actual vs Predicted pH (All Models)", width_percent=80)
    st.markdown("<div class='section-header'> Model Performance (MAE & RMSE)</div>", unsafe_allow_html=True)
    col1, space, col2 = st.columns([12, 0.01, 10])
    with col1:
        show_image("MCO2/prediction/metric.png", "Model Performance: MAE & RMSE", width_percent=90)
    with col2:
        st.markdown("""
        <div style='text-align: justify; margin-top: 50px;'>
            This figure highlights the combined comparison of model predictions using different colors per model, providing a side-by-side visual of predictive performance.
            <br><br>
            It includes the reported MAE and RMSE scores:
            <ul>
                <li><b>CNN</b> (MAE: 0.0360, RMSE: 0.0516)</li>
                <li><b>LSTM</b> (MAE: 0.0387, RMSE: 0.0518)</li>
                <li><b>Hybrid CNN-LSTM</b> (MAE: 0.0303, RMSE: 0.0407)</li>
            </ul>
            These results confirm that the <b>hybrid approach (CNN-LSTM)</b> yields more precise pH predictions.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div class='section-header'> Water Quality Index (WQI) Distribution</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 4])
    with col2:
        st.markdown("<div style='margin-top: 50px;'>", unsafe_allow_html=True)
        show_image("MCO2/WQI.png", "Water Quality Index Distribution", width_percent=90)
        st.markdown("</div>", unsafe_allow_html=True)
    with col1:
        st.markdown("""
        <div style='text-align: justify; margin-top: 20px;'>
            The distribution of the predicted Water Quality Index (WQI), as visualized in the histogram, reveals a bimodal pattern with peaks around the 0.05–0.10 and 0.32–0.35 ranges.
            <br><br>
            Despite these clusters suggesting varying levels of predicted water quality, all 1,198 samples were ultimately classified under the "Poor" category. 
            This outcome stems from the computed WQI values being consistently below the threshold typically associated with higher quality categories (e.g., Fair or Good).
            <br><br>
            The summary statistics support this observation: the mean WQI is only 0.231, and even the maximum value of 0.4207 remains below commonly accepted thresholds for fair water quality (often around 0.5 or higher).
            <br><br>
            The sample WQI values further demonstrate the narrow and low range of the index, which may be influenced by the placeholder approach used to simulate values for multiple parameters (all derived from a single predicted pH value). 
            This suggests that while the model-generated predictions offer a structured output, the derived WQI lacks the diversity expected in real-world data and may not yet accurately reflect actual water quality conditions.
        </div>
        """, unsafe_allow_html=True)

# --- Tab 5: Recommendations ---
with tab_recommendations:
    st.header("Recommendations for Future Work")
    st.markdown("""
    <div style='margin-bottom: 20px; margin-top: 0px; font-size: 16px; text-align: justify; color: #333333;'>
    Based on the current study, the following recommendations are proposed to create a more comprehensive system for predicting water quality in Taal Lake:
    </div>
    """, unsafe_allow_html=True)
    st.subheader("1. Enhance WQI Computation")
    st.markdown("""
    * **Integrate More Parameters:** Incorporate predicted values for dissolved oxygen, ammonia, and nitrate into the Water Quality Index (WQI) calculation to better evaluate diverse water quality conditions.
    * **Validate Classification Boundaries:** Compare the computed WQI with field measurements to establish and refine accurate classification thresholds.
    """)
    st.subheader("2. Expand and Diversify the Dataset")
    st.markdown("""
    * **Extend Data Collection:** Continue data collection beyond 2025 and increase the number of sampling points to improve coverage and potentially detect rapid events like volcanic impacts sooner.
    * **Incorporate Geospatial Data:** Include coordinates for sampling sites to enable mapping visualizations and spatial modeling.
    """)
    st.subheader("3. Refine and Compare Models")
    st.markdown("""
    * **Optimize Hyperparameters:** Employ methods like grid search and Bayesian optimization to fine-tune model hyperparameters, aiming for further reduction in prediction errors.
    """)
    st.subheader("4. Improve Dashboard and Deployment")
    st.markdown("""
    * **Enable Real-Time Monitoring:** Integrate real-time data feeds from agencies such as PHIVOLCS and BFAR to transition the dashboard into a live monitoring system.
    * **Add Interactive Maps:** Enhance the user experience by allowing interaction with geospatial displays or maps showing water quality data.
    """)
    st.subheader("5. Strengthen Stakeholder Engagement and Field Validation")
    st.markdown("""
    * **Collaborate for Field Validation:** Work closely with environmental agencies to obtain field-tested data, crucial for validating the model's real-world performance.
    * **Gather User Feedback:** Actively seek input from resource managers and local community members to define essential dashboard features and effective ways to visualize and report data.
    """)
    st.markdown("---")
    st.markdown("""
    <div style='font-size: 18px; text-align: center; color: #555555; margin-top: 20px;'>
    <i>These recommendations aim to build upon the current system, fostering a more robust, accurate, and user-centric tool for Taal Lake's environmental management.</i>
    </div>
    """, unsafe_allow_html=True)

# Footer Section
st.markdown("---")
now = datetime.datetime.now()
current_time_str = now.strftime("%A, %B %d, %Y at %I:%M:%S %p")
st.caption(f"Taal Lake Dashboard | BULASO - DENNA - EJERCITADO - ESPINO - INCIONG | {current_time_str}")
st.markdown("---")
