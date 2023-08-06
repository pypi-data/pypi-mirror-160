from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='fixedfloat-py',
    version='0.1.5',
    description='Python module for FixedFloat API',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='mpp1337',
    author_email='maxx_uae@protonmail.com',
    keywords=['FixedFloat', 'FixedFloat API', 'Exchanger', 'Crypto'],
    url='https://github.com/mpp1337/fixedfloat-py',
    download_url='https://pypi.org/project/fixedfloat-py/'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
