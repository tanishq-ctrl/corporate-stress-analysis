from stress_analysis import *
import os

def main():
    # Create outputs directory if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # Load data
    df = load_data('/Users/tanishq/Downloads/corporate_stress_dataset.csv')

    # Generate plots
    plot_stress_distribution(df)
    plot_department_stress(df)
    plot_hours_stress(df)

    # Calculate metrics
    metrics = calculate_stress_metrics(df)
    correlations = analyze_correlations(df)

    # Print results
    print("\nKey Findings:")
    print(f"\nOverall Average Stress Level: {metrics['Overall']:.2f}")
    print("\nAverage Stress Level by Gender:")
    print(metrics['By Gender'])
    print("\nAverage Stress Level by Department:")
    print(metrics['By Department'])
    print("\nAverage Stress Level by Remote Work:")
    print(metrics['By Remote Work'])
    print("\nCorrelations with Stress Level:")
    print(correlations)

if __name__ == "__main__":
    main() 