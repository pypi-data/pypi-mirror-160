from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='qflash_jwt_package',
    version='0.0.4',
    url='https://github.com/Quasar-Flash',
    license='MIT License',
    author='Marlon Martins',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='marlon.martins@qflash.com.br',
    keywords='Package',
    description=u'a small package for implement jwt security in API',
    packages=['qflash_jwt_package'],
    install_requires=['fastapi', 'pyjwt==1.7.1'],
)