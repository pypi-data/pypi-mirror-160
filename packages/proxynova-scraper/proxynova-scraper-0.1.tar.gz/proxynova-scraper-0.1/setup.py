from setuptools import find_packages, setup
setup(
    name='proxynova-scraper',
    packages=find_packages(),
    version='0.1',
    description='Package to get proxies from proxynova.com via web scraping',
    author='German Martinez Solis',
    author_email='german.mtz.solis@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/GermanMtzmx/proxynova_scraper",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['bs4', 'html5lib', 'pyppeteer', 'asyncio', 'unidecode'],
    python_requires='>=3',
)