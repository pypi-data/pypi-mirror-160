from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    # 'Operating System :: POSIX :: LINUX',
    # 'license :: MIT License',
    # 'Programming Language :: python :: 3'
]


setup(
    name='fpkbasiccalculator',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('readme.txt').read()+ '\n\n' + open('changelog.txt').read(),
    url='',
    author='Md Faisal Alam',
    author_email='faisalgbox@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)

