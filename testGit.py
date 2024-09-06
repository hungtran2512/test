import cv2
import os
import subprocess
import requests

# Cấu hình GitHub
repository_url = "https://github.com/hungtran2512/test.git"
local_repo_path = r"C:\\Users\\trang\\OneDrive\\Desktop\\test"  # Đường dẫn lưu ảnh

def get_next_image_number(path):
    """Lấy số tiếp theo cho tên ảnh."""
    files = os.listdir(path)
    numbers = []
    for file in files:
        if file.endswith(".jpg"):
            try:
                number = int(file.split('.')[0].split('_')[-1])
                numbers.append(number)
            except ValueError:
                pass
    return max(numbers, default=0) + 1

def run_git_command(command):
    """Chạy lệnh Git và xử lý lỗi."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi chạy lệnh Git '{' '.join(command)}': {e}")

def check_git_status():
    """Kiểm tra trạng thái repository Git."""
    run_git_command(["git", "status"])

def check_for_commits():
    """Kiểm tra xem có thay đổi nào đã được commit."""
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
    if result.stdout:
        print("Có thay đổi đã được staged và commit.")
        return True
    else:
        print("Không có thay đổi nào để commit.")
        return False

def create_new_branch(branch_name):
    """Tạo nhánh mới và chuyển sang nhánh đó."""
    run_git_command(["git", "checkout", "-b", branch_name])
    print(f"Đã tạo và chuyển sang nhánh {branch_name}.")

def delete_file_from_git(image_name, image_path):
    """Xóa file khỏi hệ thống và GitHub."""
    confirm = input(f"Bạn có chắc chắn muốn xóa {image_name}? (y/n): ")
    if confirm.lower() == 'y':
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Ảnh {image_name} đã được xóa khỏi local.")

            # Xóa file khỏi GitHub
            run_git_command(["git", "rm", image_name])
            run_git_command(["git", "commit", "-m", f"Remove image: {image_name}"])
            run_git_command(["git", "push"])
            print(f"Ảnh {image_name} đã được xóa khỏi GitHub.")
        else:
            print(f"File {image_name} không tồn tại.")
    else:
        print("Xóa ảnh đã bị hủy.")

# Lựa chọn chức năng tương tác
print("Chọn một trong các chức năng sau:")
print("1: Add & Commit")
print("2: Push")
print("3: Pull")
print("4: Tạo nhánh mới")
print("5: Xóa file")
choice = input("Lựa chọn của bạn: ")

if choice == '1':
    run_git_command(["git", "add", "."])
    commit_message = input("Nhập thông điệp commit: ")
    run_git_command(["git", "commit", "-m", commit_message])
elif choice == '2':
    if check_for_commits():
        run_git_command(["git", "push", "--set-upstream", "origin", "main"])
elif choice == '3':
    run_git_command(["git", "pull", "origin", "main"])
elif choice == '4':
    branch_name = input("Nhập tên nhánh mới: ")
    create_new_branch(branch_name)
elif choice == '5':
    image_name = input("Nhập tên file ảnh muốn xóa (ví dụ: captured_image_1.jpg): ")
    image_path = os.path.join(local_repo_path, image_name)
    delete_file_from_git(image_name, image_path)
else:
    print("Lựa chọn không hợp lệ.")
