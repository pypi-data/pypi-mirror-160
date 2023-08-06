import setuptools




setuptools.setup(
    name='trisigma',
    version='0.0.1',
    author='Arda Gok',
    author_email='ardagkmhs@gmail.com',
    description='Algorithmic trading framework',
    long_description="",
    long_description_content_type="text/markdown",
    url='https://github.com/ArdaGk/trisigma',
    project_urls={
    },
    license='MIT',
    packages=['trisigma'],
    install_requires=['requests', 'plotly', 'numpy', 'pandas', 'gspread', 'binance-connector', 'google-cloud-storage', 'ibapi'],
)


