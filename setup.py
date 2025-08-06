from setuptools import setup, find_packages

setup(
    name="ecg_receiver",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.5',
        'numpy>=1.24.0',
        'PyQt5>=5.15.0',
        'pyqtgraph>=0.13.0',
        'requests>=2.28.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ecg-receiver=ecg_receiver.main:main',
        ],
    },
    author="qiao",
    author_email="126.com",
    description="A comprehensive ECG receiver with AI-powered heart diagnosis using Gemini 2.5 Flash",
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
