from setuptools import setup, find_packages

setup(
    name="ecg_receiver",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.5',
        'numpy>=1.24.0',
        'PyQt5>=5.15.0',
        'pyqtgraph>=0.13.0',
    ],
    entry_points={
        'console_scripts': [
            'ecg-receiver=ecg_receiver.main:main',
        ],
    },
    author="qiao",
    author_email="126.com",
    description="A simple ECG receiver for ADS1292R + ESP32",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/simple/ecg-receiver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
