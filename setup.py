from setuptools import find_packages, setup

setup(
    name='book_writer',
    version='0.0.2-alpha',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'bootstrap-flask',
        'flask-paginate',
        'flask-wtf',
        'email_validator',
        'python-dotenv',
        'pytest'
    ],
)
