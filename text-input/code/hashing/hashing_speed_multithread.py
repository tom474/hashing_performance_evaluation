import hashlib
import time
import os
import argparse
from threading import Thread, Lock
from queue import Queue
from blake3 import blake3
from scipy.stats import ttest_ind
import pandas as pd

MAX_THREADS = 8
RUNS_PER_TEST = 5  # Number of runs for meaningful T-tests
CHUNK_SIZE = 64 * 1024  # 64KB for file reads

data_dir = "code/data/speed"
results_dir = "results"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

lock = Lock()

def create_random_binary_file(file_name: str, size_in_bytes: int, chunk_size: int = 64 * 1024):
    """
    Create a random binary file in chunks to avoid memory overflow.
    """
    with open(file_name, 'wb') as binary_file:
        bytes_written = 0
        while bytes_written < size_in_bytes:
            remaining_bytes = size_in_bytes - bytes_written
            binary_file.write(os.urandom(min(chunk_size, remaining_bytes)))
            bytes_written += min(chunk_size, remaining_bytes)

    print(f"Created file: {file_name} with size: {size_in_bytes // (1024 * 1024)} MB")

def generate_mb_file_sizes():
    """
    Generate a list of file sizes in MB.
    """
    sizes_in_mb = [1, 2, 4, 8, 16, 32, 64, 128, 200, 512]  # File sizes in MB
    return sizes_in_mb

def cleanup_extra_files(data_sizes_mb, folder):
    """
    Remove any extra files in the folder that are not part of the intended sizes.
    """
    intended_files = {f"random_{size}MB.bin" for size in data_sizes_mb}
    existing_files = set(os.listdir(folder))

    # Find extra files
    extra_files = existing_files - intended_files
    for extra_file in extra_files:
        file_path = os.path.join(folder, extra_file)
        os.remove(file_path)
        print(f"Removed extra file: {file_path}")

def generate_files_for_multiple_sizes(data_sizes_mb, output_folder):
    """
    Generate binary files of specified sizes in MB.
    """
    os.makedirs(output_folder, exist_ok=True)
    for size_mb in data_sizes_mb:
        file_path = os.path.join(output_folder, f"random_{size_mb}MB.bin")
        if not os.path.exists(file_path):
            create_random_binary_file(file_path, size_mb * 1024 * 1024)

def ensure_data_files_exist():
    """
    Ensure all required files exist in the data directory.
    """
    file_sizes_mb = generate_mb_file_sizes()
    generate_files_for_multiple_sizes(file_sizes_mb, data_dir)
    cleanup_extra_files(file_sizes_mb, data_dir)

def warm_up(file_path, hash_function):
    """
    Warm-up to pre-load the hashing mechanism.
    """
    with open(file_path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):  # Read file in 64KB chunks
            hash_function(chunk)

def measure_hashing_speed(algorithm, file_path, data_size_mb):
    """
    Measure the hashing speed for a specific algorithm and file.
    """
    if algorithm == "blake3":
        hash_function = lambda x: blake3(x).digest()
    else:
        hash_function = lambda x: hashlib.new(algorithm, x).digest()

    warm_up(file_path, hash_function)

    timings = []
    for _ in range(RUNS_PER_TEST):
        start_time = time.time()
        with open(file_path, "rb") as file:
            while chunk := file.read(CHUNK_SIZE):
                hash_function(chunk)
        end_time = time.time()
        timings.append((end_time - start_time) * 1e3)  # Convert seconds to milliseconds

    total_time = sum(timings)
    avg_time = total_time / RUNS_PER_TEST
    speed = data_size_mb / (total_time / 1000)  # MBps
    return timings, total_time, avg_time, speed

def worker(queue, timing_results, summary_results):
    """
    Worker function to process the hashing speed test.
    """
    while not queue.empty():
        algo, file_path, size_mb = queue.get()
        try:
            timings, total_time, avg_time, speed = measure_hashing_speed(algo, file_path, size_mb)
            with lock:
                for timing in timings:
                    timing_results.append([algo, size_mb, timing])
                summary_results.append([algo, size_mb, total_time, avg_time, speed])
        except Exception as e:
            print(f"Error processing {algo} with {file_path}: {e}")
        finally:
            queue.task_done()

def test_multithreading(algorithms, files_info):
    """
    Run the multithreaded hashing test.
    """
    timing_results = []
    summary_results = []
    queue = Queue()

    for algo in algorithms:
        for file_path, size_mb in files_info:
            queue.put((algo, file_path, size_mb))

    threads = []
    for _ in range(MAX_THREADS):
        thread = Thread(target=worker, args=(queue, timing_results, summary_results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return timing_results, summary_results

def perform_t_tests(timing_results_csv, output_folder):
    """
    Perform T-tests on timing results for algorithm comparisons.
    """
    df = pd.read_csv(timing_results_csv)
    comparison_pairs = [("blake3", "sha256"), ("blake2s", "blake2b")]
    t_test_results = []

    for size in df["Data Size (MB)"].unique():
        subset = df[df["Data Size (MB)"] == size]
        for algo1, algo2 in comparison_pairs:
            times1 = subset[subset["Algorithm"] == algo1]["Timing (ms)"]
            times2 = subset[subset["Algorithm"] == algo2]["Timing (ms)"]

            if len(times1) > 1 and len(times2) > 1:
                t_stat, p_value = ttest_ind(times1, times2, equal_var=False)
                t_test_results.append({
                    "Data Size (MB)": size,
                    "Algorithm 1": algo1,
                    "Algorithm 2": algo2,
                    "T-Statistic": round(t_stat, 4),
                    "P-Value": round(p_value, 6)
                })

    t_test_file = os.path.join(output_folder, "hashing_t_multi_threads_test_results.csv")
    pd.DataFrame(t_test_results).to_csv(t_test_file, index=False)
    print(f"T-test results saved to {t_test_file}")

def main():
    """
    Main function to run the multithreaded hashing speed test.
    """
    parser = argparse.ArgumentParser(description="Run multithreaded hashing speed test and save results to CSV.")
    parser.add_argument("--output", type=str, required=True, help="Output subdirectory under ./results/")
    args = parser.parse_args()

    output_folder = os.path.join(results_dir, args.output) + "/hashing"
    os.makedirs(output_folder, exist_ok=True)

    # Ensure data files exist
    ensure_data_files_exist()

    # Create a list of file paths and sizes
    file_sizes_mb = generate_mb_file_sizes()
    files_info = [(os.path.join(data_dir, f"random_{size}MB.bin"), size) for size in file_sizes_mb]

    algorithms = ['blake3', 'blake2s', 'blake2b', 'sha256']
    timing_results, summary_results = test_multithreading(algorithms, files_info)

    # Save timing results
    timing_csv = os.path.join(output_folder, "hashing_speed_multi_threads_timing.csv")
    pd.DataFrame(timing_results, columns=["Algorithm", "Data Size (MB)", "Timing (ms)"]).to_csv(timing_csv, index=False)

    # Save summary results
    summary_csv = os.path.join(output_folder, "hashing_speed_multi_threads_summary.csv")
    pd.DataFrame(summary_results, columns=["Algorithm", "Data Size (MB)", "Total Time (ms)", "Avg Time (ms)", "Speed (MBps)"]).to_csv(summary_csv, index=False)

    # Perform T-tests
    perform_t_tests(timing_csv, output_folder)

if __name__ == "__main__":
    main()
