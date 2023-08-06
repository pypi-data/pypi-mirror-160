import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name="flask_fuzhu",
    version="0.0.6",
    author="littlx",
    author_email="littlx@qq.com",
    description="practice build package",
    long_description=long_description,
    long_description_contet_type="text/markdown",
    # url="github.com/littlx/flask_fuzhu",
    packages=setuptools.find_packages(),
    install_requires=["flask"],
    python_requires=">=3.9",
)
