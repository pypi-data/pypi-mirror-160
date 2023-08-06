from setuptools import setup,find_packages
setup(
       name="ly-message",
       version="0.1",
       author="刘煜",
       url="http://www.baidu.com",
       packages=find_packages("src"),
       package_dir = {"":"src"},
       package_data = {"":["*.txt","*.info","*.properties","*.py"],
                          "":["data/*.*"],
       },
       exclude = ["*.test","*.test.*","test.*","test"]
)
