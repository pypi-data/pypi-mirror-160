import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neurosec",
    version="1.0.0",
    author="stdp",
    author_email="info@stdp.io",
    description="A neuromorphic inference wrapper for the popular VidGear video processing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://stdp.io",
    keywords=[
        "stdp",
        "stdp.io",
        "neuromorphic",
        "security",
        "akida",
        "brainchip",
        "camgear",
        "vidgear",
        "streaming",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/stdp/neurosec/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={"neurosec": ["templates/*", "models/*"]},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "vidgear[core]",
        "numpy",
        "akida",
        "akida-models",
        "opencv-python",
        "imutils",
        "flask",
    ],
)
