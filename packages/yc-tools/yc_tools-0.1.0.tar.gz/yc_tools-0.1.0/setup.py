from setuptools import setup
from setuptools import find_packages
requires = ["datetime>=4.0","openpyxl>=3.0.0","pyserial>=3.5"]
setup(
    name='yc_tools',
    version='0.1.0',
    description='yc_tools',
    author='Susunl',
    author_email='1253013130@qq.com',
    long_description_content_type ='text/markdown',
    license='MIT',
    packages = find_packages(),
    include_package_data = True,
    python_requires=">=3.5",
    zip_safe=False,
    platforms = 'any',
    install_requires = requires,
    classifiers=[ 'Programming Language :: Python :: 3'],
)
