from setuptools import setup
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='flyers',
    version='0.0.2',
    author='pushyzheng',
    author_email='1437876073@qq.com',
    url='https://github.com/pushyzheng',
    description=u'A collections of utils',
    packages=['flyers'],
    install_requires=install_requires
)
