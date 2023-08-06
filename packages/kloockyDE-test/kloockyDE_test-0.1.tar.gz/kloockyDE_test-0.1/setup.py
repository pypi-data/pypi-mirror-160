from setuptools import setup, find_packages


setup(
    name='kloockyDE_test',
    version='0.1',
    license='MIT',
    author='Stephan Kloock',
    author_email='kloock.stephan@gmail.com',
    packages=find_packages('dir'),
    package_dir={'': 'dir'},
    keywords='private',
    install_requires=[
        'pywin32',
        'mysql',
        'Pillow',
        'infinity',
        'pyautogui'
    ],

)
