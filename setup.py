import setuptools
from aks import __version__

try:
    long_desc = open("README.md").read()
except IOError:
    long_desc = "Failed to read README.md"

setuptools.setup(
    name="aks",
    version=__version__,
    url="https://t.me/aks",

    author="AKS",
    author_email="AKKS@GMAIL.COM",

    description="A Telegram bot",
    long_description=long_desc,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages(),

    install_requires=[
        "aiohttp>=3",
        "telethon>=1.10",
        "yarl>=1",
    ],
    extras_require={
        "fast": ["cryptg>=0.2"],
    },
    python_requires="~=3.7",

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Framework :: AsyncIO",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points="""
        [console_scripts]
        aks=aks.__main__:main
    """,
)
