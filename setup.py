from setuptools import setup, find_packages

setup(
    name="data_cleaning_agent",
    version="1.0.0",
    description="A Streamlit app for generating data cleaning recommendations using OpenAI GPT.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sandeep Kumar Palit",
    author_email="sandeepkrpalit@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.25.0",
        "openai>=0.27.8",
        "pandas>=1.5.3",
        "numpy>=1.23.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "run_cleaning_agent = data_cleaning_agent.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
