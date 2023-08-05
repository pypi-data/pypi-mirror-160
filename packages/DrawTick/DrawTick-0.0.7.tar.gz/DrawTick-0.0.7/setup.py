from setuptools import setup, find_packages

setup(
        name='DrawTick',
        version='0.0.7',
        keywords = ["pip", "DrawTick"],
        description= "DrawTick",
        license = "MIT Licence",
        url='https://www.baidu.com',
        author='liujun',
        author_email='62462156@qq.com',
        packages=find_packages(include=["DrawTick", "DrawTick.*"],),
        include_package_data=True,
        platforms=['all'],
        install_requires=["datetime","pandas", "matplotlib", "mpl_finance", "numpy"]
)
