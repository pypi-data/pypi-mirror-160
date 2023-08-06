from setuptools import setup

setup(
    name='caworker',
    version='0.1.2',
    description='Camunda Worker',
    url='https://github.com/gpcortes/caworker.git',
    author='Gustavo Côrtes',
    author_email='gpcortes@gmail.com',
    license='BSD 2-clause',
    packages=['caworker'],
    install_requires=[
        'requests>=2.27.1', 'pycamunda>=0.6.1', 'python-dotenv>=0.19.2'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)
