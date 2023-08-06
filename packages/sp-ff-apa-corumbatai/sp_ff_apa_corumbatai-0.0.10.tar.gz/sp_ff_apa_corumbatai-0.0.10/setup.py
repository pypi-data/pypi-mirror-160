from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = []
for line in open('requirements.txt', encoding='utf-8'):
    li = line.strip()
    if not li.startswith('#'):
        requirements.append(line.rstrip())


VERSION = (0, 0, 10)
__version__ = '.'.join(map(str, VERSION))


setup(
    name='sp_ff_apa_corumbatai',
    version=__version__,
    author='Michel Metran',
    author_email='michelmetran@gmail.com',
    description='Compartilhamento de Dados Espaciais',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/open-geodata/sp_ff_apa-corumbatai',
    keywords='python, dados espaciais, geoprocessamento',

    # Python and Packages
    python_requires='>=3',
    install_requires=requirements,

    # Entry
    # Our packages live under src but src is not a package itself
    package_dir={'': 'src'},

    # Quando são diversos módulos...
    packages=find_packages('src', exclude=['test']),

    # Dados
    include_package_data=True,
    package_data={'': ['data/output/zips/*.7z']},

    # Classificação
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese',
        'Intended Audience :: Developers',
    ],
)
