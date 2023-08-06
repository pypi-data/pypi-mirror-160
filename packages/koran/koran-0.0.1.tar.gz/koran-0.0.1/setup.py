import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="koran",  # Replace with your own PyPI username(id)
    version="0.0.1",
    author="Tanat",
    author_email="shrbwjd05@naver.com",
    description="랜덤 한글",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TANAT96564/KBWC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[""],
    python_requires='>=3.6',
)
