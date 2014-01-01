from setuptools import setup, find_packages 

setup(
    name="sentipy",
    version="0.0.1",
    keywords = ('sentiment analysis'), 
    description="Sentiment analysis based on sentiment word strength.",
    author="Jay Cheng",
    author_email="googcheng@gmail.com",
    url = "https://github.com/goog/sentiPY",
    license = 'MIT License',
    include_package_data=True,
    packages=['sentipy'],
    package_dir = {'sentipy': 'sentipy'},
    package_data = {"sentipy": ["data/*"]},
    install_requires=[
        "numpy >= 1.6.1",
        "pymongo >= 2.6",
    ],
    platforms = 'any',
)
