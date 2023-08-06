import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalrcore-deng",
    version="0.9.2",
    author="mandrewcito",
    author_email="anbaalo@gmail.com",
    description="修改说明：1、fork原库，在原库的基础上修复了一些多线程相关的BUG；2、支持设置网络代码，方便fiddler等软件抓包；（仅项目自用，其余用途建议直接使用原库signalrcore的最新版）",
    keywords="signalr core client 3.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_file="LICENSE",
    url="https://github.com/mandrewcito/signalrcore",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        "requests>=2.22.0",
        "websocket-client==1.0.0",
        "msgpack==1.0.2"
    ]
)
