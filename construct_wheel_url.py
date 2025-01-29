import platform
import sys
import os

def get_wheel_url():
    base_url = "https://github.com/programmingAthlete/alegebraic_immunity_utils/releases/download/1.4.1/"
    python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    system = platform.system()
    architecture = platform.machine()

    if system == "Linux":
        if architecture == "x86_64":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
        elif architecture == "aarch64":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"
    elif system == "Windows":
        if architecture == "AMD64":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-win_amd64.whl"
        elif architecture == "x86":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-win32.whl"
    elif system == "Darwin":
        if architecture == "x86_64":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-macosx_10_9_x86_64.whl"
        elif architecture == "arm64":
            wheel_file = f"algebraic_immunity_utils-1.4.1-{python_version}-{python_version}-macosx_11_0_arm64.whl"
    else:
        raise Exception(f"Unsupported platform: {system} {architecture}")

    return base_url + wheel_file

def install_wheel():
    try:
        wheel_url = get_wheel_url()
        os.system(f"pip install {wheel_url}")
        print(f"Successfully installed from {wheel_url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(get_wheel_url())
