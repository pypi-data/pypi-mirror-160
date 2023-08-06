from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
    'Natural Language :: English'
]


setup(
    name='rosmini',
    version='0.0.2',
    description='ROS Mini',
    # long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='FelipeVein',
    author_email='veinfelipe@hotmail.com',
    url='',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[''],
    keywords='ros rosmini'
)