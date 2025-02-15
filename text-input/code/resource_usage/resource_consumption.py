import hashlib
import psutil
import os
import csv
import argparse
from blake3 import blake3
from scipy.stats import ttest_ind
import pandas as pd
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base directories
data_dir = "code/data/resources"
default_results_dir = "results"

# Ensure base directories exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(default_results_dir, exist_ok=True)


def create_random_binary_file(file_name: str, size_in_bytes: int, chunk_size: int = 64 * 1024):
    """
    Create a random binary file in chunks to avoid memory overflow.
    """
    try:
        with open(file_name, 'wb') as binary_file:
            bytes_written = 0
            while bytes_written < size_in_bytes:
                remaining_bytes = size_in_bytes - bytes_written
                binary_file.write(os.urandom(min(chunk_size, remaining_bytes)))
                bytes_written += min(chunk_size, remaining_bytes)
        logging.info(f"Created file: {file_name} with size: {size_in_bytes // (1024 * 1024)} MB")
    except Exception as e:
        logging.error(f"Error creating file {file_name}: {e}")


def generate_files_for_multiple_sizes(data_sizes_mb, output_folder):
    """
    Generate binary files of specified sizes in MB.
    """
    os.makedirs(output_folder, exist_ok=True)
    for size_mb in data_sizes_mb:
        file_path = os.path.join(output_folder, f"dataset_{size_mb}MB.bin")
        if not os.path.exists(file_path):
            create_random_binary_file(file_path, size_mb * 1024 * 1024)


def ensure_data_files_exist():
    """
    Ensure all required files exist in the data directory.
    """
    file_sizes_mb = [1, 2, 4, 8, 16, 32, 64, 128, 200, 512]
    generate_files_for_multiple_sizes(file_sizes_mb, data_dir)


import time

def measure_resource_usage(algorithm, data_size_mb, iterations):
    """
    Measure CPU and memory usage for a given hashing algorithm and data size.
    """
    ensure_data_files_exist()
    file_path = os.path.join(data_dir, f"dataset_{data_size_mb}MB.bin")

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        logging.error(f"File not found or empty: {file_path}")
        return [], 0

    if algorithm == "blake3":
        hash_function = lambda x: blake3(x).digest()
    else:
        hash_function = lambda x: hashlib.new(algorithm, x).digest()

    process = psutil.Process(os.getpid())
    peak_memory_mb = 0
    cpu_usages = []

    for _ in range(iterations):
        try:
            start_time = time.time()
            with open(file_path, "rb") as file:
                while chunk := file.read(8192):  # Read file in 8KB chunks
                    hash_function(chunk)

            elapsed_time = time.time() - start_time
            logging.info(f"Iteration completed in {elapsed_time:.6f} seconds for {data_size_mb} MB with {algorithm}")

            # Add a short delay before measuring CPU usage
            time.sleep(2)  # 100 milliseconds delay

            # Measure CPU usage with a short interval
            cpu_usage = psutil.cpu_percent(interval=2)
            cpu_usages.append(cpu_usage)

            # Check memory usage
            current_memory_mb = process.memory_info().rss / (1024 * 1024)
            peak_memory_mb = max(peak_memory_mb, current_memory_mb)

        except Exception as e:
            logging.error(f"Error during resource measurement: {e}")
            continue

    return cpu_usages, peak_memory_mb


def test_resource_usage(algorithms, data_sizes_mb, iterations):
    """
    Test resource usage for multiple algorithms and file sizes.
    """
    results = []
    for algo in algorithms:
        for size_mb in data_sizes_mb:
            logging.info(f"Testing {algo} with {size_mb} MB")
            cpu_usages, peak_memory = measure_resource_usage(algo, size_mb, iterations)
            for cpu in cpu_usages:
                results.append([algo, size_mb, round(cpu, 6), round(peak_memory, 6)])
    return results


def perform_t_tests(results_csv, output_folder):
    """
    Perform T-tests between different hashing algorithms and save results.
    """
    df = pd.read_csv(results_csv)
    data_sizes = df["Data Size (MB)"].unique()
    comparison_pairs = [("blake3", "sha256"), ("blake2s", "blake2b")]
    t_test_results = []

    for size in data_sizes:
        subset = df[df["Data Size (MB)"] == size]
        for algo1, algo2 in comparison_pairs:
            values_algo1 = subset[subset["Algorithm"] == algo1]["CPU (%)"].values
            values_algo2 = subset[subset["Algorithm"] == algo2]["CPU (%)"].values

            if len(values_algo1) > 1 and len(values_algo2) > 1:
                t_stat, p_value = ttest_ind(values_algo1, values_algo2, equal_var=False)
                t_test_results.append({
                    "Data Size (MB)": size,
                    "Algorithm 1": algo1,
                    "Algorithm 2": algo2,
                    "T-Statistic": round(t_stat, 8),
                    "P-Value": round(p_value, 8)
                })

    t_test_output = os.path.join(output_folder, "hashing_resource_t_test_results.csv")
    pd.DataFrame(t_test_results).to_csv(t_test_output, index=False)
    logging.info(f"T-test results saved to {t_test_output}")


def calculate_averages(input_csv, output_folder):
    """
    Calculate averages of CPU usage and memory usage and save results.
    """
    df = pd.read_csv(input_csv)
    avg_df = (
        df.groupby(["Algorithm", "Data Size (MB)"])
        .agg(Average_CPU_Usage=("CPU (%)", lambda x: round(x.mean(), 6)),
             Peak_Memory=("Peak Memory (MB)", lambda x: round(x.mean(), 6)))
        .reset_index()
    )
    avg_csv = os.path.join(output_folder, "hashing_resource_avg_results.csv")
    avg_df.to_csv(avg_csv, index=False)
    logging.info(f"Average results saved to {avg_csv}")


def main():
    """
    Main function to orchestrate the resource usage measurement.
    """
    logging.info("Starting resource usage measurement...")
    parser = argparse.ArgumentParser(description="Measure and analyze resource usage of hashing algorithms.")
    parser.add_argument("--output", type=str, required=True, help="Subdirectory in the results folder to save the results.")
    args = parser.parse_args()

    algorithms = ['md5', 'sha1', 'sha256', 'sha512', 'sha3_256', 'blake2s', 'blake2b', 'blake3']
    data_sizes_mb = [1, 2, 4, 8, 16, 32, 64, 128, 200, 512]
    iterations = 1

    results = test_resource_usage(algorithms, data_sizes_mb, iterations)
    results_dir = os.path.join(default_results_dir, args.output, "resource_usage")
    os.makedirs(results_dir, exist_ok=True)
    results_csv = os.path.join(results_dir, "hashing_resource_results.csv")

    try:
        with open(results_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Data Size (MB)", "CPU (%)", "Peak Memory (MB)"])
            writer.writerows(results)
        logging.info(f"Resource results saved to {results_csv}")
    except Exception as e:
        logging.error(f"Error saving results: {e}")

    perform_t_tests(results_csv, results_dir)
    calculate_averages(results_csv, results_dir)


if __name__ == "__main__":
    main()
