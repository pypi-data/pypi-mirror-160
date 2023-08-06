from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='rayasdk',
    packages=find_packages(),
    version='1.0.10',
    license='MIT',
    description='Raya SDK - Unlimited Robotics Software Development Kit',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Unlimited Robotics',
    author_email='camilo@unlimited-robotics.com',
    url='',
    python_requires=">=3.8",
    download_url = '',
    package_data={'':['./template/*']},
    keywords = ['robotics', 'unlimited-robotics', 'gary'],
    install_requires=[
        'tabulate',
        'importlib_metadata',
        'tqdm',
        'docker',
        'progressbar',
        'simple_file_checksum'
    ],
    entry_points={
        'console_scripts': [
            'rayasdk = rayasdk.__main__:main',
        ],
    },
)