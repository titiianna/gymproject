import json
import os

class FileHandler:
    @staticmethod
    def ensure_data_dir(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except:
            return False

    @staticmethod
    def save_to_json(file_path, data):
        try:
            FileHandler.ensure_data_dir(os.path.dirname(file_path) or ".")
            tmp_path = file_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, file_path)
            return True
        except:
            return False

    @staticmethod
    def load_from_json(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None

    @staticmethod
    def txt_append(file_path, content):
        try:
            FileHandler.ensure_data_dir(os.path.dirname(file_path) or ".")
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content)
            return True
        except:
            return False

    @staticmethod
    def txt_write(file_path, content):
        try:
            FileHandler.ensure_data_dir(os.path.dirname(file_path) or ".")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except:
            return False

    @staticmethod
    def txt_read(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().splitlines()
        except:
            return []

    @staticmethod
    def export_users_txt(file_path, users_dict):
        lines = ["Name | Username | Role | Email | Account status"]
        for user in users_dict.values():
            status = "Active" if user.is_active else "Inactive"
            lines.append(f"{user.name} | {user.username} | {user.role} | {user.email} | {status}")
        return FileHandler.txt_write(file_path, "\n".join(lines) + "\n")
