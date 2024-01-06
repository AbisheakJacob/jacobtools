import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='jacobtools',
    version='0.0.9',
    author='Abisheak Jacob J',
    author_email='abisheakjacob0032@gmail.com',
    description='my package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AbisheakJacob/jacobtools',
    project_urls = {
        "Bug Tracker": "https://github.com/Muls/toolbox/issues"
    },
    license='MIT',
    packages=['jacobtools'],
    install_requires=['pandas', 'psycopg2', 'sqlalchemy', 'more-itertools'],
)
