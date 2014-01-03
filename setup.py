try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [r for r in map(str.strip, open('requirements.txt').readlines())]
exec([v for v in open('pluto/__init__.py') if '__version__' in v][0])

setup(
    name='pluto',
    version=__version__,
    author='Aaron Westendorf',
    author_email="aaron.westendorf@gmail.com",
    packages=['pluto'],
    url='https://github.com/agoragames/pluto',
    license='LICENSE.txt',
    description="Celery-based framework for building analytics engines",
    long_description=open('README.rst').read(),
    keywords=['python', 'analytics', 'celery'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2.7',
    ]
)
