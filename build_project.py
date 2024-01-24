import os
import re


def replace_word_in_file(file_path, old_word, new_word, script_path):
    if file_path == script_path:
        print(f"Skipping the script file itself: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        # Create a pattern that matches the exact old_word
        pattern = re.escape(old_word)
        file_contents = re.sub(pattern, new_word, file_contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_contents)

    except UnicodeDecodeError:
        print(f"Skipping file due to decoding error: {file_path}")


def replace_word_in_dirname(dir_path, old_word, new_word):
    parent_dir = os.path.dirname(dir_path)
    dir_name = os.path.basename(dir_path)
    new_dir_name = re.sub(re.escape(old_word), new_word, dir_name)

    if new_dir_name != dir_name:
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        os.rename(dir_path, new_dir_path)
        print(f"Renamed directory from {dir_path} to {new_dir_path}")
        return new_dir_path
    return dir_path


def main(root_dir, old_word, new_word):
    script_path = os.path.abspath(__file__)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Replace in files
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            replace_word_in_file(file_path, old_word, new_word, script_path)

        # Replace in directory names
        for dirname in dirnames:
            full_dir_path = os.path.join(dirpath, dirname)
            replace_word_in_dirname(full_dir_path, old_word, new_word)


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.realpath(__file__))  # Root directory is script's location
    old_word = '{{ your_project_name }}'  # Word to be replaced
    new_word = ''  # New word

    main(root_dir, old_word, new_word)