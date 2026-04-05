import os

# Root project folder
BASE_DIR = "webapp"

# Folder structure
folders = [
    "app",
    "app/models",
    "app/schemas",
    "app/auth",
    "app/users",
    "app/media",
    "app/uploads"
]

# Files to create
files = [
    "app/main.py",
    "app/database.py",
    "app/config.py",

    "app/models/user.py",
    "app/models/media.py",

    "app/schemas/user.py",
    "app/schemas/media.py",

    "app/auth/routes.py",
    "app/auth/utils.py",
    "app/auth/dependencies.py",

    "app/users/routes.py",

    "app/media/routes.py",
    "app/media/utils.py",

    "requirements.txt",
    ".env"
]


def create_structure():
    print("🚀 Creating FastAPI project structure...\n")

    # Create base directory
    os.makedirs(BASE_DIR, exist_ok=True)

    # Create folders
    for folder in folders:
        path = os.path.join(BASE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"📁 Created folder: {path}")

    # Create files
    for file in files:
        path = os.path.join(BASE_DIR, file)
        with open(path, "w") as f:
            pass
        print(f"📄 Created file: {path}")

    print("\n✅ Project structure created successfully!")


if __name__ == "__main__":
    create_structure()