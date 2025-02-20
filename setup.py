from setuptools import setup, find_packages

__version__ = "0.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()



setup(
    name="restricted_algebraic_immunity",
    version=__version__,
    description="Restricted Algebraic Immunity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=read_requirements(),
    url="https://github.com/LucaBonamino/restricted_algebraic_immunity-immunity.git",
    package_data={
        'algebraic_immunity': ['full_reed_muller/pre_computation/*'],
    },
    packages=find_packages(where="src", include=["restricted_algebraic_immunity*"]),
    package_dir={"": "src"},
    zip_safe=False,
    console_scripts={
            "restrictedAI": "restricted_algebraic_immunity.entry_point:main"
    }
)
