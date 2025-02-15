import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Define hash algorithms and rounds
hash_names = ["blake2b", "blake2s", "blake3", "sha256", "sha512"]
rounds = [f"round{i}" for i in range(1, 10)]

# Argument parser to accept parameters
parser = argparse.ArgumentParser(description="Visualize hash algorithm performance.")
parser.add_argument("--folder", type=str, required=True, help="Folder for reading results and saving images (e.g., MacOs, Wins)")
args = parser.parse_args()

# Input and output directories based on argument
base_dir = os.path.join("test_data/results", args.folder)
output_dir = os.path.join("visualization", args.folder)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to load results for a specific hash algorithm
def load_results(hash_name):
    data = []
    for round_name in rounds:
        file_path = os.path.join(base_dir, hash_name, f"{round_name}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                times = [int(line.strip()) for line in file.readlines()]  # Read nanoseconds
                avg_time_ns = sum(times) / len(times) if times else 0
                data.append({"Hash": hash_name, "Round": round_name, "AvgTime(ns)": avg_time_ns})
    return data

# Load results for all hash algorithms
all_data = []
for hash_name in hash_names:
    all_data.extend(load_results(hash_name))

# Convert data to a DataFrame
df = pd.DataFrame(all_data)

# Plot grouped bar chart for specified rounds
def visualize_results(dataframe, round_indices, title, filename):
    plt.figure(figsize=(12, 6))
    
    # Filter data for the specified rounds
    filtered_rounds = [rounds[i] for i in round_indices]
    x = range(len(filtered_rounds))  # Number of selected rounds
    width = 0.15  # Bar width
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]  # Colors for each hash

    for i, hash_name in enumerate(hash_names):
        subset = dataframe[dataframe["Hash"] == hash_name]
        avg_times = subset[subset["Round"].isin(filtered_rounds)]["AvgTime(ns)"].values
        plt.bar([p + i * width for p in x], avg_times, width=width, label=hash_name, color=colors[i])

    # Add labels and title
    plt.title(title, fontsize=16)
    plt.xlabel("Rounds", fontsize=14)
    plt.ylabel("Average Execution Time (ns)", fontsize=14)  # Update label to nanoseconds
    plt.xticks([p + 2 * width for p in x], filtered_rounds, rotation=45)  # Adjust x-axis ticks
    plt.legend(title="Hash Algorithm")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    # Save the image
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path)
    print(f"Saved: {output_path}")
    plt.close()

# Generate and save visualizations
visualize_results(df, round_indices=range(0, 3), 
                  title="Execution Time in Nanoseconds (Rounds 1-3)", 
                  filename="rounds_1_to_3.png")
visualize_results(df, round_indices=range(3, 6), 
                  title="Execution Time in Nanoseconds (Rounds 4-6)", 
                  filename="rounds_4_to_6.png")
visualize_results(df, round_indices=range(6, 9), 
                  title="Execution Time in Nanoseconds (Rounds 7-9)", 
                  filename="rounds_7_to_9.png")
