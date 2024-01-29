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
        # 파일 내 일치하는 코드 대체
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            replace_word_in_file(file_path, old_project_name, new_project_name, script_path)

        # 디렉토리 명 내 일치하는 코드 대체
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
        subprocess.run(["git", "switch", "-c", branch_name, f"origin/{branch_name}"], check=True)
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


def initialize_new_git(git_url):
    # 입력한 Git URL이 적합한지 확인
    try:
        subprocess.run(["git", "ls-remote", git_url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Invalid or inaccessible Git URL: {e}")
        return False

    remove_git_connection()

    # 입력한 Git URL이 정상적일 경우 기존 Git 초기화 및 remote 연결
    try:
        subprocess.run(["git", "init"], check=True, cwd=root_dir)
        print("Initialized a new Git repository.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing new Git repository: {e}")
        return False

    try:
        subprocess.run(["git", "remote", "add", "origin", git_url], check=True, cwd=root_dir)
        print(f"Added Git remote: {git_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding Git remote: {e}")
        return False

    print("Git repository initialized and remote added successfully.")
    return True


if __name__ == "__main__":
    """
    1. 사용자로부터 project, app name을 입력받아 기존 값 대체
    2. Celery, Redis 사용 유무에 따라 사전에 설정된 코드들이 존재하는 git branch로 switch
    3. 사용자로부터 Git URL을 입력받아 접근 가능한지 확인 후 Git 초기화 및 연결
    """
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

    git_url = input("Enter the Git remote URL: ")
    initialize_new_git(git_url)

    main(root_dir, old_app_name, new_app_name)
    main(root_dir, old_project_name, new_project_name)
