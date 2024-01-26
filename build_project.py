import os
import re
import shutil
import subprocess


# 파일 내부에 일치하는 단어를 탐색하여 대체
def replace_word_in_file(file_path, old_project_name, new_project_name, script_path):
    if file_path == script_path:
        # print(f"Skipping the script file itself: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        pattern = re.escape(old_project_name)
        file_contents = re.sub(pattern, new_project_name, file_contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(file_contents)

    except UnicodeDecodeError:
        # print(f"Skipping file due to decoding error: {file_path}")
        return


# 디렉토리명을 순회하여 대체
def replace_word_in_dirname(dir_path, old_project_name, new_project_name):
    parent_dir = os.path.dirname(dir_path)
    dir_name = os.path.basename(dir_path)
    new_dir_name = re.sub(re.escape(old_project_name), new_project_name, dir_name)

    if new_dir_name != dir_name:
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        os.rename(dir_path, new_dir_path)
        # print(f"Renamed directory from {dir_path} to {new_dir_path}")
        return new_dir_path
    return dir_path


def main(root_dir, old_project_name, new_project_name):
    script_path = os.path.abspath(__file__)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Replace in files
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            replace_word_in_file(file_path, old_project_name, new_project_name, script_path)

        # Replace in directory names
        for dirname in dirnames:
            full_dir_path = os.path.join(dirpath, dirname)
            replace_word_in_dirname(full_dir_path, old_project_name, new_project_name)


def get_valid_input(prompt):
    while True:
        user_input = input(prompt)

        if re.match("^[a-z0-9_]+$", user_input) is not None:
            return user_input
        else:
            print("Invalid input. Please use only lowercase letters, numbers, and underscores.")


def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def change_git_branch(branch_name):
    try:
        subprocess.run(["git", "pull", "origin", branch_name], check=True)
        print(f"Switched to branch: {branch_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error changing to branch {branch_name}: {e}")


def remove_git_connection():
    git_dir = os.path.join(root_dir, '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
        print("Removed existing Git connection.")
    else:
        print("No existing Git connection found.")


def initialize_new_git():
    try:
        subprocess.run(["git", "init"], check=True, cwd=root_dir)
        print("Initialized a new Git repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing new Git repository: {e}")


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.realpath(__file__))
    old_project_name = '{{ your_project_name }}'
    new_project_name = get_valid_input("Enter the new project name: ")

    old_app_name = '{{ your_app_name }}'
    new_app_name = get_valid_input("Enter the new app name: ")

    use_celery = get_yes_no_input("Use Celery (y/n): ")
    use_redis = get_yes_no_input("Use Redis (y/n): ")

    branch_decision = use_celery + use_redis
    if branch_decision == "nn":
        change_git_branch("without_celery_and_redis")
    elif branch_decision == "yn":
        change_git_branch("without_redis")
    elif branch_decision == "ny":
        change_git_branch("without_celery")

    remove_git_connection()
    initialize_new_git()

    subprocess.run("git", "remote", )

    # main(root_dir, old_project_name, new_project_name)
    # main(root_dir, old_app_name, new_app_name)
