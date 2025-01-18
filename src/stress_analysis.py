import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data(filepath):
    """Load and return the corporate stress dataset"""
    return pd.read_csv(filepath)

def plot_stress_distribution(df):
    """Plot the overall distribution of stress levels"""
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='Stress_Level', bins=11)
    plt.title('Distribution of Stress Levels')
    plt.xlabel('Stress Level (0-10)')
    plt.ylabel('Count')
    plt.savefig('outputs/stress_distribution.png')
    plt.close()

def calculate_stress_metrics(df):
    """Calculate key stress-related metrics"""
    metrics = {
        'Overall': df['Stress_Level'].mean(),
        'By Gender': df.groupby('Gender')['Stress_Level'].mean(),
        'By Department': df.groupby('Department')['Stress_Level'].mean(),
        'By Remote Work': df.groupby('Remote_Work')['Stress_Level'].mean()
    }
    return metrics

def analyze_correlations(df):
    """Analyze correlations with stress levels"""
    return df[['Stress_Level', 'Age', 'Working_Hours_per_Week', 
               'Monthly_Salary_INR', 'Sleep_Hours', 'Work_Life_Balance']].corr()['Stress_Level']

def plot_department_stress(df):
    """Plot stress levels by department"""
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Department', y='Stress_Level')
    plt.title('Stress Levels by Department')
    plt.xticks(rotation=45)
    plt.savefig('outputs/department_stress.png')
    plt.close()

def plot_hours_stress(df):
    """Plot relationship between working hours and stress"""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df.sample(1000), x='Working_Hours_per_Week', y='Stress_Level', alpha=0.5)
    plt.title('Working Hours vs Stress Level')
    plt.savefig('outputs/hours_stress.png')
    plt.close()

def analyze_workplace_dynamics(df):
    """
    Analyze workplace dynamics including remote work, department stress, and company size impact
    """
    # Remote work analysis
    remote_stats = df.groupby('Remote_Work').agg({
        'Stress_Level': ['mean', 'std', 'count'],
        'Work_Life_Balance': 'mean'
    }).round(2)
    
    # Department analysis
    dept_stats = df.groupby('Department').agg({
        'Stress_Level': ['mean', 'std'],
        'Working_Hours_per_Week': 'mean',
        'Monthly_Salary_INR': 'mean'
    }).round(2)
    
    return remote_stats, dept_stats 