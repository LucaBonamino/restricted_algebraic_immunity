import argparse
import enum
import platform
import sys
import os

class HostingLocation(enum.Enum):
    GITHUB = 'github'
    ZENODO = 'zenodo'

def get_wheel_url(version: str, hosting_location: HostingLocation) -> str:
    idx = '15042593' if version == '0.1.0' else '15290894'
    base_url = f"https://github.com/LucaBonamino/restricted_algebraic_immunity/releases/download/{version}/"\
        if hosting_location == HostingLocation.GITHUB else f"https://zenodo.org/record/{idx}/files/"
    python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    system = platform.system()
    architecture = platform.machine()

    if system == "Linux":
        if architecture == "x86_64":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
        elif architecture == "aarch64":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"
    elif system == "Windows":
        if architecture == "AMD64":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-win_amd64.whl"
        elif architecture == "x86":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-win32.whl"
    elif system == "Darwin":
        if architecture == "x86_64":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-macosx_10_9_x86_64.whl"
        elif architecture == "arm64":
            wheel_file = f"algebraic_immunity_utils-{version}-{python_version}-{python_version}-macosx_11_0_arm64.whl"
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
    parser = argparse.ArgumentParser(
        prog='ConstructWheelURL',
        description='Construct the URL of the algebraic_immunity_utils package wheel corresponding to your system',
    )
    parser.add_argument('-v', '--version', help='version of the package release', type=str, default='0.2.0')
    parser.add_argument('-l', '--location', type=lambda a: HostingLocation(a),
                        default=HostingLocation.GITHUB.value, help='location hosting the wheels: GITHUB or ZENODO - default GITHUB')
    args = parser.parse_args()
    print(get_wheel_url(version=args.version, hosting_location=args.location))