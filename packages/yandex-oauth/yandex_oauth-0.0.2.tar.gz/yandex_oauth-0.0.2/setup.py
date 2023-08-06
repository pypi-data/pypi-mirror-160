from setuptools import setup, find_packages
from os.path import join, dirname
import yandex_oauth

setup(
    name='yandex_oauth',
    version=yandex_oauth.__version__,
    packages=find_packages(),
    description='yandex_oauth - Yandex OAuth Lib',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author=yandex_oauth.__author__,
    author_email='ya360@uh.net.ru',
    maintainer=yandex_oauth.__author__,
    maintainer_email='ya360@uh.net.ru',
    download_url='https://github.com/imercury13/yandex_oauth',
    #url='https://ya360.uh.net.ru',
    license='GPL-3.0',
    project_urls={
        #"Documentation": "https://ya360.readthedocs.io/",
        "Bug Tracker": "https://github.com/imercury13/yandex_oauth/issues"
    },
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Intended Audience :: System Administrators'

    ],
    install_requires=[
		'requests',
    ],
    include_package_data=True,
)
