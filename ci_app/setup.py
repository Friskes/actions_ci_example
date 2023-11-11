from setuptools import setup


setup(
    name='ci_example',
    version='0.0.1',
    description="Training with GitHub Actions",
    author='Friskes',
    packages=['ci_app'],
    install_requires=['fastapi', 'uvicorn', 'pydantic', 'docker'],
    include_package_data=True,
    keywords=[
        'ci', 'github actions', 'fastapi', 'docker'
    ],
    entry_points={
        'console_scripts': [
            'ci_example = ci_app.app:main']},
)
