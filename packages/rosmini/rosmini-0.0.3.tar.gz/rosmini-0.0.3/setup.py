from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
    'Natural Language :: English'
]


setup(
    name='rosmini',
    version='0.0.3',
    description='ROS Mini',
    # long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='FelipeVein',
    author_email='veinfelipe@hotmail.com',
    entry_points='''
        [console_scripts]
        rosminicore=rosmini.__main__:rosminicore
        rostopiclist=rosmini.__main__:rostopiclist
        ''',
    url='',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[''],
    keywords='ros rosmini'
)