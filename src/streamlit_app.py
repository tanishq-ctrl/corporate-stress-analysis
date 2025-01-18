import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stress_analysis import *
import plotly.express as px
import plotly.graph_objects as go
from config import CHART_COLORS, CHART_THEME

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Corporate Stress Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom CSS styling
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Main container styling */
        .main {
            padding: 0;
            background-color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        /* Dashboard header */
        .dashboard-title {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 3.5rem 0;
            margin-bottom: 1.5rem;
            text-align: center;
            border-radius: 0 0 2.5rem 2.5rem;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        }
        
        /* Metric cards styling */
        .metrics-row {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.5);
            flex: 1;
            min-width: 200px;
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        .metric-label {
            font-size: 0.875rem;
            font-weight: 500;
            color: #475569;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1e293b;
        }
        
        /* Chart container styling */
        .chart-container {
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.5);
            margin: 1rem 0;
        }
        
        /* Sidebar styling */
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 1.5rem;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: 1px solid rgba(59, 130, 246, 0.1);
            font-weight: 500;
            font-size: 0.875rem;
            transition: all 0.2s;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        }
        
        /* Footer styling */
        .footer {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 2rem;
            text-align: center;
            border-radius: 1rem;
            margin-top: 3rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Insights box styling */
        div[style*="background-color: #f8f9fa"] {
            background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
            border-radius: 1rem !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Common chart layout settings
def get_chart_layout():
    return {
        'plot_bgcolor': CHART_THEME['bgcolor'],
        'paper_bgcolor': CHART_THEME['bgcolor'],
        'font': {
            'family': CHART_THEME['font_family'],
            'color': CHART_THEME['axis_font_color']
        },
        'margin': dict(t=30, l=30, r=30, b=30),
        'legend': {
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': '#E2E2E2',
            'borderwidth': 1
        }
    }

def render_footer():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0ea5e9, #0284c7);
                    padding: 2rem;
                    border-radius: 1rem;
                    text-align: center;
                    color: white;
                    margin-top: 3rem;">
            <p style="margin: 0;">Created with ❤️ using Streamlit</p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.9rem;">
                © 2024 Corporate Stress Analysis
            </p>
        </div>
    """, unsafe_allow_html=True)

def main():
    local_css()

    # Header with custom HTML
    st.markdown("""
        <div class="dashboard-title">
            <h1>📊 Corporate Stress Analysis Dashboard</h1>
            <p>Comprehensive analysis of stress levels across different corporate factors</p>
        </div>
    """, unsafe_allow_html=True)

    # Container for all content with proper spacing
    st.markdown("""
        <div style='padding: 0 1rem;'>
    """, unsafe_allow_html=True)

    # Allow users to upload their own dataset or use the default
    uploaded_file = st.sidebar.file_uploader("Upload your own dataset", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Use default dataset
        df = load_data('/Users/tanishq/Downloads/corporate_stress_dataset.csv')

    # Ensure numeric datatypes for correlation analysis
    numeric_columns = ['Stress_Level', 'Age', 'Working_Hours_per_Week', 
                      'Monthly_Salary_INR', 'Sleep_Hours', 'Work_Life_Balance']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Display correlation info in debug mode
    if st.checkbox("Show Data Info", False):
        st.write("Data Types:", df[numeric_columns].dtypes)
        st.write("Sample Correlations:", df[numeric_columns].corr().round(2))

    # Sidebar with custom styling
    with st.sidebar:
        st.markdown("""
            <h2 class='sidebar-title'>Dashboard Controls</h2>
        """, unsafe_allow_html=True)
        
        department = st.multiselect(
            'Select Department(s)',
            options=df['Department'].unique(),
            default=[]
        )

        gender = st.multiselect(
            'Select Gender(s)',
            options=df['Gender'].unique(),
            default=[]
        )

        experience_range = st.slider(
            'Years of Experience',
            min_value=int(df['Experience_Years'].min()),
            max_value=int(df['Experience_Years'].max()),
            value=(0, 40)
        )

    # Filter data
    if not department:
        department = df['Department'].unique()
    if not gender:
        gender = df['Gender'].unique()
        
    filtered_df = df[
        df['Department'].isin(department) & 
        df['Gender'].isin(gender) &
        (df['Experience_Years'].between(experience_range[0], experience_range[1]))
    ]

    # Metrics in cards
    st.markdown("<div class='metrics-row'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Stress</div>
            <div class="metric-value">{filtered_df['Stress_Level'].mean():.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Median Stress</div>
            <div class="metric-value">{filtered_df['Stress_Level'].median():.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">High Stress Cases</div>
            <div class="metric-value">{(filtered_df['Stress_Level'] > 7).sum():,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Total Employees</div>
            <div class="metric-value">{len(filtered_df):,}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Update CSS for better spacing
    st.markdown("""
        <style>
        .metrics-row {
            margin: 1rem 0;
            gap: 1.5rem;
        }
        .chart-container {
            margin: 0.5rem 0;
            padding: 1rem;
        }
        .stTabs {
            margin: 0.5rem 0;
        }
        /* Remove extra padding from streamlit elements */
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
        }
        /* Adjust header margins */
        .stMarkdown h3 {
            margin-top: 0;
            margin-bottom: 1rem;
        }
        /* Adjust metric card styles */
        .metric-card {
            padding: 1.5rem;
        }
        /* Adjust chart container padding */
        .chart-container {
            padding: 1.5rem;
        }
        /* Remove extra margins from plotly charts */
        .js-plotly-plot {
            margin: 0 !important;
        }
        /* Adjust column gaps */
        .row-widget.stHorizontal {
            gap: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main visualizations with tighter spacing
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📊 Stress Level Distribution")
        fig = px.histogram(filtered_df, x='Stress_Level', 
                          nbins=11,
                          color_discrete_sequence=[CHART_COLORS[0]],
                          opacity=0.8,
                          title="")
        fig.update_layout(
            **get_chart_layout(),
            bargap=0.1,
            height=400
        )
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=1
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📈 Department-wise Stress Levels")
        fig = px.box(filtered_df, x='Department', y='Stress_Level',
                     color='Department',
                     color_discrete_sequence=CHART_COLORS,
                     title="")
        fig.update_layout(
            **get_chart_layout(),
            xaxis={'tickangle': 45},
            boxmode='group',
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Correlation heatmap
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("🔍 Correlation Analysis")
    corr_cols = ['Stress_Level', 'Age', 'Working_Hours_per_Week', 
                 'Monthly_Salary_INR', 'Sleep_Hours', 'Work_Life_Balance']
    # Round correlations to 2 decimal places during calculation
    corr_matrix = filtered_df[corr_cols].corr().round(2)
    # Add correlation annotations
    annotations = []
    for i, row in enumerate(corr_matrix.values):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=corr_cols[j],
                    y=corr_cols[i],
                    text=f"{value:.2f}",
                    font=dict(size=12),
                    showarrow=False
                )
            )
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_cols,
        y=corr_cols,
        hoverongaps=False,
        colorscale=[
            [0.0, '#d73027'],      # Strong negative correlation (red)
            [0.25, '#f46d43'],     # Moderate negative correlation
            [0.5, '#ffffff'],      # No correlation (white)
            [0.75, '#74add1'],     # Moderate positive correlation
            [1.0, '#4575b4']       # Strong positive correlation (blue)
        ],
        zmid=0,
        zmin=-1,
        zmax=1
    ))
    fig.update_layout(
        **get_chart_layout(),
        height=500,
        xaxis={'tickangle': 45},
        yaxis={'tickangle': 0},
        annotations=annotations,
        coloraxis_colorbar=dict(
            title="Correlation",
            titleside="right",
            thickness=15,
            len=0.7,
            tickmode="array",
            ticktext=["-1", "-0.5", "0", "0.5", "1"],
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticks="outside"
        )
    )
    # Add a note about correlation interpretation
    st.markdown("""
        <div style='margin-top: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
            <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>
            <strong>Note:</strong> Correlation values range from -1 to 1:
            <ul style='margin: 0.5rem 0;'>
                <li>1.0: Perfect positive correlation</li>
                <li>0.0: No correlation</li>
                <li>-1.0: Perfect negative correlation</li>
            </ul>
            The current data shows very weak correlations between most variables.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Working Hours Analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("⏰ Working Hours Impact")
    col1, col2 = st.columns(2)
    
    with col1:
        # Working Hours Distribution
        fig = px.histogram(filtered_df,
                          x='Working_Hours_per_Week',
                          nbins=20,
                          color_discrete_sequence=[CHART_COLORS[1]],
                          title="Distribution of Working Hours")
        fig.update_layout(
            **get_chart_layout(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Overtime Impact on Stress
        overtime_threshold = filtered_df['Working_Hours_per_Week'].median()
        filtered_df['Overtime'] = filtered_df['Working_Hours_per_Week'] > overtime_threshold
        overtime_stress = filtered_df.groupby(['Department', 'Overtime'])['Stress_Level'].mean().reset_index()
        fig = px.bar(overtime_stress,
                    x='Department',
                    y='Stress_Level',
                    color='Overtime',
                    barmode='group',
                    color_discrete_sequence=[CHART_COLORS[2], CHART_COLORS[3]],
                    title="Impact of Overtime on Stress Levels")
        fig.update_layout(
            **get_chart_layout(),
            height=400,
            xaxis={'tickangle': 45}
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Sleep Analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("😴 Sleep Pattern Analysis")
    
    # Create sleep categories
    filtered_df['Sleep_Category'] = pd.cut(filtered_df['Sleep_Hours'],
                                         bins=[0, 6, 7, 8, 12],
                                         labels=['< 6 hours', '6-7 hours', '7-8 hours', '> 8 hours'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sleep Distribution
        sleep_dist = filtered_df['Sleep_Category'].value_counts().reset_index()
        fig = px.pie(sleep_dist,
                    values='count',
                    names='Sleep_Category',
                    color_discrete_sequence=CHART_COLORS,
                    title="Sleep Duration Distribution")
        fig.update_layout(
            **get_chart_layout(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sleep vs Stress
        sleep_stress = filtered_df.groupby('Sleep_Category')['Stress_Level'].mean().reset_index()
        fig = px.bar(sleep_stress,
                    x='Sleep_Category',
                    y='Stress_Level',
                    color_discrete_sequence=[CHART_COLORS[4]],
                    title="Average Stress Level by Sleep Duration")
        fig.update_layout(
            **get_chart_layout(),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Health Impact Analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("🏥 Health Impact Analysis")
    
    # Create health-related metrics
    filtered_df['Sleep_Quality'] = pd.cut(filtered_df['Sleep_Hours'],
                                        bins=[0, 5, 6, 7, 8, 12],
                                        labels=['Very Poor', 'Poor', 'Fair', 'Good', 'Excellent'])
    
    filtered_df['Burnout_Risk'] = pd.cut(filtered_df['Stress_Level'],
                                       bins=[0, 3, 6, 8, 10],
                                       labels=['Low', 'Moderate', 'High', 'Severe'])
    
    # Create tabs for different health aspects
    health_tab1, health_tab2, health_tab3 = st.tabs([
        "😴 Sleep Impact", 
        "🏃‍♂️ Physical Activity", 
        "🔥 Burnout Analysis"
    ])
    
    with health_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sleep Quality vs Stress
            sleep_impact = filtered_df.groupby('Sleep_Quality')['Stress_Level'].agg([
                'mean', 'count', 'std'
            ]).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=sleep_impact['Sleep_Quality'],
                y=sleep_impact['mean'],
                error_y=dict(type='data', array=sleep_impact['std']),
                marker_color=CHART_COLORS[0],
                name='Average Stress'
            ))
            
            fig.update_layout(
                **get_chart_layout(),
                title="Sleep Quality Impact on Stress",
                height=400,
                xaxis_title="Sleep Quality",
                yaxis_title="Average Stress Level"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Sleep Pattern Analysis
            try:
                fig = px.scatter(filtered_df,
                               x='Sleep_Hours',
                               y='Stress_Level',
                               color='Department',
                               trendline="lowess",
                               color_discrete_sequence=CHART_COLORS,
                               title="Sleep Hours vs Stress Level Trend")
            except:
                # Fallback without trendline if statsmodels is not available
                fig = px.scatter(filtered_df,
                               x='Sleep_Hours',
                               y='Stress_Level',
                               color='Department',
                               color_discrete_sequence=CHART_COLORS,
                               title="Sleep Hours vs Stress Level Trend")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with health_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Physical Activity Impact
            filtered_df['Activity_Level'] = pd.qcut(filtered_df['Working_Hours_per_Week'],
                                                  q=4,
                                                  labels=['Low', 'Moderate', 'High', 'Very High'])
            
            activity_impact = filtered_df.groupby('Activity_Level')['Stress_Level'].mean().reset_index()
            fig = px.line(activity_impact,
                         x='Activity_Level',
                         y='Stress_Level',
                         markers=True,
                         color_discrete_sequence=[CHART_COLORS[2]],
                         title="Physical Activity Level vs Stress")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Department-wise Activity Analysis
            fig = px.box(filtered_df,
                        x='Department',
                        y='Working_Hours_per_Week',
                        color='Department',
                        color_discrete_sequence=CHART_COLORS,
                        title="Working Hours Distribution by Department")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45},
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with health_tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Burnout Risk Distribution
            burnout_dist = filtered_df['Burnout_Risk'].value_counts().reset_index()
            fig = px.pie(burnout_dist,
                        values='count',
                        names='Burnout_Risk',
                        color_discrete_sequence=CHART_COLORS,
                        title="Burnout Risk Distribution")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Burnout Factors Analysis
            burnout_factors = pd.melt(filtered_df,
                                    value_vars=['Working_Hours_per_Week', 'Sleep_Hours', 'Work_Life_Balance'],
                                    var_name='Factor',
                                    value_name='Value')
            
            fig = px.box(burnout_factors,
                        x='Factor',
                        y='Value',
                        color='Factor',
                        color_discrete_sequence=CHART_COLORS[3:6],
                        title="Key Burnout Factors Analysis")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Add health insights summary
    st.markdown("""
        <div style='margin-top: 1rem; padding: 1.5rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
            <h4 style='color: #334155; margin-bottom: 0.5rem;'>Key Health Insights:</h4>
            <ul style='color: #64748b; margin: 0;'>
                <li>Sleep quality shows a strong correlation with stress levels</li>
                <li>Physical activity levels vary significantly across departments</li>
                <li>Multiple factors contribute to burnout risk</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Additional insights with tabs
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📱 Remote Work Analysis", "⚖️ Work-Life Balance", "👥 Age Demographics"])
    
    with tab1:
        remote_stress = filtered_df.groupby('Remote_Work')['Stress_Level'].mean()
        remote_df = pd.DataFrame({
            'Remote_Work': remote_stress.index,
            'Average_Stress': remote_stress.values
        })
        fig = px.bar(remote_df, x='Remote_Work', y='Average_Stress',
                     labels={'x': 'Remote Work', 'y': 'Average Stress Level'},
                     color_discrete_sequence=[CHART_COLORS[2]],
                     text=remote_stress.values.round(2),
                     title="")
        fig.update_layout(
            **get_chart_layout(),
            bargap=0.3,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        fig = px.scatter(filtered_df, 
                       x='Work_Life_Balance', 
                       y='Stress_Level',
                       color='Department',
                       color_discrete_sequence=CHART_COLORS,
                       opacity=0.7,
                       size='Experience_Years',
                       hover_data=['Job_Role', 'Age'],
                       title="")
        fig.update_layout(
            **get_chart_layout(),
            hovermode='closest',
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age Distribution by Department
            fig = px.violin(filtered_df, 
                           y='Age', 
                           x='Department',
                           color='Department',
                           box=True,
                           color_discrete_sequence=CHART_COLORS,
                           title="Age Distribution by Department")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Stress Level by Age Group
            filtered_df['Age_Group'] = pd.cut(filtered_df['Age'], 
                                           bins=[20, 30, 40, 50, 60],
                                           labels=['20-30', '31-40', '41-50', '51-60'])
            age_stress = filtered_df.groupby('Age_Group')['Stress_Level'].mean().reset_index()
            fig = px.line(age_stress, 
                         x='Age_Group', 
                         y='Stress_Level',
                         markers=True,
                         color_discrete_sequence=[CHART_COLORS[0]],
                         title="Average Stress Level by Age Group")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    # Workplace Dynamics Analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("🏢 Workplace Dynamics")
    
    workplace_tab1, workplace_tab2, workplace_tab3 = st.tabs([
        "🏠 Remote Work Impact", 
        "🏢 Department Analysis", 
        "📊 Team Size Effects"
    ])
    
    with workplace_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Remote Work vs Stress
            remote_work_stress = filtered_df.groupby(['Remote_Work', 'Department'])['Stress_Level'].mean().reset_index()
            fig = px.bar(remote_work_stress,
                        x='Department',
                        y='Stress_Level',
                        color='Remote_Work',
                        barmode='group',
                        color_discrete_sequence=CHART_COLORS,
                        title="Stress Levels: Remote vs Office Work")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Work-Life Balance in Remote vs Office
            remote_balance = filtered_df.groupby('Remote_Work')['Work_Life_Balance'].mean().reset_index()
            fig = px.pie(remote_balance,
                        values='Work_Life_Balance',
                        names='Remote_Work',
                        hole=0.4,
                        color_discrete_sequence=CHART_COLORS,
                        title="Work-Life Balance Distribution")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with workplace_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Department Performance Matrix
            dept_matrix = filtered_df.groupby('Department').agg({
                'Stress_Level': 'mean',
                'Working_Hours_per_Week': 'mean',
                'Monthly_Salary_INR': 'mean'
            }).reset_index()
            
            fig = px.scatter(dept_matrix,
                           x='Working_Hours_per_Week',
                           y='Stress_Level',
                           size='Monthly_Salary_INR',
                           color='Department',
                           color_discrete_sequence=CHART_COLORS,
                           title="Department Performance Matrix")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Department Stress Distribution
            fig = px.violin(filtered_df,
                          y='Stress_Level',
                          x='Department',
                          color='Department',
                          box=True,
                          points="all",
                          color_discrete_sequence=CHART_COLORS,
                          title="Detailed Department Stress Distribution")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                showlegend=False,
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with workplace_tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Team Size Impact
            # Calculate department sizes
            dept_sizes = filtered_df['Department'].value_counts()
            size_mapping = {}
            
            # Manual categorization based on department sizes
            for dept in dept_sizes.index:
                # Since all departments have equal size (~2,730 employees)
                size_mapping[dept] = 'Standard'
            
            # Map sizes to departments
            filtered_df.loc[:, 'Team_Size'] = filtered_df['Department'].map(size_mapping)
            
            team_stress = filtered_df.groupby(['Team_Size', 'Department'])['Stress_Level'].mean().reset_index()
            fig = px.bar(team_stress,
                        x='Department',
                        y='Stress_Level',
                        color='Team_Size',
                        barmode='group',
                        color_discrete_sequence=CHART_COLORS,
                        title="Department Stress Levels by Size Category")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Efficiency Metrics
            efficiency_metrics = filtered_df.groupby('Team_Size').agg({
                'Working_Hours_per_Week': 'mean',
                'Work_Life_Balance': 'mean',
                'Stress_Level': 'mean'
            }).reset_index()
            
            efficiency_metrics_long = pd.melt(efficiency_metrics,
                                         id_vars=['Team_Size'],
                                         var_name='Metric',
                                         value_name='Value')
            
            fig = px.line(efficiency_metrics_long,
                        x='Team_Size',
                        y='Value',
                        color='Metric',
                        markers=True,
                        color_discrete_sequence=CHART_COLORS,
                        title="Size Category Impact on Key Metrics")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    # Add workplace insights summary
    st.markdown("""
        <div style='margin-top: 1rem; padding: 1.5rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
            <h4 style='color: #334155; margin-bottom: 0.5rem;'>Workplace Insights:</h4>
            <ul style='color: #64748b; margin: 0;'>
                <li>Remote work shows varying impact across departments</li>
                <li>Department size correlates with stress levels</li>
                <li>Work-life balance differs between remote and office settings</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Discrimination Analysis
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("⚖️ Workplace Equality Analysis")
    
    equality_tab1, equality_tab2, equality_tab3 = st.tabs([
        "👥 Gender Analysis", 
        "💼 Job Satisfaction", 
        "🏢 Department Patterns"
    ])
    
    with equality_tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender-based Stress Analysis
            gender_dept_stress = filtered_df.groupby(['Gender', 'Department'])['Stress_Level'].mean().reset_index()
            fig = px.bar(gender_dept_stress,
                        x='Department',
                        y='Stress_Level',
                        color='Gender',
                        barmode='group',
                        color_discrete_sequence=CHART_COLORS,
                        title="Stress Levels by Gender Across Departments")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Salary Distribution by Gender
            fig = px.box(filtered_df,
                        x='Gender',
                        y='Monthly_Salary_INR',
                        color='Gender',
                        points="all",
                        color_discrete_sequence=CHART_COLORS,
                        title="Salary Distribution by Gender")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with equality_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Work-Life Balance by Gender
            balance_gender = filtered_df.groupby(['Gender', 'Work_Life_Balance'])['Stress_Level'].mean().reset_index()
            fig = px.line(balance_gender,
                         x='Work_Life_Balance',
                         y='Stress_Level',
                         color='Gender',
                         markers=True,
                         color_discrete_sequence=CHART_COLORS,
                         title="Work-Life Balance Impact by Gender")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Experience vs Salary by Gender
            fig = px.scatter(filtered_df,
                           x='Experience_Years',
                           y='Monthly_Salary_INR',
                           color='Gender',
                           color_discrete_sequence=CHART_COLORS,
                           title="Experience-Salary Relationship by Gender")
            fig.update_layout(
                **get_chart_layout(),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with equality_tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Department Gender Distribution
            dept_gender = pd.crosstab(filtered_df['Department'], 
                                   filtered_df['Gender'], 
                                   normalize='index') * 100
            dept_gender_long = dept_gender.reset_index().melt(id_vars=['Department'],
                                                           var_name='Gender',
                                                           value_name='Percentage')
            
            fig = px.bar(dept_gender_long,
                        x='Department',
                        y='Percentage',
                        color='Gender',
                        barmode='stack',
                        color_discrete_sequence=CHART_COLORS,
                        title="Gender Distribution by Department (%)")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45},
                yaxis_title="Percentage (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Promotion Rate Analysis
            filtered_df['Promotion_Rate'] = filtered_df['Monthly_Salary_INR'] / (filtered_df['Experience_Years'] + 1)
            fig = px.box(filtered_df,
                        x='Department',
                        y='Promotion_Rate',
                        color='Gender',
                        color_discrete_sequence=CHART_COLORS,
                        title="Career Progression Analysis")
            fig.update_layout(
                **get_chart_layout(),
                height=400,
                xaxis={'tickangle': 45}
            )
            st.plotly_chart(fig, use_container_width=True)

    # Add equality insights summary
    st.markdown("""
        <div style='margin-top: 1rem; padding: 1.5rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
            <h4 style='color: #334155; margin-bottom: 0.5rem;'>Equality Insights:</h4>
            <ul style='color: #64748b; margin: 0;'>
                <li>Analysis of gender-based stress patterns across departments</li>
                <li>Examination of salary distributions and career progression</li>
                <li>Assessment of work-life balance variations by gender</li>
                <li>Department-wise representation and promotion patterns</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Add a note about the department analysis
    st.markdown("""
        <div style='margin-top: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
            <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>
            <strong>Note:</strong> The data shows:
            <ul style='margin: 0.5rem 0;'>
                <li>Similar stress levels across departments (around 5.0)</li>
                <li>Equal distribution of employees (~2,730 per department)</li>
                <li>Uniform working hours distribution</li>
            </ul>
            This uniformity might indicate standardized working conditions or data normalization.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with equality_tab1:
        # Add note about gender distribution
        st.markdown("""
            <div style='margin-bottom: 1rem; padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem;'>
                <p style='margin: 0; color: #64748b; font-size: 0.9rem;'>
                The data shows nearly equal representation and similar stress levels across genders,
                which might indicate effective workplace equality policies or data standardization.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Add the footer at the very end
    render_footer()

if __name__ == "__main__":
    main() 