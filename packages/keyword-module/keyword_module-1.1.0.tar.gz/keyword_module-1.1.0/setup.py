from setuptools import setup,find_packages


setup(
    name='keyword_module',
    version='1.1.0',
    description='keyword_module',
    author='birdcrane',
    author_email='hsblhs2808@gmail.com',
    url=None,
    py_modules=['text2keyword'],
    packages=find_packages(),
    install_requires=[
        'sentence_transformers',
        'numpy',
        'sklearn',
        'konlpy'
    ],


)
