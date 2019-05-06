# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name="algo",
    version="1.0",
    keywords=("images", "review status", "review result", "algorithm"),
    description="images review algorithm",
    long_description="An algorithm for intelligent images review",
    license="MIT Licence",
    url="https://www.qipeipu.com",
    author="yang zhifan",
    author_email="yangzhifan@qipeipu.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'SQLAlchemy',
        'numpy',
        'pandas',
        'PyMySQL',
        'pyyaml',
        'pytorch',
        'torchvision',
        'pillow',
        'opencv-python',
        'pytesseract',
        'tesseract-ocr'
    ])
