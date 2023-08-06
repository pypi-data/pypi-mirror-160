import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brudercropper",
    version="0.1.7",
    author="Niggo",
    description="Croppt Zeug auf 62mm für Bruderlabeldrucker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "imutils",
        "numpy",
        "opencv-python",
        "packaging",
        "Pillow",
        "pylibdmtx",
        "pyparsing",
        "pytesseract",
        "python-barcode"
    ],
    classifiers=[
        # "Development Status :: 3 - Alpha"
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'brudercrop = brudercropper.crop:main',
        ],
    }
)