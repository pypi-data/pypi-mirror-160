import subprocess
import shutil
import os

if __name__ == "__main__":
    # Remove /dist folder
    if os.path.exists("./dist"):
        shutil.rmtree("./dist")
    # Build package
    subprocess.call(["python", "-m", "build"])
    # Publish to PyPI
    # subprocess.call(
    #     ["python", "-m", "twine", "upload", "--repository", "testpypi", "dist/*"]
    # )
    subprocess.call(["python", "-m", "twine", "upload", "dist/*"])
    # Example test installation from TestPyPI
    # --extra-index-url to download dependencies from PyPI
    # pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple FanTeX
