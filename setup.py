import setuptools


setuptools.setup(
    name="valleytext",
    version="0.1",
    url='https://github.com/yzho0907/valleytext.git',
    author='young, xiuzhizheng',
    author_email='598299410@qq.com, xiuzhi_zxz@163.com',
    description='Extract keywords from sentences.',
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
