# Hashing Performance Evaluation

A performance evaluation of various **hashing algorithms** (`SHA256`, `Blake2b`, `Blake3`, `Blake2s`, `SHA512`), focusing on **Merkle tree efficiency, hashing speed, and resource consumption**. This project compares single-threaded and multi-threaded hashing performance and visualizes the results using grouped bar charts.  

## Tech Stack

- Python

## Features

- **Merkle Tree Performance**: Evaluates Merkle tree construction using different hashing algorithms.  
- **Single-Threaded Hashing Speed**: Measures hashing efficiency in a single-threaded environment.  
- **Multi-Threaded Hashing Speed**: Compares hashing speed across multiple threads.  
- **Resource Consumption Analysis**: Tracks CPU and memory usage for different hash algorithms.  
- **Visualization Reports**: Generates bar charts to compare performance results.

## Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.8 or higher**
- **Pip** for managing Python packages

### Run Blockchain Test

Step 1: Install necessary libraries

```bash
pip install -r requirements.txt
```

Step 2: Access blockchain directory

```bash
cd blockchain/
```

Step 3: Run server

```bash
python test_data/server.py
```

Step 4: Run client script

```bash
python test_data/client.py --results_dir <result_directory>
```

Examples:

```bash
python test_data/client.py --results_dir Windows
python test_data/client.py --results_dir Linux
python test_data/client.py --results_dir MacOS
```

Step 5: Generate Visualization Reports

```bash
python visualization/main.py --folder <output_folder>
```

Examples:

```bash
python visualization/main.py --folder Windows
python visualization/main.py --folder MacOS
python visualization/main.py --folder Linux
```

### Run Text Input Test

Step 1: Unzip the data folder

```bash
cd text-input/code
unzip data.zip
```

Step 2: Go back to text-input directory.

```bash
cd ..

pwd
> text-input/
```

> Important: your current directory must be text-input

Step 3: Run test to measure the speed among hashing algorithms in single thread.

```bash
python code/hashing/hashing_speed.py --output <output_folder>
```

Examples:

```bash
python code/hashing/hashing_speed.py --output Windows
python code/hashing/hashing_speed.py --output MacOS
python code/hashing/hashing_speed.py --output Linux
```

Step 4: Run test to measure the speed among hashing algorithms in multi thread.

```bash
python code/hashing/hashing_speed_multithread.py --output <output_folder>
```

Examples:

```bash
python code/hashing/hashing_speed_multithread.py --output Windows
python code/hashing/hashing_speed_multithread.py --output MacOS
python code/hashing/hashing_speed_multithread.py --output Linux
```

Step 5: Generate Visualization Reports

```bash
python visualization/hashing_visualization.py --folder <output_folder>
```

Examples:

```bash
python visualization/hashing_visualization.py --folder Windows
python visualization/hashing_visualization.py --folder MacOS
python visualization/hashing_visualization.py --folder Linux
```

Step 6: Run test to measure the resource usage among hashing algorithms.

```bash
python code/resource_usage/resource_consumption.py --output <output_folder>
```

Examples:

```bash
python code/resource_usage/resource_consumption.py --output Windows
python code/resource_usage/resource_consumption.py --output MacOS
python code/resource_usage/resource_consumption.py --output Linux
```

Step 7: Generate Visualization Reports

```bash
python visualization/resource_visualization.py --folder <output_folder>
```

Examples:

```bash
python visualization/resource_visualization.py --folder Windows
python visualization/resource_visualization.py --folder MacOS
python visualization/resource_visualization.py --folder Linux
```

## Final Result

You can access results folder in the source code to observe the result.

    .
    ├── blockchain
        ├── test_data
            ├── results
            ├── chain.py
            ├── client.py
            ├── config.py
            ├── server.py
        ├── visualization
            ├── <output_folder>
            ├── main.py
    ├── text-input
        ├── code
            ├── data
            ├── hashing
                ├── hashing_speed.py
                ├── hashing_speed_multithread.py
            ├── resource_usage
                ├── resource_consumption.py
        ├── results
            ├── <output_folder>
                ├── hashing
                ├── resource_usage
        ├── visualization
            ├── <output_folder>
                ├── hashing
                ├── resource_usage
            ├── hashing_visualization.py
            ├── resource_visualization.py
