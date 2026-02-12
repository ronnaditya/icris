from setuptools import setup, find_packages

setup(
    name='icris_automation',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'python_docx>=0.8.10',
        'selenium>=3.141.0',
        'pandas>=0.24.2',
        'docx>=0.2.4'
    ],
    description="A Python framework for automating various tasks on the Hong Kong government's ICRIS website'",
    long_description="""**icris_automation** is a Python package that  provides convenient classes based on the Page Object Model to make redundant tasks such as document purchasing from the Hong Kong goevernment's ICRIS website convenient and efficient. The package is highly modularized, making it easy to modify and extend the functionality provided. In the context of this project, an `identifier` is a registered company name or a Companies Registry Number through which a coporate entity in Hong Kong can be identified independently.""",
    author='Aditya Verma',
    author_email='verma.aditya.415@gmail.com',
    license='MIT',
)