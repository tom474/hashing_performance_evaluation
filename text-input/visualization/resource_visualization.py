import matplotlib.pyplot as plt
import csv
import argparse
import os
import pandas as pd

# Function to read results from a CSV file
def read_resource_results_from_csv(file_path):
    results = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            # Correctly handle floating-point and string data
            results.append([row[0], int(row[1]), float(row[2]), float(row[3])])
    return results

# Visualization of CPU Usage (Bar Chart)
def visualize_cpu_usage_bar(results, output_dir):
    # Convert results to DataFrame for easy manipulation
    df = pd.DataFrame(results, columns=["Algorithm", "Data Size (MB)", "Average CPU Usage (%)", "Peak Memory (MB)"])

    # Pivot the data for bar chart grouping
    pivot_df = df.pivot(index="Data Size (MB)", columns="Algorithm", values="Average CPU Usage (%)")
    pivot_df.plot(kind="bar", figsize=(12, 8), width=0.8)

    # Chart details
    plt.title("Average CPU Usage Across Data Sizes", fontsize=16)
    plt.xlabel("Data Size (MB)", fontsize=14)
    plt.ylabel("Average CPU Usage (%)", fontsize=14)
    plt.legend(title="Algorithm", fontsize=12)
    plt.grid(axis='y', linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the image
    output_path = os.path.join(output_dir, "cpu_usage_bar.png")
    plt.savefig(output_path)
    print(f"Saved CPU usage bar chart to: {output_path}")
    plt.close()

# Visualization of Peak Memory Usage (Bar Chart)
def visualize_memory_usage_bar(results, output_dir):
    # Convert results to DataFrame for easy manipulation
    df = pd.DataFrame(results, columns=["Algorithm", "Data Size (MB)", "Average CPU Usage (%)", "Peak Memory (MB)"])

    # Pivot the data for bar chart grouping
    pivot_df = df.pivot(index="Data Size (MB)", columns="Algorithm", values="Peak Memory (MB)")
    pivot_df.plot(kind="bar", figsize=(12, 8), width=0.8)

    # Chart details
    plt.title("Average Peak Memory Usage Across Data Sizes", fontsize=16)
    plt.xlabel("Data Size (MB)", fontsize=14)
    plt.ylabel("Peak Memory Usage (MB)", fontsize=14)
    plt.legend(title="Algorithm", fontsize=12)
    plt.grid(axis='y', linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the image
    output_path = os.path.join(output_dir, "memory_usage_bar.png")
    plt.savefig(output_path)
    print(f"Saved memory usage bar chart to: {output_path}")
    plt.close()

# Main function
def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Visualize resource usage from hashing results.")
    parser.add_argument("--folder", type=str, required=True, help="Subdirectory in the results folder to read the results.")
    args = parser.parse_args()

    # Construct the path to the results file
    results_dir = os.path.join("results", args.folder, "resource_usage")
    results_file = os.path.join(results_dir, "hashing_resource_avg_results.csv")
    visualization_dir = os.path.join("visualization", args.folder, "resource_usage")

    # Ensure visualization directory exists
    os.makedirs(visualization_dir, exist_ok=True)

    if not os.path.exists(results_file):
        print(f"Error: Results file not found at {results_file}")
        return

    # Read results and visualize
    print(f"Reading results from: {results_file}")
    results = read_resource_results_from_csv(results_file)

    # Generate bar chart visualizations
    visualize_cpu_usage_bar(results, visualization_dir)
    visualize_memory_usage_bar(results, visualization_dir)

if __name__ == "__main__":
    main()
