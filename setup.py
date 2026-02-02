"""Setup configuration for chordify-agent package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chordify-agent",
    version="1.0.0",
    author="2nist",
    author_email="",
    description="MIDI chord recognition and analysis with fallback to music21 heuristics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2nist/chordify-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mido>=1.2.0",
        "music21>=5.0.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
    },
)
