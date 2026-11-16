"""
AERIS AI - High-Contrast Dark Theme Plotly Charts
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config

DARK_LAYOUT = dict(
    paper_bgcolor="#192630",
    plot_bgcolor="#141E27",
    font=dict(
        family="Plus Jakarta Sans, sans-serif",
        color="#F8FAFC",
        size=12
    ),
    margin=dict(l=40, r=30, t=50, b=40),
    xaxis=dict(
        gridcolor="#293946",
        zerolinecolor="#293946",
        showline=True,
        linecolor="#293946",
        tickfont=dict(color="#94A3B8")
    ),
    yaxis=dict(
        gridcolor="#293946",
        zerolinecolor="#293946",
        showline=True,
        linecolor="#293946",
        tickfont=dict(color="#94A3B8")
    ),
    legend=dict(
        bgcolor="rgba(25, 38, 48, 0.8)",
        bordercolor="#293946",
        borderwidth=1,
        font=dict(color="#F8FAFC")
    )
)

def apply_dark_theme(fig, title: str = ""):
    """Apply the standard AERIS dark theme to any Plotly figure."""
    fig.update_layout(**DARK_LAYOUT)
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans"),
                x=0.02,
                y=0.95
            )
        )
    return fig

def create_aqi_gauge(aqi_value: float, title: str = "Current AQI Gauge"):
    """Create a sleek, high-contrast dark gauge for AQI."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#F8FAFC'}},
        number={'font': {'size': 36, 'color': '#F8FAFC'}},
        gauge={
            'axis': {'range': [0, 500], 'tickwidth': 1, 'tickcolor': "#94A3B8", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': "#22D3EE", 'thickness': 0.28},
            'bgcolor': "#141E27",
            'borderwidth': 1,
            'bordercolor': "#293946",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(16, 185, 129, 0.4)'},
                {'range': [51, 100], 'color': 'rgba(132, 204, 22, 0.4)'},
                {'range': [101, 200], 'color': 'rgba(234, 179, 8, 0.4)'},
                {'range': [201, 300], 'color': 'rgba(249, 115, 22, 0.4)'},
                {'range': [301, 400], 'color': 'rgba(239, 68, 68, 0.4)'},
                {'range': [401, 500], 'color': 'rgba(153, 27, 27, 0.6)'},
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.8,
                'value': aqi_value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="#192630",
        font=dict(color="#F8FAFC", family="Plus Jakarta Sans"),
        margin=dict(l=30, r=30, t=50, b=20),
        height=260
    )
    return fig

def create_trend_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "AQI Trend Over Time"):
    """Create a polished trend line chart with dark aesthetic."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        name=y_col,
        line=dict(color='#10B981', width=2.5),
        marker=dict(size=4, color='#22D3EE'),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.08)'
    ))
    
    # Add CPCB category reference threshold lines
    fig.add_hline(y=100, line_dash="dash", line_color="#EAB308", opacity=0.6, annotation_text="Moderate (100)", annotation_font_color="#EAB308")
    fig.add_hline(y=200, line_dash="dash", line_color="#F97316", opacity=0.6, annotation_text="Poor (200)", annotation_font_color="#F97316")
    fig.add_hline(y=300, line_dash="dash", line_color="#EF4444", opacity=0.6, annotation_text="Very Poor (300)", annotation_font_color="#EF4444")
    
    apply_dark_theme(fig, title)
    fig.update_layout(height=380)
    return fig

def create_pollutant_comparison_chart(pollutants: dict, title: str = "Pollutant Concentrations vs Standards"):
    """Horizontal bar chart comparing pollutant values to their safe standard limits."""
    names = list(pollutants.keys())
    values = [pollutants[k]["value"] for k in names]
    limits = [pollutants[k]["limit"] for k in names]
    
    fig = go.Figure()
    
    # Observed Values
    fig.add_trace(go.Bar(
        y=names,
        x=values,
        name='Recorded Concentration',
        orientation='h',
        marker=dict(color='#22D3EE', line=dict(color='#141E27', width=1))
    ))
    
    # CPCB Standard Limits
    fig.add_trace(go.Bar(
        y=names,
        x=limits,
        name='CPCB Safe Limit',
        orientation='h',
        marker=dict(color='rgba(148, 163, 184, 0.4)', line=dict(color='#94A3B8', width=1))
    ))
    
    apply_dark_theme(fig, title)
    fig.update_layout(
        barmode='group',
        height=320,
        xaxis_title="Concentration (µg/m³ except CO in mg/m³)"
    )
    return fig

def create_city_comparison_bar(cities: list, aqi_vals: list, title: str = "Comparative AQI Index"):
    """Bar chart comparing multiple cities."""
    colors = []
    for val in aqi_vals:
        if val <= 50:
            colors.append('#10B981')
        elif val <= 100:
            colors.append('#84CC16')
        elif val <= 200:
            colors.append('#EAB308')
        elif val <= 300:
            colors.append('#F97316')
        elif val <= 400:
            colors.append('#EF4444')
        else:
            colors.append('#991B1B')
            
    fig = go.Figure(go.Bar(
        x=cities,
        y=aqi_vals,
        marker=dict(color=colors, line=dict(color='#293946', width=1)),
        text=[int(v) for v in aqi_vals],
        textposition='outside',
        textfont=dict(color='#F8FAFC', size=12)
    ))
    
    apply_dark_theme(fig, title)
    fig.update_layout(
        height=350,
        yaxis=dict(range=[0, max(aqi_vals) * 1.2])
    )
    return fig

def create_multi_parameter_trend(df: pd.DataFrame, parameters: list, title: str = "Multi-Parameter Time Series"):
    """Interactive line chart comparing multiple pollutants across dates."""
    fig = go.Figure()
    palette = ["#10B981", "#22D3EE", "#F59E0B", "#EF4444", "#A855F7", "#EC4899"]
    
    for idx, p in enumerate(parameters):
        if p in df.columns:
            color = palette[idx % len(palette)]
            fig.add_trace(go.Scatter(
                x=df["Date"],
                y=df[p],
                mode='lines',
                name=p,
                line=dict(color=color, width=2.0)
            ))

    apply_dark_theme(fig, title)
    fig.update_layout(
        height=400,
        hovermode="x unified",
        xaxis_title="Timeline",
        yaxis_title="Concentration / Index"
    )
    return fig

def create_correlation_bar_chart(corr_df: pd.DataFrame, title: str = "Pollutant Correlation with AQI"):
    """Horizontal bar chart displaying Pearson correlation with AQI."""
    fig = go.Figure(go.Bar(
        y=corr_df["Pollutant"],
        x=corr_df["Correlation_With_AQI"],
        orientation='h',
        marker=dict(
            color=corr_df["Correlation_With_AQI"],
            colorscale=[[0, "#22D3EE"], [1, "#10B981"]],
            line=dict(color='#293946', width=1)
        ),
        text=[f"{v:.3f}" for v in corr_df["Correlation_With_AQI"]],
        textposition='outside',
        textfont=dict(color="#F8FAFC", size=11)
    ))
    apply_dark_theme(fig, title)
    fig.update_layout(
        height=280,
        xaxis=dict(range=[0, 1.15], title="Pearson Correlation (r)")
    )
    return fig

def create_yearly_comparison_chart(yearly_dict: dict, city: str):
    """Bar chart comparing 2023 vs 2024 annual metrics."""
    years = [str(y) for y in [2023, 2024] if y in yearly_dict]
    avg_aqi = [yearly_dict[int(y)]["avg_aqi"] for y in years]
    clean_days = [yearly_dict[int(y)]["clean_days"] for y in years]
    severe_days = [yearly_dict[int(y)]["severe_days"] for y in years]

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Mean AQI', x=years, y=avg_aqi, marker_color='#22D3EE'))
    fig.add_trace(go.Bar(name='Clean Days (AQI ≤ 100)', x=years, y=clean_days, marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Severe Days (AQI ≥ 401)', x=years, y=severe_days, marker_color='#EF4444'))

    apply_dark_theme(fig, f"{city}: 2023 vs 2024 Annual Benchmarking")
    fig.update_layout(barmode='group', height=320)
    return fig
