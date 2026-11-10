from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name="py_qive",
    version="0.1.0",
    license="MIT License",
    author="Yuri Gomes",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="yurialdegomes@gmail.com",
    keywords="qive arquivei nfe nfse cte mdfe",
    description="Wrapper não oficial da API Qive (Arquivei)",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.8",
)
