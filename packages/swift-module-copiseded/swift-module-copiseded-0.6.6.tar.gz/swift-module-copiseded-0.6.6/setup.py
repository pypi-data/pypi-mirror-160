import setuptools

with open("README.rst", "r",encoding = "UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swift-module-copiseded",
    version="0.6.6",
    author="Monkey Hammer Copiseded",
    author_email="Wf6350177@163.com",
    description="本次更新并没有改变上次的库，而是将地址修改，本次更新将淘汰之前的旧版github库，将会开启一个新的库，你可以在这儿获取主要文件夹，本次更新将会在下载文件上做改变。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monkeyhammercopiseded/swift-module-copiseded-new-/",
    project_urls={
        "Bug Tracker": "https://github.com/monkeyhammercopiseded/swift-module-copiseded-new-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "swift apple"},
    packages=setuptools.find_packages(where="swift apple"),
    python_requires=">=3.6",
)
