from setuptools import setup, find_packages

setup(
    name="mcp_service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-dotenv>=0.19.0",
        "mcp>=0.0.1.dev385"
    ],
    python_requires=">=3.10",
) 