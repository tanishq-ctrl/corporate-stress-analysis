import os

# Default dataset path
DEFAULT_DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                  'data', 
                                  'corporate_stress_dataset.csv')

# Visualization settings
CHART_COLORS = [
    '#3b82f6',  # Primary Blue
    '#22c55e',  # Success Green
    '#f97316',  # Warning Orange
    '#ef4444',  # Danger Red
    '#8b5cf6',  # Purple
    '#06b6d4',  # Cyan
    '#14b8a6',  # Teal
    '#f59e0b'   # Amber
]

# Chart theme settings
CHART_THEME = {
    'bgcolor': '#ffffff',
    'font_family': 'Inter, sans-serif',
    'title_font_size': 20,
    'title_font_color': '#1e293b',
    'axis_font_size': 12,
    'axis_font_color': '#475569',
    'grid_color': '#f8fafc'
} 