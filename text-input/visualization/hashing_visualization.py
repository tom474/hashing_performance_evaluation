import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Argument parser
parser = argparse.ArgumentParser(description="Visualize hashing performance metrics for single-threaded and multi-threaded results.")
parser.add_argument("--folder", type=str, required=True, help="Folder name inside results and visualization directories.")
args = parser.parse_args()

# Directories for results and output
results_dir = os.path.join("results", args.folder, "hashing")
output_dir = os.path.join("visualization", args.folder, "hashing")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load CSV data into pandas DataFrame
def load_csv_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    return pd.read_csv(file_path)

# Visualization function
def visualize_metric(df, x_col, y_col, ylabel, title, filename):
    plt.figure(figsize=(12, 6))
    algorithms = df["Algorithm"].unique()

    for algo in algorithms:
        subset = df[df["Algorithm"] == algo]
        plt.plot(subset[x_col], subset[y_col], marker='o', label=algo.upper())

    # Add labels, title, and legend
    plt.title(title, fontsize=16)
    plt.xlabel(x_col.replace("_", " ").title(), fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(title="Algorithm", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Save the plot
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path)
    print(f"Saved: {output_path}")
    plt.close()

# Main function for visualization
def main():
    # File paths for summaries
    single_thread_summary_file = os.path.join(results_dir, "hashing_speed_single_thread_summary.csv")
    multi_thread_summary_file = os.path.join(results_dir, "hashing_speed_multi_threads_summary.csv")

    # Single-threaded visualization
    if os.path.exists(single_thread_summary_file):
        print("Visualizing single-threaded summary results...")
        single_thread_summary_df = load_csv_data(single_thread_summary_file)

        # Visualize average timing
        visualize_metric(
            single_thread_summary_df,
            x_col="Data Size (MB)",
            y_col="Avg Time (ms)",
            ylabel="Average Time (ms)",
            title="Single-Threaded Hashing: Average Timing Per Algorithm",
            filename="single_thread_avg_time.png"
        )

        # Visualize speed
        visualize_metric(
            single_thread_summary_df,
            x_col="Data Size (MB)",
            y_col="Speed (MBps)",
            ylabel="Speed (MBps)",
            title="Single-Threaded Hashing: Speed Per Algorithm",
            filename="single_thread_speed.png"
        )

    # Multi-threaded visualization
    if os.path.exists(multi_thread_summary_file):
        print("Visualizing multi-threaded summary results...")
        multi_thread_summary_df = load_csv_data(multi_thread_summary_file)

        # Visualize average timing
        visualize_metric(
            multi_thread_summary_df,
            x_col="Data Size (MB)",
            y_col="Avg Time (ms)",
            ylabel="Average Time (ms)",
            title="Multi-Threaded Hashing: Average Timing Per Algorithm",
            filename="multi_thread_avg_time.png"
        )

        # Visualize speed
        visualize_metric(
            multi_thread_summary_df,
            x_col="Data Size (MB)",
            y_col="Speed (MBps)",
            ylabel="Speed (MBps)",
            title="Multi-Threaded Hashing: Speed Per Algorithm",
            filename="multi_thread_speed.png"
        )

if __name__ == "__main__":
    main()
