from setuptools import setup

setup(
    name='lw-spapi',
    version='1.0.3',
    packages=[
        'spapi',
    ],
    url='https://www.lifewit.cn',
    license='',
    author='liftwit',
    author_email='jiangzuojia@lifewit.com',
    description='A wrapper to access Amazon Selling Partner API with an easy-to-use SDK.',
    install_requires=[
        'boto3==1.20.26',
        'Flask',
        'pycrypto',
        'redis',
        'requests',
    ],
)
