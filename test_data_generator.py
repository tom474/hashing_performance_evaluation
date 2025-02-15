import os

def create_zero_filled_binary_file(file_name: str, size_in_bytes: int):
    """
    Create a zero-filled binary file.
    """
    with open(file_name, 'wb') as binary_file:
        binary_file.write(b'\x00' * size_in_bytes)

def create_repeated_pattern_binary_file(file_name: str, pattern: bytes, size_in_bytes: int):
    """
    Create a binary file with a repeated pattern.
    """
    with open(file_name, 'wb') as binary_file:
        binary_file.write(pattern * (size_in_bytes // len(pattern)))

def create_random_binary_file(file_name: str, size_in_bytes: int):
    """
    Create a random binary file.
    """
    with open(file_name, 'wb') as binary_file:
        binary_file.write(os.urandom(size_in_bytes))

def generate_kb_file_sizes():
    """
    Generate a list of file sizes in KB.
    Returns:
        list: List of file sizes in bytes.
    """
    sizes_in_kb = [1, 2, 5, 10, 20, 50, 100]  # File sizes in KB
    sizes_in_bytes = [size * 1024 for size in sizes_in_kb]  # Convert to bytes
    return sizes_in_bytes

def generate_mb_file_sizes():
    """
    Generate a list of file sizes in MB with larger gaps.
    Returns:
        list: List of file sizes in bytes.
    """
    sizes_in_mb = [1, 2, 5, 10, 20, 50, 100, 200]  # File sizes in MB
    sizes_in_bytes = [size * 1024 * 1024 for size in sizes_in_mb]  # Convert to bytes
    return sizes_in_bytes

def generate_files_for_multiple_sizes(sizes_in_bytes, size_label, output_folder="test_data"):
    """
    Generate multiple binary files of varying sizes for all types: zero-filled, repeated-pattern, random.
    """
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    for size in sizes_in_bytes:
        # Define file names
        if size_label == "KB":
            size_in_units = size // 1024
        else:  # MB
            size_in_units = size // (1024 * 1024)

        zero_file_name = os.path.join(output_folder, f"zero_filled_{size_in_units}{size_label}.bin")
        pattern_file_name = os.path.join(output_folder, f"pattern_{size_in_units}{size_label}.bin")
        random_file_name = os.path.join(output_folder, f"random_{size_in_units}{size_label}.bin")

        # Generate files
        create_zero_filled_binary_file(zero_file_name, size)
        create_repeated_pattern_binary_file(pattern_file_name, b'AB', size)
        create_random_binary_file(random_file_name, size)

    print(f"Files of sizes {sizes_in_bytes} bytes ({size_label}) have been created in the '{output_folder}' folder.")

# Generate KB and MB file sizes
kb_file_sizes = generate_kb_file_sizes()
mb_file_sizes = generate_mb_file_sizes()

# Generate files for both KB and MB sizes
generate_files_for_multiple_sizes(kb_file_sizes, "KB")
generate_files_for_multiple_sizes(mb_file_sizes, "MB")