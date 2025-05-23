import streamlit as st
import base64
import pandas as pd
import numpy as np
import plotly.express as px

# ==== PAGE CONFIG ====
st.set_page_config(page_title="Water Quality Dashboard", page_icon="📊", layout="wide")

# ==== LOAD FONT ====
font_base64 = None
try:
    with open("Montserrat-Bold.ttf", "rb") as f:
        font_base64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    st.warning("Montserrat-Bold.ttf not found. Using default font.")

# ==== LOAD BANNER IMAGE ====
banner_img_base64 = None
try:
    with open("images/header.png", "rb") as img_file:
        banner_img_base64 = base64.b64encode(img_file.read()).decode()
except FileNotFoundError:
    st.warning("header.png not found. Using solid background for tabs.")

# ==== LOAD DATA ====
@st.cache_data
def load_data():
    bfar_df = pd.DataFrame()
    philvolcs_df = pd.DataFrame()
    try:
        bfar_df = pd.read_csv('datasets/cleaned_dataset.csv')
        if 'Date' in bfar_df.columns:
            bfar_df['Date'] = pd.to_datetime(bfar_df['Date'], errors='coerce')
        else:
            st.error("'cleaned_dataset.csv' must contain a 'Date' column.")
            bfar_df = pd.DataFrame()
        numeric_cols = ['Year', 'Month', 'Surface Temperature', 'Middle Temperature', 'pH', 'Ammonia',
                        'Nitrate', 'Phosphate', 'Dissolved Oxygen', 'Air Temperature', 'Seismicity',
                        'Acidity', 'Temperature (in Celsius)', 'SO2', 'Plume (in meters)', 'Ground Deformation']
        for col in numeric_cols:
            if col in bfar_df.columns:
                bfar_df[col] = pd.to_numeric(bfar_df[col], errors='coerce')
    except FileNotFoundError:
        st.error("cleaned_dataset.csv not found.")
    except Exception as e:
        st.error(f"Error loading cleaned_dataset.csv: {e}")

    try:
        philvolcs_df = pd.read_csv('datasets/PHIVOLCS.csv')
        if 'Date' in philvolcs_df.columns:
            philvolcs_df['Date'] = pd.to_datetime(philvolcs_df['Date'], errors='coerce')
    except FileNotFoundError:
        st.error("PHIVOLCS.csv not found.")
    except Exception as e:
        st.error(f"Error loading PHIVOLCS.csv: {e}")

    return bfar_df, philvolcs_df

bfar_df, philvolcs_df = load_data()

# ==== LOAD TAAL INFO ====
taal_info = ""
try:
    with open("taalinfo.txt", "r") as f:
        taal_info = f.read()
except FileNotFoundError:
    st.warning("taalinfo.txt not found.")

# ==== CSS STYLING ====
font_style = f"""
@font-face {{
    font-family: 'Montserrat';
    src: url("data:font/ttf;base64,{font_base64}") format('truetype');
}}
""" if font_base64 else ""

tab_style = f"""
.stTabs [data-baseweb="tab-list"] {{
    background-image: linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0)), 
    url("data:image/png;base64,{banner_img_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    padding: 30px;
    border-radius: 8px 8px 0px 0px;
}}
""" if banner_img_base64 else """
.stTabs [data-baseweb="tab-list"] {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    margin-bottom: 0px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
"""

st.markdown(f"""
<style>
    {font_style}
    .block-container {{
        max-width: 1200px !important;
        padding: 3rem 0rem !important;
        margin: 0 auto !important;
    }}
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .section-header, .custom-label, .stTabs [data-baseweb="tab"] p,
    .stButton button, .stMultiSelect, .streamlit-expanderHeader p, .streamlit-expanderContent div,
    .custom-text-primary, .custom-text-secondary {{
        font-family: {'Montserrat' if font_base64 else 'sans-serif'} !important;
    }}
    /* Selected parameters in multiselect (background and text color) */
    .stMultiSelect [data-baseweb="select"] .st-ae {{
        background-color: #004A99 !important;
        color: #FFFFFF !important;
    }}
    /* Checkbox styling (including Select All Parameters) */
    .stCheckbox input {{
        accent-color: #004A99 !important;
    }}
    /* Checkbox label text color */
    .stCheckbox label {{
        color: #222831 !important;
    }}
    /* Outline of dropdown menus (selectbox and multiselect) */
    [data-baseweb="select"] > div {{
        border: 1px solid #004A99 !important;
        border-radius: 8px !important;
    }}
    {tab_style}
    .stTabs [data-baseweb="tab-panel"] {{
        padding: 0px 5px 5px 5px ;
        margin: 0 0 0 0;
    }}

    .stTabs [data-baseweb="tab-list"] {{ 10px; gap: 25px; justify-content: right; }}
    .stTabs [data-baseweb="tab"] {{ 
        background-color: rgba(128, 150, 173, 0.5);
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        border: none !important;
        padding: 20px;
        backdrop-filter: blur(5px);
    }}
    .stTabs [data-baseweb="tab"] p {{ 
        color: #002244;
        font-weight: 600;
        margin: 0;
        font-size: 15px;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ 
        background-color: rgba(88, 139, 206, 0.5) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(2px);
    }}
    .stTabs [data-baseweb="tab"]:hover p {{ color: #FFFFFF !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ display: none !important; }}
    .stTabs [aria-selected="true"] {{ 
        background-color: rgba(0, 74, 173, 0.95) !important;
        color: #ffffff !important;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.4);
        transform: translateY(-3px);
    }}
    .stTabs [aria-selected="true"] p {{ color: #ffffff !important; }}
    .custom-divider {{ border-top: 1px solid #748DA6; margin-top: 10px; margin-bottom:15px ; }}
    .custom-text-primary {{ color: #222831; font-size: 18px; padding-top: 0px; }}
    .custom-text-secondary {{ color: #393E46; font-size: 16px; }}
</style>
""", unsafe_allow_html=True)

# ==== TABS ====
tab1, tab3, tab4, tab_info = st.tabs(["🏠 Homepage", "📈 Visualizations", "🔮 Prediction", "ℹ️ About"])

# ==== TAB 1: Homepage ====
# ==== TAB 1: Homepage ====
with tab1:
    # Add CSS to style the full-width GIF
    st.markdown("""
    <style>
    .full-width-gif {
        max-width: 2000px; /* Matches .block-container max-width */
        display: block;
        margin: 0 auto; /* Center the GIF */
        margin-top: 3rem; /* Move GIF upward to offset block-container padding */
        border-radius: 8px; /* Add rounded corners */
    }
    .greeting-message {
        text-align: center;
        margin-bottom: 1rem; /* Space between greeting and GIF */
    }
    </style>
    """, unsafe_allow_html=True)

    # Load and display the GIF
    try:
        with open("images/homepage.gif", "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f'<img src="data:image/gif;base64,{img_base64}" class="full-width-gif" alt="Homepage GIF">',
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("homepage.gif not found in the images folder. Please ensure the file exists.")
    except Exception as e:
        st.error(f"Error loading homepage.gif: {e}")

with tab3:
    # Initialize session state for visualization selection
    if 'visualization' not in st.session_state:
        st.session_state.visualization = "Correlation Matrix"

    # Update CSS to style buttons
    st.markdown("""
    <style>
    [data-testid="stButton"] button {
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        background-color: rgba(128, 150, 173, 0.15) !important;
        border-radius: 8px !important;
        padding: 0px 15px !important;
        width: 180px !important; 
        text-align: center !important;
        color: #002244 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        font-family: Montserrat, sans-serif !important;
        border: none !important;
        margin-bottom: 0px !important;
        cursor: pointer !important;
        display: block !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.);
    }
    [data-testid="stButton"] button:hover {
        background-color: rgba(88, 139, 206, 0.5) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.0);
        transform: translateX(5px);
    }
    [data-testid="stButton"] button[kind="primary"] {
        background-color: #004A99 !important; 
        color: #FFFFFF !important;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0);
        transform: translateX(5px);
    }
    [data-testid="stButton"] button:active {
        background-color: #003366 !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transform: translateX(5px);
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    colA, colB = st.columns([1, 5])
    with colA:
        st.markdown(
            "<div class='custom-text-primary' style='margin-bottom: 10px; margin-top: 0px; "
            "font-size: 15px; text-align: justify;'>Select a Visualization</div>",
            unsafe_allow_html=True)
        # Visualization buttons
        visualization_options = [
            "Correlation Matrix",
            "Scatter Plots",
            "Distributions",
            "Histogram",
            "Box Plot",
            "Line Chart"
        ]
        for option in visualization_options:
            # Determine if this button is selected
            is_selected = st.session_state.visualization == option
            st.button(
                option,
                key=f"vis_button_{option.lower().replace(' ', '_')}",
                on_click=lambda opt=option: st.session_state.update(visualization=opt),
                type="primary" if is_selected else "secondary"
            )
        visualization = st.session_state.visualization

    with colB:
        if visualization == "Correlation Matrix":
            if not bfar_df.empty:
                available_sites = sorted(bfar_df['Site'].astype(str).unique())
                numeric_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                        if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition', 'Wind Direction']
                                        and bfar_df[col].notna().any()])
                col1, col2 = st.columns([5, 2])
                with col2:
                    st.markdown(
                        "<div class='custom-text-primary' style='margin-bottom: 00px; margin-top: 0px; "
                        "font-size: 15px; text-align: justify;'>Correlation Matrix Configuration</div>",
                        unsafe_allow_html=True)
                    sites = ['All Sites'] + available_sites
                    selected_site = st.selectbox("Select Site:", sites, key="heatmap_site")
                    select_all_params = st.checkbox("Select All Parameters", key="heatmap_select_all_params")
                    selected_params = st.multiselect(
                        "Select Parameters (min 2):",
                        options=numeric_params,
                        default=numeric_params if select_all_params else numeric_params[:min(len(numeric_params), 5)],
                        key="heatmap_params"
                    )
                    min_date = bfar_df['Date'].min()
                    max_date = bfar_df['Date'].max()
                    start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date, max_value=max_date,
                                            key="heatmap_start_date")
                    end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date, max_value=max_date,
                                            key="heatmap_end_date")
                with col1:
                    try:
                        filtered_df = bfar_df.copy()
                        if selected_site != 'All Sites':
                            filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                        if start_date:
                            start_date = pd.to_datetime(start_date)
                            filtered_df = filtered_df[filtered_df['Date'] >= start_date]
                        if end_date:
                            end_date = pd.to_datetime(end_date)
                            filtered_df = filtered_df[filtered_df['Date'] <= end_date]
                        if start_date and end_date and start_date > end_date:
                            st.error("Error: Start date cannot be after end date.")
                        elif len(selected_params) < 2:
                            st.info("Please select at least two parameters for the correlation heatmap.")
                        else:
                            corr_df = filtered_df[selected_params].dropna()
                            if len(corr_df) < 2:
                                st.warning("Not enough data points after filtering to calculate correlation.")
                            else:
                                corr_matrix = corr_df.corr()
                                if not corr_matrix.empty:
                                    fig_heatmap = px.imshow(
                                        corr_matrix,
                                        text_auto=True,
                                        aspect="auto",
                                        color_continuous_scale='Blues',
                                        title=f"Correlation Matrix for {selected_site}"
                                    )
                                    fig_heatmap.update_traces(
                                        xgap=0,
                                        ygap=0
                                    )
                                    fig_heatmap.update_layout(
                                        xaxis_title="Parameters",
                                        yaxis_title="Parameters",
                                        height=550,
                                        plot_bgcolor='white',
                                        paper_bgcolor='white',
                                        title_font=dict(
                                            size=18,
                                            family='Montserrat' if font_base64 else 'sans-serif'
                                        ),
                                        title_x=0.03,
                                        margin=dict(l=00, r=0, t=40, b=0),
                                        font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                    )
                                    fig_heatmap.update_xaxes(tickangle=45)
                                    fig_heatmap.update_yaxes(tickangle=0)
                                    st.plotly_chart(fig_heatmap, use_container_width=True)
                                else:
                                    st.warning("No correlation data to display.")
                    except Exception as e:
                        st.error(f"Error generating heatmap: {e}")
            else:
                st.error("Water Quality data not loaded. Cannot display heatmap.")

        elif visualization == "Scatter Plots":
            if not bfar_df.empty:
                numeric_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                         if
                                         col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition', 'Wind Direction']
                                         and bfar_df[col].notna().any()])
                if len(numeric_params) < 2:
                    st.warning("At least two numeric parameters are required for scatter plots.")
                else:
                    col1, col2 = st.columns([5, 2])
                    with col2:
                        st.markdown(
                            "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
                            "font-size: 17px; text-align: justify;'>Scatter Plot Configuration</div>",
                            unsafe_allow_html=True)
                        x_axis = st.selectbox("Select X-axis Parameter:", numeric_params, key="scatter_x")
                        y_axis = st.selectbox("Select Y-axis Parameter:", numeric_params,
                                              index=1 if len(numeric_params) > 1 else 0, key="scatter_y")
                        sites = ['All Sites'] + sorted(bfar_df['Site'].astype(str).unique())
                        selected_site = st.selectbox("Filter by Site (Optional):", sites, key="scatter_site_filter")
                        min_date = bfar_df['Date'].min()
                        max_date = bfar_df['Date'].max()
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date,
                                                   key="scatter_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date, max_value=max_date,
                                                 key="scatter_end_date")
                    with col1:
                        filtered_df = bfar_df.copy()
                        if selected_site != 'All Sites':
                            filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                        if start_date and end_date:
                            start_date = pd.to_datetime(start_date)
                            end_date = pd.to_datetime(end_date)
                            if start_date > end_date:
                                st.error("Error: Start date cannot be after end date.")
                            else:
                                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                          (filtered_df['Date'] <= end_date)]
                        elif start_date:
                            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                        elif end_date:
                            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                        filtered_df = filtered_df.dropna(subset=[x_axis, y_axis])
                        if not filtered_df.empty:
                            fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='Site',
                                                     title=f"{y_axis} vs. {x_axis}", hover_data=['Date'])
                            fig_scatter.update_layout(
                                height=500,
                                plot_bgcolor='white',
                                paper_bgcolor='white',
                                title_font=dict(
                                    size=18,
                                    family='Montserrat' if font_base64 else 'sans-serif'
                                ),
                                title_x=0.03,
                                margin=dict(l=00, r=0, t=40, b=0),
                                font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)
                        else:
                            st.warning("No data available for the selected parameters and filters.")
            else:
                st.error("Water Quality data not loaded. Cannot display scatter plots.")
        elif visualization == "Distributions":
            if not bfar_df.empty or not philvolcs_df.empty:
                bfar_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                      if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition',
                                                     'Wind Direction']
                                      and bfar_df[col].notna().any()])
                philvolcs_params = sorted([col for col in philvolcs_df.select_dtypes(include=np.number).columns
                                           if col not in ['Year', 'Month', 'Day', 'Latitude', 'Longitude']
                                           and philvolcs_df[col].notna().any()])
                param_options = ([f"{param} (Water Quality)" for param in bfar_params] +
                                 [f"{param} (PHIVOLCS)" for param in philvolcs_params])
                if not param_options:
                    st.warning("No numeric parameters available for distribution plots.")
                else:
                    col1, col2 = st.columns([5, 2])
                    with col2:
                        st.markdown(
                            "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
                            "font-size: 17px; text-align: justify;'>Distributions Configuration</div>",
                            unsafe_allow_html=True)
                        selected_param = st.selectbox("Select Parameter for Distribution:", param_options,
                                                      index=0, key="dist_param")
                        sites = ['All Sites'] + sorted(bfar_df['Site'].astype(str).unique()) if not bfar_df.empty else [
                            'All Sites']
                        selected_site = st.selectbox("Filter by Site (Optional, Water Quality only):", sites,
                                                     key="dist_site_filter")
                        min_date = bfar_df['Date'].min() if not bfar_df.empty else philvolcs_df['Date'].min()
                        max_date = bfar_df['Date'].max() if not bfar_df.empty else philvolcs_df['Date'].max()
                        show_trend_line = st.checkbox("Show Trend Line", value=False, key="dist_trend_line")
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date,
                                                   key="dist_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date,
                                                 max_value=max_date,
                                                 key="dist_end_date")
                    with col1:
                        param_name = selected_param.split(" (")[0]
                        dataset = selected_param.split(" (")[1].rstrip(")")
                        if dataset == "Water Quality" and not bfar_df.empty:
                            filtered_df = bfar_df.copy()
                            if selected_site != 'All Sites':
                                filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                        elif dataset == "PHIVOLCS" and not philvolcs_df.empty:
                            filtered_df = philvolcs_df.copy()
                        else:
                            filtered_df = pd.DataFrame()
                        if not filtered_df.empty:
                            if start_date and end_date:
                                start_date = pd.to_datetime(start_date)
                                end_date = pd.to_datetime(end_date)
                                if start_date > end_date:
                                    st.error("Error: Start date cannot be after end date.")
                                else:
                                    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                              (filtered_df['Date'] <= end_date)]
                            elif start_date:
                                filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                            elif end_date:
                                filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                            data = filtered_df[param_name].dropna()
                            title = f"Distribution of {param_name} ({dataset}) in {selected_site}"
                            if not data.empty:
                                fig_hist = px.histogram(data, x=param_name, nbins=30, title=title,
                                                        color_discrete_sequence=['#004A99'])
                                fig_hist.update_traces(opacity=0.75)
                                if show_trend_line:
                                    from scipy.stats import gaussian_kde
                                    import numpy as np
                                    kde = gaussian_kde(data)
                                    x_range = np.linspace(data.min(), data.max(), 100)
                                    kde_vals = kde(x_range)
                                    # Scale KDE to match histogram height
                                    hist_height = data.size  # Approximate height per bin
                                    kde_vals_scaled = kde_vals * hist_height * (data.max() - data.min()) / 30
                                    fig_hist.add_scatter(
                                        x=x_range,
                                        y=kde_vals_scaled,
                                        mode='lines',
                                        name='KDE Trend',
                                        showlegend=False,  # Hide in legend
                                        line=dict(color='red', width=2)
                                    )
                                fig_hist.update_layout(
                                    showlegend=False,  # No legend for histogram or KDE
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    height=500,
                                    xaxis_title=param_name,
                                    title_font=dict(
                                        size=18,
                                        family='Montserrat' if font_base64 else 'sans-serif'
                                    ),
                                    title_x=0.03,
                                    margin=dict(l=00, r=0, t=40, b=0),
                                    yaxis_title="Count",
                                    font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                )
                                st.plotly_chart(fig_hist, use_container_width=True)
                            else:
                                st.warning(f"No data available for {selected_param} after applying filters.")
                        else:
                            st.warning(f"No data available for {selected_param}.")
        elif visualization == "Histogram":
            if not bfar_df.empty or not philvolcs_df.empty:
                bfar_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                      if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition',
                                                     'Wind Direction']
                                      and bfar_df[col].notna().any()])
                philvolcs_params = sorted([col for col in philvolcs_df.select_dtypes(include=np.number).columns
                                           if col not in ['Year', 'Month', 'Day', 'Latitude', 'Longitude']
                                           and philvolcs_df[col].notna().any()])
                param_options = ([f"{param} (Water Quality)" for param in bfar_params] +
                                 [f"{param} (PHIVOLCS)" for param in philvolcs_params])
                if not param_options:
                    st.warning("No numeric parameters available for histogram.")
                else:
                    col1, col2 = st.columns([5, 2])
                    with col2:
                        st.markdown(
                            "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
                            "font-size: 17px; text-align: justify;'>Histogram Configuration</div>",
                            unsafe_allow_html=True)
                        selected_param = st.selectbox("Select Parameter for Histogram:", param_options,
                                                      index=0, key="hist_param")
                        sites = ['All Sites'] + sorted(bfar_df['Site'].astype(str).unique()) if not bfar_df.empty else [
                            'All Sites']
                        selected_site = st.selectbox("Filter by Site (Optional, Water Quality only):", sites,
                                                     key="hist_site_filter")
                        min_date = bfar_df['Date'].min() if not bfar_df.empty else philvolcs_df['Date'].min()
                        max_date = bfar_df['Date'].max() if not bfar_df.empty else philvolcs_df['Date'].max()
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date,
                                                   key="hist_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date,
                                                 max_value=max_date,
                                                 key="hist_end_date")
                    with col1:
                        param_name = selected_param.split(" (")[0]
                        dataset = selected_param.split(" (")[1].rstrip(")")
                        if dataset == "Water Quality" and not bfar_df.empty:
                            filtered_df = bfar_df.copy()
                            if selected_site != 'All Sites':
                                filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                        elif dataset == "PHIVOLCS" and not philvolcs_df.empty:
                            filtered_df = philvolcs_df.copy()
                        else:
                            filtered_df = pd.DataFrame()
                        if not filtered_df.empty:
                            if start_date and end_date:
                                start_date = pd.to_datetime(start_date)
                                end_date = pd.to_datetime(end_date)
                                if start_date > end_date:
                                    st.error("Error: Start date cannot be after end date.")
                                else:
                                    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                              (filtered_df['Date'] <= end_date)]
                            elif start_date:
                                filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                            elif end_date:
                                filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                            data = filtered_df[param_name].dropna()
                            title = f"Histogram of {param_name} ({dataset}) in {selected_site}"
                            if not data.empty:
                                fig_hist = px.histogram(data, x=param_name, nbins=30, title=title,
                                                        color_discrete_sequence=['#004A99'])
                                fig_hist.update_traces(opacity=0.75)
                                fig_hist.update_layout(
                                    showlegend=False,
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    height=500,
                                    title_font=dict(
                                        size=18,
                                        family='Montserrat' if font_base64 else 'sans-serif'
                                    ),
                                    title_x=0.03,
                                    margin=dict(l=00, r=0, t=40, b=0),
                                    xaxis_title=param_name,
                                    yaxis_title="Count",
                                    font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                )
                                st.plotly_chart(fig_hist, use_container_width=True)
                            else:
                                st.warning(f"No data available for {selected_param} after applying filters.")
                        else:
                            st.warning(f"No data available for {selected_param}.")
            else:
                st.error("No data loaded. Cannot display histogram.")

        elif visualization == "Box Plot":
            if not bfar_df.empty or not philvolcs_df.empty:
                bfar_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                      if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition',
                                                     'Wind Direction']
                                      and bfar_df[col].notna().any()])
                philvolcs_params = sorted([col for col in philvolcs_df.select_dtypes(include=np.number).columns
                                           if col not in ['Year', 'Month', 'Day', 'Latitude', 'Longitude']
                                           and philvolcs_df[col].notna().any()])
                param_options = ([f"{param} (Water Quality)" for param in bfar_params] +
                                 [f"{param} (PHIVOLCS)" for param in philvolcs_params])
                if not param_options:
                    st.warning("No numeric parameters available for box plot.")
                else:
                    col1, col2 = st.columns([5, 2])
                    with col2:
                        st.markdown(
                            "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
                            "font-size: 17px; text-align: justify;'>Box Plot Configuration</div>",
                            unsafe_allow_html=True)
                        selected_param = st.selectbox("Select Parameter for Box Plot:", param_options,
                                                      index=0, key="box_param")
                        sites = ['All Sites'] + sorted(bfar_df['Site'].astype(str).unique()) if not bfar_df.empty else [
                            'All Sites']
                        selected_site = st.selectbox("Filter by Site (Optional, Water Quality only):", sites,
                                                     key="box_site_filter")
                        min_date = bfar_df['Date'].min() if not bfar_df.empty else philvolcs_df['Date'].min()
                        max_date = bfar_df['Date'].max() if not bfar_df.empty else philvolcs_df['Date'].max()
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date,
                                                   key="box_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date,
                                                 max_value=max_date,
                                                 key="box_end_date")
                    with col1:
                        param_name = selected_param.split(" (")[0]
                        dataset = selected_param.split(" (")[1].rstrip(")")
                        if dataset == "Water Quality" and not bfar_df.empty:
                            filtered_df = bfar_df.copy()
                            if selected_site != 'All Sites':
                                filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                        elif dataset == "PHIVOLCS" and not philvolcs_df.empty:
                            filtered_df = philvolcs_df.copy()
                        else:
                            filtered_df = pd.DataFrame()
                        if not filtered_df.empty:
                            if start_date and end_date:
                                start_date = pd.to_datetime(start_date)
                                end_date = pd.to_datetime(end_date)
                                if start_date > end_date:
                                    st.error("Error: Start date cannot be after end date.")
                                else:
                                    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                              (filtered_df['Date'] <= end_date)]
                            elif start_date:
                                filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                            elif end_date:
                                filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                            data = filtered_df[[param_name]].dropna(subset=[param_name])
                            title = f"Box Plot of {param_name} ({dataset}) in {selected_site}"
                            if not data.empty:
                                fig_box = px.box(data, x=param_name, title=title,
                                                 color_discrete_sequence=['#004A99'])
                                fig_box.update_traces(marker=dict(size=5, opacity=0.75))
                                # Calculate tick values for x-axis
                                min_val = data[param_name].min()
                                max_val = data[param_name].max()
                                tick_vals = np.linspace(min_val, max_val, num=10).round(2)  # 10 evenly spaced ticks
                                fig_box.update_xaxes(
                                    tickvals=tick_vals,
                                    ticktext=[f"{val:.2f}" for val in tick_vals],
                                    gridcolor='rgba(200, 200, 200, 0.5)',
                                    showgrid=True,
                                    zeroline=False
                                )
                                fig_box.update_layout(
                                    showlegend=False,
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    title_font=dict(
                                        size=18,
                                        family='Montserrat' if font_base64 else 'sans-serif'
                                    ),
                                    title_x=0.03,
                                    margin=dict(l=00, r=0, t=40, b=0),
                                    xaxis_title=param_name,
                                    yaxis_title="",
                                    font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                )
                                st.plotly_chart(fig_box, use_container_width=True)
                            else:
                                st.warning(f"No data available for {selected_param} after applying filters.")
                        else:
                            st.warning(f"No data available for {selected_param}.")

        elif visualization == "Line Chart":
            if not bfar_df.empty or not philvolcs_df.empty:
                bfar_params = sorted([col for col in bfar_df.select_dtypes(include=np.number).columns
                                      if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition', 'Wind Direction']
                                      and bfar_df[col].notna().any()])
                philvolcs_params = sorted([col for col in philvolcs_df.select_dtypes(include=np.number).columns
                                           if col not in ['Year', 'Month', 'Day', 'Latitude', 'Longitude']
                                           and philvolcs_df[col].notna().any()])
                param_options = ([f"{param} (Water Quality)" for param in bfar_params] +
                                 [f"{param} (PHIVOLCS)" for param in philvolcs_params])
                if not param_options:
                    st.warning("No numeric parameters available for line chart.")
                else:
                    col1, col2 = st.columns([5, 2])
                    with col2:
                        st.markdown(
                            "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
                            "font-size: 17px; text-align: justify;'>Line Chart Configuration</div>",
                            unsafe_allow_html=True)
                        compare_mode = st.radio("Compare By:", ["Parameters", "Sites"], index=0, key="line_compare_mode", horizontal=True)
                        if compare_mode == "Parameters":
                            selected_params = st.multiselect("Select Parameters for Comparison (at least 1):",
                                                             param_options,
                                                             default=[param_options[0]] if param_options else [],
                                                             key="line_params")
                            sites = ['All Sites'] + sorted(bfar_df['Site'].astype(str).unique()) if not bfar_df.empty else [
                                'All Sites']
                            selected_site = st.selectbox("Filter by Site (Optional, Water Quality only):", sites,
                                                         key="line_site_filter")
                        else:  # Compare Sites
                            if not bfar_df.empty:
                                selected_param = st.selectbox("Select Parameter for Comparison:", param_options,
                                                              index=0, key="line_param")
                                sites = sorted(bfar_df['Site'].astype(str).unique())
                                selected_sites = st.multiselect("Select Sites for Comparison (at least 1):", sites,
                                                                default=[sites[0]] if sites else [], key="line_sites")
                            else:
                                st.warning("Site comparison is only available for Water Quality data.")
                                selected_param = None
                                selected_sites = []
                        min_date = bfar_df['Date'].min() if not bfar_df.empty else philvolcs_df['Date'].min()
                        max_date = bfar_df['Date'].max() if not bfar_df.empty else philvolcs_df['Date'].max()
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date,
                                                   key="line_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date, max_value=max_date,
                                                 key="line_end_date")
                    with col1:
                        if compare_mode == "Parameters":
                            if not selected_params:
                                st.warning("Please select at least one parameter for the line chart.")
                            else:
                                # Extract dataset and parameter names
                                datasets = [param.split(" (")[1].rstrip(")") for param in selected_params]
                                param_names = [param.split(" (")[0] for param in selected_params]
                                # Check if all parameters are from the same dataset
                                if len(set(datasets)) > 1:
                                    st.error(
                                        "Please select parameters from the same dataset (either Water Quality or PHIVOLCS).")
                                else:
                                    dataset = datasets[0]
                                    if dataset == "Water Quality" and not bfar_df.empty:
                                        filtered_df = bfar_df.copy()
                                        if selected_site != 'All Sites':
                                            filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                                    elif dataset == "PHIVOLCS" and not philvolcs_df.empty:
                                        filtered_df = philvolcs_df.copy()
                                    else:
                                        filtered_df = pd.DataFrame()
                                    if not filtered_df.empty:
                                        if start_date and end_date:
                                            start_date = pd.to_datetime(start_date)
                                            end_date = pd.to_datetime(end_date)
                                            if start_date > end_date:
                                                st.error("Error: Start date cannot be after end date.")
                                            else:
                                                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                                          (filtered_df['Date'] <= end_date)]
                                        elif start_date:
                                            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                                        elif end_date:
                                            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                                        data = filtered_df[['Date'] + param_names].dropna(subset=param_names)
                                        data = data.sort_values('Date')
                                        if not data.empty:
                                            melted_data = data.melt(id_vars=['Date'], value_vars=param_names,
                                                                    var_name='Parameter', value_name='Value')
                                            title = f"Line Chart of Selected Parameters ({dataset})"
                                            fig_line = px.line(melted_data, x='Date', y='Value', color='Parameter',
                                                               title=title)
                                            fig_line.update_traces(line=dict(width=2))
                                            fig_line.update_layout(
                                                showlegend=True,
                                                plot_bgcolor='white',
                                                paper_bgcolor='white',
                                                height=500,
                                                title_font=dict(
                                                    size=18,
                                                    family='Montserrat' if font_base64 else 'sans-serif'
                                                ),
                                                title_x=0.03,
                                                margin=dict(l=00, r=0, t=40, b=0),
                                                xaxis_title="Date",
                                                yaxis_title="Value",
                                                font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                            )
                                            st.plotly_chart(fig_line, use_container_width=True)
                                        else:
                                            st.warning(
                                                f"No data available for the selected parameters after applying filters.")
                                    else:
                                        st.warning(f"No data available for the selected parameters.")
                        else:  # Compare Sites
                            if not bfar_df.empty:
                                if not selected_sites:
                                    st.warning("Please select at least one site for the line chart.")
                                else:
                                    param_name = selected_param.split(" (")[0]
                                    dataset = selected_param.split(" (")[1].rstrip(")")
                                    if dataset != "Water Quality":
                                        st.error("Site comparison is only available for Water Quality data.")
                                    else:
                                        filtered_df = bfar_df.copy()
                                        filtered_df = filtered_df[filtered_df['Site'].isin(selected_sites)]
                                        if start_date and end_date:
                                            start_date = pd.to_datetime(start_date)
                                            end_date = pd.to_datetime(end_date)
                                            if start_date > end_date:
                                                st.error("Error: Start date cannot be after end date.")
                                            else:
                                                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                                          (filtered_df['Date'] <= end_date)]
                                        elif start_date:
                                            filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                                        elif end_date:
                                            filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                                        data = filtered_df[['Date', 'Site', param_name]].dropna(subset=[param_name])
                                        data = data.sort_values('Date')
                                        if not data.empty:
                                            title = f"Line Chart of {param_name} Across Sites (Water Quality)"
                                            fig_line = px.line(data, x='Date', y=param_name, color='Site',
                                                               title=title)
                                            fig_line.update_traces(line=dict(width=2))
                                            fig_line.update_layout(
                                                showlegend=True,
                                                plot_bgcolor='white',
                                                paper_bgcolor='white',
                                                height=500,
                                                title_font=dict(
                                                    size=18,
                                                    family='Montserrat' if font_base64 else 'sans-serif'
                                                ),
                                                title_x=0.03,
                                                margin=dict(l=00, r=0, t=40, b=0),
                                                xaxis_title="Date",
                                                yaxis_title=param_name,
                                                font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                            )
                                            st.plotly_chart(fig_line, use_container_width=True)
                                        else:
                                            st.warning(
                                                f"No data available for {param_name} at the selected sites after applying filters.")
                            else:
                                st.error("No Water Quality data loaded. Cannot display site comparison.")
            else:
                st.error("No data loaded. Cannot display line chart.")

# ==== TAB 4: Prediction ====
with tab4:
    st.info("This section is under development.")

# ==== TAB INFO: About ====
with tab_info:
    st.markdown(
        "<div class='custom-text-primary' style='font-size: 22px; text-align: justify;'>Dataset Information</div>",
        unsafe_allow_html=True)

    # Load uncleaned datasets for overview
    bfar_raw_df = pd.DataFrame()
    philvolcs_raw_df = pd.DataFrame()
    try:
        bfar_raw_df = pd.read_csv('datasets/BFAR.csv')
    except FileNotFoundError:
        st.error("BFAR.csv not found.")
    except Exception as e:
        st.error(f"Error loading BFAR.csv: {e}")

    try:
        philvolcs_raw_df = pd.read_csv('datasets/PHIVOLCS.csv')
    except FileNotFoundError:
        st.error("PHIVOLCS.csv not found.")
    except Exception as e:
        st.error(f"Error loading PHIVOLCS.csv: {e}")

    col1, col2, col3 = st.columns([10, 0.5, 10])
    with col1:
        colA, colB, colC = st.columns([3, 0.05, 10])
        with colA:
            try:
                st.image("images/BFAR.png", width=100)
            except FileNotFoundError:
                st.warning("BFAR.png not found.")
        with colC:
            st.markdown("""
                <div class='custom-text-primary' style='margin-top: 23px; font-size: 30px; text-align: left; color: #023AA8;'>Water Quality Dataset</div>
                <div class='custom-text-secondary' style='color: #4E94DC; font-size: 15px; text-align: left;'>(Source: BFAR.csv)</div>
            """, unsafe_allow_html=True)
        if not bfar_raw_df.empty:
            st.markdown(f"**Shape:** {bfar_raw_df.shape[0]} rows × {bfar_raw_df.shape[1]} columns")
            missing = bfar_raw_df.isnull().sum()
            missing_filtered = missing[missing > 0]
            if not missing_filtered.empty:
                st.markdown("**Top 3 Parameters with Missing Values:**")
                for param, count in missing_filtered.sort_values(ascending=False).head(3).items():
                    st.markdown(f"- **{param}**: {count} missing values")
            else:
                st.markdown("No missing values in the Water Quality dataset.")
            st.markdown(f"**Total Missing Cells:** {missing.sum()} cells")
            with st.expander("Water Quality Dataset Preview (First 20 rows)"):
                st.dataframe(bfar_raw_df.head(20), height=250)
        else:
            st.warning("Water Quality data (BFAR.csv) not loaded.")

    with col3:
        colA_ph, colB_ph, colC_ph = st.columns([3, 0.05, 10])
        with colA_ph:
            try:
                st.image("images/PHIVOLCS.png", width=100)
            except FileNotFoundError:
                st.warning("PHIVOLCS.png not found.")
        with colC_ph:
            st.markdown("""
                <div class='custom-text-primary' style='margin-top: 18px; font-size: 30px; text-align: left; color: #222831;'>PHIVOLCS Dataset</div>
                <div class='custom-text-secondary' style='margin-bottom: 27px;color: #43B5C3; font-size: 18px; text-align: left;'>(Volcanic Activity, Source: PHIVOLCS.csv)</div>
            """, unsafe_allow_html=True)
        if not philvolcs_raw_df.empty:
            st.markdown(f"**Shape:** {philvolcs_raw_df.shape[0]} rows × {philvolcs_raw_df.shape[1]} columns")
            missing = philvolcs_raw_df.isnull().sum()
            missing_filtered = missing[missing > 0]
            if not missing_filtered.empty:
                st.markdown("**Top 3 Parameters with Missing Values:**")
                for param, count in missing_filtered.sort_values(ascending=False).head(3).items():
                    st.markdown(f"- **{param}**: {count} missing values")
            else:
                st.markdown("No missing values in the PHIVOLCS dataset.")
            st.markdown(f"**Total Missing Cells:** {missing.sum()} cells")
            with st.expander("PHIVOLCS Dataset Preview (First 20 rows)"):
                st.dataframe(philvolcs_raw_df.head(20), height=250)
        else:
            st.warning("PHIVOLCS data (PHIVOLCS.csv) not loaded.")

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-text-primary' style='margin-bottom:15px; font-size: 23px; text-align: justify;'>About Taal Lake</div>",
                unsafe_allow_html=True)
    col_taal1, col_taal2, col_taal3 = st.columns([5, 0.5, 10])
    with col_taal1:
        try:
            st.image("images/Taal-volcano-map.jpg", caption="Image from: ShelterBox USA")
        except FileNotFoundError:
            st.warning("Taal-volcano-map.jpg not found.")
    with col_taal3:
        st.markdown(f"<div style='text-align: justify; font-size: 19px; color: #393E46;'>{taal_info}</div>",
                    unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class='custom-text-primary' style='font-size: 23px; text-align: justify;'>About the Developers</div>
        <div class='custom-text-primary' style='font-size: 15px; text-align: justify; margin-bottom:25px; '>Group 2 - BS CPE 3-1</div>
    """, unsafe_allow_html=True)

    developers = [
        {"name": "BULASO, DAVE PATRICK I.", "phone": "+63XXXXXXXXXX", "email": "main.davepatrick.bulaso@cvsu.edu.ph",
         "img": "1x1/dave.jpg"},
        {"name": "DENNA, ALEXA YVONNE V.", "phone": "+639184719122", "email": "main.alexayvonne.denna@cvsu.edu.ph",
         "img": "1x1/alexa.jpg"},
        {"name": "EJERCITADO, JOHN MARTIN P.", "phone": "+639262333664",
         "email": "main.johnmartin.ejercitado@cvsu.edu.ph>  }", "img": "1x1/martin.png"},
        {"name": "ESPINO, GIAN JERICHO Z.", "phone": "+639108733830", "email": "main.gianjericho.espino@cvsu.edu.ph",
         "img": "1x1/gian.jpg"},
        {"name": "INCIONG, HARLEY EVANGEL J.", "phone": "+639516120316",
         "email": "main.harleyevangel.inciong@cvsu.edu.ph", "img": "1x1/harley.jpg"},
    ]

    dev_col1, dev_col2, dev_col3 = st.columns(3)
    cols = [dev_col1, dev_col2, dev_col3]
    for i, dev in enumerate(developers):
        with cols[i % 3]:
            try:
                st.image(dev["img"], width=100)
            except FileNotFoundError:
                st.warning(f"{dev['img']} not found.")
            st.markdown(f"**{dev['name']}**<br>Phone: {dev['phone']}<br>Email: {dev['email']}", unsafe_allow_html=True)
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)