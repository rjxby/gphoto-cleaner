import os
import shutil
import logging
import argparse
import sys
import time

def load_config_from_args():
    """
    Loads the root folder, destination folder, and excluded substrings from command-line arguments.
    
    Returns:
        tuple: A tuple containing the root folder, destination folder paths, and excluded substrings.
        
    Raises:
        Exception: If the arguments are not provided correctly.
    """
    parser = argparse.ArgumentParser(description='File Finder and Copier with Exclusion')
    parser.add_argument('root_folder', type=str, help='The root folder to search for files')
    parser.add_argument('destination_folder', type=str, help='The destination folder to copy files to')
    parser.add_argument('--exclude', type=str, nargs='*', help='Substrings to exclude from file names', default=[])
    
    args = parser.parse_args()
    return args.root_folder, args.destination_folder, args.exclude

def find_files(root_folder, exclude_substrings):
    """
    Traverses the root folder and all subfolders to find files grouped by their extensions,
    excluding files that contain any of the specified substrings in their names.
    
    Parameters:
        root_folder (str): The root directory to start the search.
        exclude_substrings (list): List of substrings to exclude from file names.
        
    Returns:
        dict: A dictionary where keys are file extensions and values are lists of file paths.
        
    Raises:
        Exception: If there is an error accessing the directories or files.
    """
    found_files = {}
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if any(sub in file for sub in exclude_substrings):
                continue
            _, extension = os.path.splitext(file)
            if extension not in found_files:
                found_files[extension] = []
            found_files[extension].append(os.path.join(subdir, file))
    return found_files

def copy_files(files, selected_extensions, destination_folder):
    """
    Copies files with selected extensions to the destination folder with a unique prefix and keeps statistics.
    
    Parameters:
        files (dict): Dictionary of found files grouped by extensions.
        selected_extensions (list): List of extensions to copy.
        destination_folder (str): Destination directory where files will be copied.
        
    Logs:
        Info messages for successful copies and error messages for failed copies.
        
    Returns:
        dict: Statistics of files processed and copied.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    stats = {'total_files': 0, 'copied_files': 0, 'failed_files': 0}

    total_files = sum(len(file_list) for ext, file_list in files.items() if ext in selected_extensions)
    copied_files = 0

    for extension, file_list in files.items():
        if extension in selected_extensions:
            for file in file_list:
                stats['total_files'] += 1
                unique_prefix = f"{int(time.time())}_"
                new_file_name = unique_prefix + os.path.basename(file)
                destination_path = os.path.join(destination_folder, new_file_name)
                try:
                    shutil.copy(file, destination_path)
                    logging.info(f"Copied {file} to {destination_path}")
                    stats['copied_files'] += 1
                except Exception as e:
                    logging.error(f"Failed to copy {file} to {destination_path}: {e}")
                    stats['failed_files'] += 1
                copied_files += 1
                print_progress(copied_files, total_files)
                
    return stats

def get_user_selected_extensions(available_extensions):
    """
    Prompts the user to select file extensions to copy.
    
    Parameters:
        available_extensions (list): List of available file extensions.
        
    Returns:
        list: List of selected file extensions.
    """
    print("Available file extensions:")
    for idx, ext in enumerate(available_extensions, start=1):
        print(f"{idx}. {ext}")
    
    selected_indices = input("Select the extensions you want to copy (comma-separated indices): ")
    selected_indices = [int(idx.strip()) for idx in selected_indices.split(',')]
    
    selected_extensions = [available_extensions[idx-1] for idx in selected_indices]
    return selected_extensions

def print_progress(current, total, bar_length=50):
    """
    Displays a progress bar.
    
    Parameters:
        current (int): The current progress.
        total (int): The total number of steps.
        bar_length (int): The length of the progress bar.
    """
    progress = current / total
    block = int(bar_length * progress)
    bar = '#' * block + '-' * (bar_length - block)
    progress_percentage = progress * 100
    sys.stdout.write(f"\r[{bar}] {progress_percentage:.2f}%")
    sys.stdout.flush()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        root_folder, destination_folder, exclude_substrings = load_config_from_args()
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        exit(1)
    
    try:
        files = find_files(root_folder, exclude_substrings)
    except Exception as e:
        logging.error(f"Failed to scan directories: {e}")
        exit(1)
    
    try:
        available_extensions = list(files.keys())
        if not available_extensions:
            logging.error("No files found in the specified root folder.")
            exit(1)
    except Exception as e:
        logging.error(f"Error processing file extensions: {e}")
        exit(1)
    
    try:
        selected_extensions = get_user_selected_extensions(available_extensions)
        if not selected_extensions:
            logging.error("No extensions selected for copying.")
            exit(1)
    except Exception as e:
        logging.error(f"Error getting user-selected extensions: {e}")
        exit(1)
    
    try:
        stats = copy_files(files, selected_extensions, destination_folder)
        logging.info(f"Statistics: {stats}")
    except Exception as e:
        logging.error(f"Failed to copy files: {e}")
        exit(1)
