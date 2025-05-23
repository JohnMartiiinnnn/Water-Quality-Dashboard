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
        bfar_df = pd.read_parquet('datasets/cleaned_dataset.parquet', engine='pyarrow')
    except FileNotFoundError:
        st.error("cleaned_dataset.parquet not found.")
    except Exception as e:
        st.error(f"Error loading cleaned_dataset.parquet: {e}")

    try:
        philvolcs_df = pd.read_parquet('datasets/PHIVOLCS.parquet', engine='pyarrow')
    except FileNotFoundError:
        st.error("PHIVOLCS.parquet not found.")
    except Exception as e:
        st.error(f"Error loading PHIVOLCS.parquet: {e}")

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
        max-width: 98% !important;
        padding: 3rem 0rem 3rem 0rem !important;  # Adjusted bottom padding for footer
        margin: 0 5px 5px 5px !important;
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
        border: 0px solid #004A99 !important;
        border-radius: 8px !important;
    }}
    {tab_style}
    .stTabs [data-baseweb="tab-panel"] {{
        padding: 0px 5px 5px 5px;
        margin: 0 0 0 0;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 25px; justify-content: right; padding-right: 3rem; }}
    
    .stTabs [data-baseweb="tab"] {{ 
        background-color: rgba(128, 150, 173, 0.5);
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        border: none !important;
        padding: 20px;
        backdrop-filter: blur(2px);
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
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        transform: translateY(-3px);
    }}
    .stTabs [aria-selected="true"] p {{ color: #ffffff !important; }}
    .custom-divider {{ border-top: 1px solid #748DA6; margin-top: 10px; margin-bottom:15px; }}
    .custom-text-primary {{ color: #222831; font-size: 18px; padding-top: 0px; }}
    .custom-text-secondary {{ color: #393E46; font-size: 16px; }}
    
    .full-width-footer {{
        max-width: 100% !important;
        display: block;
        margin: 0 auto;
        border-radius: 0 0 8px 8px;
        width: 100%;
        position: relative;
        bottom: 0;
    }}
</style>
""", unsafe_allow_html=True)

# ==== TABS ====
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Homepage"

def set_active_tab(tab):
    st.session_state.active_tab = tab

tab1, tab3, tab4, tab_info = st.tabs(["🏠 Homepage", "📈 Visualizations", "🔮 Prediction", "ℹ️ About"])

with tab1:
    set_active_tab("Homepage")
    st.markdown("""
    <style>
    .full-width-gif {
        max-width: 100% !important;
        display: block;
        margin: 0 auto;
        margin-top: 1rem;
        border-radius: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

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

    st.markdown("<div class='custom-divider' style='margin-bottom: 7rem;'></div>", unsafe_allow_html=True)

with tab3:
    set_active_tab("Visualizations")
    if 'visualization' not in st.session_state:
        st.session_state.visualization = "Correlation Matrix"

    st.markdown("""
    <style>
    [data-testid="stButton"] button {
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        background-color: rgba(128, 150, 173, 0.15) !important;
        border-radius: 8px !important;
        padding: 0px 13px !important;
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
    div.js-plotly-plot {
        border: 2px solid #004A99 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 0px 5px rgba(0, 0, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    colA, colB = st.columns([1, 5])
    with colA:
        st.markdown(
            "<div class='custom-text-primary' style='margin-bottom: 10px; margin-top: 0px; "
            "font-size: 15px; text-align: justify;'>Select a Visualization</div>",
            unsafe_allow_html=True)
        visualization_options = [
            "Correlation Matrix",
            "Scatter Plots",
            "Distributions",
            "Histogram",
            "Box Plot",
            "Line Chart",
            "Descriptive Analytics",
        ]
        for option in visualization_options:
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
                                         if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition',
                                                        'Wind Direction']
                                         and bfar_df[col].notna().any()])
                col1, col2 = st.columns([5, 2])
                with col2:
                    st.markdown(
                        "<div class='custom-text-primary' style='margin-bottom: 0px; margin-top: 0px; "
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
                    start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                               max_value=max_date,
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
                                corr_matrix = corr_df.corr().round(2)
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
                                        margin=dict(l=20, r=20, t=60, b=20),
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
                                         if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition',
                                                        'Wind Direction']
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
                        show_best_fit = st.checkbox("Show Best-Fit Line", value=True, key="scatter_best_fit")
                        min_date = bfar_df['Date'].min()
                        max_date = bfar_df['Date'].max()
                        start_date = st.date_input("Start Date (Optional):", value=None, min_value=min_date,
                                                   max_value=max_date, key="scatter_start_date")
                        end_date = st.date_input("End Date (Optional):", value=None, min_value=min_date,
                                                 max_value=max_date, key="scatter_end_date")

                    with col1:
                        try:
                            filtered_df = bfar_df.copy()
                            if selected_site != 'All Sites':
                                filtered_df = filtered_df[filtered_df['Site'] == selected_site]
                            if start_date and end_date:
                                start_date = pd.to_datetime(start_date)
                                end_date = pd.to_datetime(end_date)
                                if start_date > end_date:
                                    st.error("Error: Start date cannot be after end date.")
                                    st.stop()
                                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) &
                                                          (filtered_df['Date'] <= end_date)]
                            elif start_date:
                                filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
                            elif end_date:
                                filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
                            filtered_df = filtered_df.dropna(subset=[x_axis, y_axis])
                            if filtered_df.empty:
                                st.warning("No data available for the selected parameters and filters.")
                                st.stop()
                            if len(filtered_df) < 2:
                                st.warning("Not enough data points (minimum 2 required) to generate scatter plot.")
                                st.stop()
                            if not (filtered_df[x_axis].dtype in [np.float64, np.int64] and
                                    filtered_df[y_axis].dtype in [np.float64, np.int64]):
                                st.error("Selected parameters must be numeric for scatter plot.")
                                st.stop()
                            fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='Site',
                                                     title=f"{y_axis} vs. {x_axis}", hover_data=['Date'])
                            if show_best_fit:
                                try:
                                    x_data = filtered_df[x_axis].values
                                    y_data = filtered_df[y_axis].values
                                    coeffs = np.polyfit(x_data, y_data, 1)
                                    slope, intercept = coeffs
                                    x_range = np.array([x_data.min(), x_data.max()])
                                    y_fit = slope * x_range + intercept
                                    fig_scatter.add_scatter(
                                        x=x_range,
                                        y=y_fit,
                                        mode='lines',
                                        name='Best Fit',
                                        line=dict(color='red', width=2)
                                    )
                                except Exception as e:
                                    st.warning(f"Unable to compute best-fit line: {str(e)}")
                            fig_scatter.update_layout(
                                height=500,
                                plot_bgcolor='white',
                                paper_bgcolor='white',
                                title_font=dict(
                                    size=18,
                                    family='Montserrat' if font_base64 else 'sans-serif'
                                ),
                                title_x=0.03,
                                margin=dict(l=20, r=20, t=60, b=20),
                                font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                            )
                            st.plotly_chart(fig_scatter, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error generating scatter plot: {str(e)}")
                            st.stop()
            else:
                st.error("Water Quality data not loaded. Cannot display scatter plots.")
                st.stop()

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
                                    try:
                                        from scipy.stats import gaussian_kde
                                        import numpy as np
                                        if len(data) >= 2 and data.nunique() > 1:
                                            kde = gaussian_kde(data)
                                            x_range = np.linspace(data.min(), data.max(), 100)
                                            kde_vals = kde(x_range)
                                            hist_height = data.size
                                            kde_vals_scaled = kde_vals * hist_height * (data.max() - data.min()) / 30
                                            fig_hist.add_scatter(
                                                x=x_range,
                                                y=kde_vals_scaled,
                                                mode='lines',
                                                name='KDE Trend',
                                                showlegend=False,
                                                line=dict(color='red', width=2)
                                            )
                                        else:
                                            st.warning(
                                                "Not enough data or variability in the selected range to compute KDE trend line.")
                                    except Exception as e:
                                        st.warning(
                                            "Not enough data or variability in the selected range to compute KDE trend line.")
                                fig_hist.update_layout(
                                    showlegend=False,
                                    plot_bgcolor='white',
                                    paper_bgcolor='white',
                                    height=500,
                                    xaxis_title=param_name,
                                    title_font=dict(
                                        size=18,
                                        family='Montserrat' if font_base64 else 'sans-serif'
                                    ),
                                    title_x=0.03,
                                    margin=dict(l=20, r=20, t=60, b=20),
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
                                    margin=dict(l=20, r=20, t=60, b=20),
                                    xaxis_title=param_name,
                                    yaxis_title="Count",
                                    font=dict(family='Montserrat' if font_base64 else 'sans-serif')
                                )
                                st.plotly_chart(fig_hist, use_container_width=True)
                            else:
                                st.warning(f"No data available for {selected_param} after applying filters.")
                        else:
                            st.warning(f"No data available for {selected_param}.")

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
                                min_val = data[param_name].min()
                                max_val = data[param_name].max()
                                tick_vals = np.linspace(min_val, max_val, num=10).round(2)
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
                                    height=500,
                                    title_font=dict(
                                        size=18,
                                        family='Montserrat' if font_base64 else 'sans-serif'
                                    ),
                                    title_x=0.03,
                                    margin=dict(l=20, r=20, t=60, b=20),
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
                        else:
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
                                datasets = [param.split(" (")[1].rstrip(")") for param in selected_params]
                                param_names = [param.split(" (")[0] for param in selected_params]
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
                                                margin=dict(l=20, r=20, t=60, b=20),
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
                        else:
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
                                                margin=dict(l=20, r=20, t=60, b=20),
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

        elif visualization == "Descriptive Analytics":
            if not bfar_df.empty:
                st.markdown(
                    "<div class='custom-text-primary' style='margin-bottom: 8px; margin-top: 0px; "
                    "font-size: 20px; text-align: justify;'>Descriptive Analytics</div>",
                    unsafe_allow_html=True)
                numeric_params = [col for col in bfar_df.select_dtypes(include=np.number).columns
                                  if col not in ['Date', 'Site', 'Year', 'Month', 'Weather Condition', 'Wind Direction']
                                  and bfar_df[col].notna().any()]
                if numeric_params:
                    stats_df = bfar_df[numeric_params].describe().T
                    stats_df = stats_df[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
                    stats_df = stats_df.rename(columns={
                        'count': 'Count',
                        'mean': 'Mean',
                        'std': 'Std Dev',
                        'min': 'Min',
                        '25%': 'Q1',
                        '50%': 'Median',
                        '75%': 'Q3',
                        'max': 'Max'
                    })
                    stats_df = stats_df.round(2)
                    st.dataframe(stats_df, use_container_width=True)
                else:
                    st.warning("No numeric parameters available for descriptive analytics.")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Water Quality data not loaded. Cannot display analytics or overview.")

with tab4:
    pass

with tab_info:
    set_active_tab("About")
    st.markdown(
        "<div class='custom-text-primary' style='font-size: 22px; text-align: justify;'>Dataset Information</div>",
        unsafe_allow_html=True)

    bfar_raw_df = pd.DataFrame()
    philvolcs_raw_df = pd.DataFrame()
    try:
        bfar_raw_df = pd.read_parquet('datasets/BFAR.parquet', engine='pyarrow')
    except FileNotFoundError:
        st.error("BFAR.parquet not found.")
    except Exception as e:
        st.error(f"Error loading BFAR.parquet: {e}")

    try:
        philvolcs_raw_df = pd.read_parquet('datasets/PHIVOLCS.parquet', engine='pyarrow')
    except FileNotFoundError:
        st.error("PHIVOLCS.parquet not found.")
    except Exception as e:
        st.error(f"Error loading PHIVOLCS.parquet: {e}")

    col1, col2, col3 = st.columns([10, 0.5, 10])
    with col1:
        colA, colB, colC = st.columns([3, 0.05, 10])
        with colA:
            try:
                with open("images/BFAR.png", "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                st.markdown(
                    f'<img src="data:image/png;base64,{img_base64}" width="100" alt="BFAR Logo">',
                    unsafe_allow_html=True
                )
            except FileNotFoundError:
                st.warning("BFAR.png not found in the images folder. Please ensure the file exists in the repository.")
            except Exception as e:
                st.error(f"Error loading BFAR.png: {e}")
        with colC:
            st.markdown(""" 
                <div class='custom-text-primary' style='margin-top: 23px; font-size: 30px; text-align: left; color: #023AA8;'>Water Quality Dataset</div>
                <div class='custom-text-secondary' style='margin-bottom: 27px; color: #4E94DC; font-size: 15px; text-align: left;'>(BFAR)</div>
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
            st.warning("Water Quality data (BFAR.parquet) not loaded.")

    with col3:
        colA_ph, colB_ph, colC_ph = st.columns([3, 0.05, 10])
        with colA_ph:
            try:
                with open("images/PHIVOLCS.png", "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                st.markdown(
                    f'<img src="data:image/png;base64,{img_base64}" width="100" alt="PHIVOLCS Logo">',
                    unsafe_allow_html=True
                )
            except FileNotFoundError:
                st.warning("PHIVOLCS.png not found in the images folder. Please ensure the file exists in the repository.")
            except Exception as e:
                st.error(f"Error loading PHIVOLCS.png: {e}")
        with colC_ph:
            st.markdown(""" 
                <div class='custom-text-primary' style='margin-top: 18px; font-size: 30px; text-align: left; color: #222831;'>PHIVOLCS Dataset</div>
                <div class='custom-text-secondary' style='margin-bottom: 27px;color: #43B5C3; font-size: 18px; text-align: left;'>(Volcanic Activity)</div>
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
            st.warning("PHIVOLCS data (PHIVOLCS.parquet) not loaded.")

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-text-primary' style='margin-bottom:15px; font-size: 23px; text-align: justify;'>About Taal Lake</div>",
                unsafe_allow_html=True)
    col_taal1, col_taal2, col_taal3 = st.columns([5, 0.5, 10])
    with col_taal1:
        try:
            with open("images/Taal-volcano-map.jpg", "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'<img src="data:image/jpeg;base64,{img_base64}" alt="Taal Volcano Map" style="width: 100%;">',
                unsafe_allow_html=True
            )
            st.caption("Image from: ShelterBox USA")
        except FileNotFoundError:
            st.warning("Taal-volcano-map.jpg not found in the images folder. Please ensure the file exists in the repository.")
        except Exception as e:
            st.error(f"Error loading Taal-volcano-map.jpg: {e}")
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
         "email": "main.johnmartin.ejercitado@cvsu.edu.ph", "img": "1x1/martin.png"},
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
                with open(dev["img"], "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{img_base64}" width="100" alt="{dev["name"]} Photo">',
                    unsafe_allow_html=True
                )
            except FileNotFoundError:
                st.warning(f"{dev['img']} not found in the 1x1 folder. Please ensure the file exists in the repository.")
            except Exception as e:
                st.error(f"Error loading {dev['img']}: {e}")
            st.markdown(f"**{dev['name']}**<br>Phone: {dev['phone']}<br>Email: {dev['email']}", unsafe_allow_html=True)

# ==== FOOTER ====
footer_img = "images/footer.png"
try:
    with open(footer_img, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f'<img src="data:image/png;base64,{img_base64}" alt="Footer" class="full-width-footer">',
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.warning(f"{footer_img} not found in the images folder. Please ensure the file exists in the repository.")
except Exception as e:
    st.error(f"Error loading {footer_img}: {e}")
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
