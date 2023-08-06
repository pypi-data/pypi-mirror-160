from setuptools import setup, find_packages


setup(
    name='kloockyDE_test',
    version='0.6',
    license='MIT',
    author='Stephan Kloock',
    author_email='kloock.stephan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='private',
    install_requires=[
        'pywin32',
        'mysql',
        'Pillow',
        'infinity',
        'pyautogui'
    ],

)
