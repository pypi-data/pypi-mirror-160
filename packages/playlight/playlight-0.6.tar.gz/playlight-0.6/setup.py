import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="playlight",
    version="0.6",
    author="TEARK",
    author_email="913355434@qq.com",
    description="基于playwright的通用版本，简约并提升稳定性。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/teark/playlight.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'playwright',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
