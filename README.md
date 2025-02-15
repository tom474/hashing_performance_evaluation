# Blake2b_Security_Research

## Features

- Test and compare Merkle tree performance with various hash algorithms (`SHA256`, `Blake2b`, `Blake3`, `Blake2s`, `SHA512`).
- Visualize and analyze results with grouped bar charts.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.8 or higher**
- **Pip** for managing Python packages

---

## Run Blockchain Test

- Step 1: Install necessary libraries.

```
pip install -r requirements.txt
```

- Step 2: Access blockchain directory.

```
cd blockchain/
```

- Step 3: Run server

```
python test_data/server.py
```

- Step 4: Run client script

```
python test_data/client.py --results_dir <result_directory>

for example
python test_data/client.py --results_dir Windows
python test_data/client.py --results_dir Linux
python test_data/client.py --results_dir MacOS
```

- Step 5: Generate Visualization Reports

```
python visualization/main.py --folder <output_folder>

example
python visualization/main.py --folder Windows
python visualization/main.py --folder MacOS
python visualization/main.py --folder Linux
```

---

## Run Test for text input

- Step 1: Unzip the data folder

```
cd text-input/code
unzip data.zip
```

- Step 2: cd back to text-input directory.

```
cd ..

pwd
> text-input/
```

! Important: your current directory must be text-input

- Step 3: Run test to measure the speed among hashing algorithms in single thread.

```
python code/hashing/hashing_speed.py --output <output_folder>

example
python code/hashing/hashing_speed.py --output Windows
python code/hashing/hashing_speed.py --output MacOS
python code/hashing/hashing_speed.py --output Linux
```

- Step 4: Run test to measure the speed among hashing algorithms in multi thread.

```
python code/hashing/hashing_speed_multithread.py --output <output_folder>

example
python code/hashing/hashing_speed_multithread.py --output Windows
python code/hashing/hashing_speed_multithread.py --output MacOS
python code/hashing/hashing_speed_multithread.py --output Linux
```

- Step 5: Generate Visualization Reports

```
python visualization/hashing_visualization.py --folder <output_folder>

example
python visualization/hashing_visualization.py --folder Windows
python visualization/hashing_visualization.py --folder MacOS
python visualization/hashing_visualization.py --folder Linux
```

- Step 4: Run test to measure the resource usage among hashing algorithms.

```
python code/resource_usage/resource_consumption.py --output <output_folder>

example
python code/resource_usage/resource_consumption.py --output Windows
python code/resource_usage/resource_consumption.py --output MacOS
python code/resource_usage/resource_consumption.py --output Linux
```

- Step 5: Generate Visualization Reports

```
python visualization/resource_visualization.py --folder <output_folder>

example
python visualization/resource_visualization.py --folder Windows
python visualization/resource_visualization.py --folder MacOS
python visualization/resource_visualization.py --folder Linux
```

---

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
