from blonde.BlonDe import BLONDE
import os

# Function to read a file and return its contents as a list of strings
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]  # Remove empty lines

# Create a BLONDE object
blonde = BLONDE()

# Dictionary to store results
results = {}

# Define the path to the folder
folder_path = 'C:/Users/yvonn/Desktop/TT Assignment2'

# Define input and output directories
input_dir = f"{folder_path}/input"
output_dir = f"{folder_path}/output"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the input files and reference file
output_files = ["02_NMT Output.txt", "02_LLM Output.txt"]
reference_file_path = f"{input_dir}/03_Reference.txt"
output_file_path = f"{output_dir}/04_Results.txt"

# Read the reference file (human translation)
if not os.path.exists(reference_file_path):
    raise FileNotFoundError(f"Reference file not found: {reference_file_path}")
ref_doc = [read_file(reference_file_path)]  # Wrap in an outer list for BLONDE compatibility

# Process each output file and compute the BLONDE score
for file_name in output_files:
    input_file_path = f"{input_dir}/{file_name}"

    if not os.path.exists(input_file_path):
        print(f"Input file not found: {input_file_path}")
        results[file_name] = None
        continue

    sys_doc = [read_file(input_file_path)]  # Wrap in an outer list for BLONDE compatibility

    # Debugging: Print file contents to verify format
    print(f"\nProcessing file: {file_name}")
    print(f"System Output: {sys_doc}")
    print(f"Reference: {ref_doc}")

    if not sys_doc or not ref_doc or len(sys_doc[0]) == 0 or len(ref_doc[0]) == 0:
        print(f"File {file_name} or reference is empty or invalid.")
        results[file_name] = None
        continue

    # Compute the BLONDE score
    try:
        score = blonde.corpus_score(sys_doc, ref_doc)
        results[file_name] = score
    except Exception as e:
        print(f"Error computing BLONDE for {file_name}: {e}")
        results[file_name] = None

# Write all scores to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    for file_name, score in results.items():
        file.write(f"BLONDE score for {file_name} against 03_Reference:\n")
        file.write(str(score) + "\n\n")

# Display the results
print("\nProcessing complete. Results:")
for file_name, score in results.items():
    print(f"Results for {file_name}:")
    print(score)
    print("\n")