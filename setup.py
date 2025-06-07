
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-web-scraper",
    version="1.0.0",
    author="Ayush Padhy",
    author_email="ayushpadhy2001@gmail.com",
    description="AI-Powered Agentic Web Scraping Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agentic-web-scraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "beautifulsoup4>=4.13.4",
        "lxml>=5.4.0",
        "openai>=1.84.0",
        "requests>=2.32.3",
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agentic-scraper=agentic_scraper.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "agentic_scraper": ["templates/*.json", "configs/*.yaml"],
    },
)
