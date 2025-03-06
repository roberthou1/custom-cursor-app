from setuptools import setup, find_packages

setup(
    name="custom-cursor-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.5.0",
        "pillow>=9.5.0",
        "pywin32>=306; sys_platform == 'win32'",
        "pyobjc-framework-Cocoa>=9.0; sys_platform == 'darwin'",
    ],
    entry_points={
        "console_scripts": [
            "custom-cursor-app=src.main:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A cross-platform application to set custom PNG images as your cursor",
    keywords="cursor, custom, png, mac, windows",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
)
