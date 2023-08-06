from setuptools import setup

readme = open('README.md').read()

setup(
    name='sqlalchemy-mogdb',
    version='0.1.2',
    description='Enmotech MogDB Dialect for SQLAlchemy',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='Enmotech',
    maintainer='Vimiix',
    maintainer_email='i@vimiix.com',
    license="MIT",
    url='https://gitee.com/enmotech/sqlalchemy-mogdb',
    packages=['sqlalchemy_mogdb'],
    keywords='Enmotech MogDB',
    install_requires=[
        'SQLAlchemy',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'mogdb = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2',
            'mogdb.psycopg2 = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2',
            'mogdb.psycopg2cffi = sqlalchemy_mogdb.dialect:MogDBDialect_psycopg2cffi',
        ]
    },
)
