import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="korcen test",  # Replace with your own PyPI username(id)
    version="0.0.1",
    author="Tanat",
    author_email="shrbwjd05@naver.com",
    description="korcen 테스트 버전",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/KR-korcen/korcen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["better_profanity"],
    python_requires='>=3.6',
)
