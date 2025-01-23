def compare_files_on2(file1_path, file2_path):
    """
    Compare two text files line by line using O(n^2) approach without sets.

    Args:
        file1_path: Path to the first file.
        file2_path: Path to the second file.

    Returns:
        A tuple containing:
        - Total matched lines.
        - Lines in File 1 missing from File 2.
        - Lines in File 2 not found in File 1.
    """
    match = False
    count_match = 0
    count_not_match = 0
    with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
        file1_lines = file1.readlines()  # Read lines including \n
        file2_lines = file2.readlines()  # Read lines including \n

        for i in file1_lines:
            # print(str(i).strip())
            for j in file2_lines:
                if i.strip() == j.strip():
                    count_match+=1
                    match = True
            if not match:
                count_not_match+=1
                print(f"Line from File 1: {str(i)[19:32]}")
            match = False  # Reset match flag for next iteration in file1_lines list
            
    print(count_match, count_not_match, count_not_match+count_match)

# Example usage
file1_path = 'GBR.txt'  # Path to the first text file
file2_path = 'R035950525_GBR_combine.txt'  # 

compare_files_on2(file1_path,file2_path)