from setuptools import setup, find_packages

setup(
    name="autopwn-suite",
    version="2.1.1",
    description="AutoPWN Suite is a project for scanning vulnerabilities and exploiting systems automatically.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GamehunterKaan",
    url="https://auto.pwnspot.com",
    project_urls={
        "Documentation": "https://auto.pwnspot.com",
        "Source": "https://github.com/GamehunterKaan/AutoPWN-Suite",
        "Tracker": "https://github.com/GamehunterKaan/AutoPWN-Suite/issues",
    },
    license="EULA",
    install_requires=["requests", "rich", "python-nmap", "bs4", "distro"],
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["modules/data/*"]},
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Environment :: Console",
        "Topic :: Security",
    ],
    entry_points={
        "console_scripts": [
            "autopwn-suite = autopwn_suite.autopwn:main",
        ],
    },
)
