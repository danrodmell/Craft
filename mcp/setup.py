from setuptools import setup, find_packages

setup(
    name="mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "pytest>=7.0.0",
        "flake8>=4.0.0",
        "black>=22.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "anyio>=4.5",
        "httpx>=0.27",
        "httpx-sse>=0.4",
        "pydantic>=2.7.2,<3.0.0",
        "starlette>=0.27",
        "sse-starlette>=1.6.1",
        "pydantic-settings>=2.5.2",
        "uvicorn>=0.23.1",
        "websockets>=15.0.1"
    ],
    python_requires=">=3.10",
) 