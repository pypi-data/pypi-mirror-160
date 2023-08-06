from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent


VERSION = '0.0.5'
DESCRIPTION = 'A basic gradio class and class function wrapper'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="gradioWrapper",
    version=VERSION,
    author="LucaVivona (Luca Vivona)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/LVivona/gradio_wrap",
    install_requires=['gradio'],
    keywords=['python', 'sockets', 'artificial intelligence', 'machine learning', 'visualizatio', 'wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)