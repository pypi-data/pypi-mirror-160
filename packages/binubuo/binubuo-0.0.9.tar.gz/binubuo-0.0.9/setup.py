from setuptools import setup, find_packages
from pathlib import Path

readme = """# Binubuo

Binubuo python library is a powerful client to the Binubuo Synthetic Data API from [**https://binubuo.com**](https://binubuo.com/ords/r/binubuo_ui/binubuo). The API can be used to create dynamic an realistic looking synthetic data that can be used very easily for functional and performance testing as well as validating database design. One major strength of the Binubuo client, is that it integrates tightly with your database, and can use your existing design and data to create new synthetic data. This means that you can very quickly create test data from production data, that can be used by everyone in your organisation without worrying about data protection and other legal or regulatory requirements. The data will look like your production data, except it will be randomly created.

**Highlighted Features**

- 150+ Reeal life data generators
- Pre made dataset creators for very quick prototyping
- Postgres and Oracle integration
- Create synthetic dataset creators directly from your table definition

## Installing Binubuo client and supported versions

Binubuo is available and installable from PyPI:

    $ python -m pip install binubuo

Binubuo officially supports Python 2.7 & 3.6+.

## Registering an account

You can register an account on the website; just click the "Sign up" link in the menu bar or click the "Create account now!" button on the front page, or you can create an account from the client itself. Just run the ```create_account``` function and supply an account name and email for the registration.:

```python
>>> from binubuo import binubuo
>>> b = binubuo()
>>> b.create_account("my_account_name", "my_email@example.com")
Please go to this url in your browser: https://binubuo.com/ords/r/binubuo_ui/binubuo/challenge-response?p_sha=1311FE507E555130581C2E70000
Please input the code displayed in the above URL: 468039
Your API key for Binubuo is (please save it.): 2C48D11E2BCE3731DD0E22E8EEA584A6F756BED5
>>> b.key("2C48D11E2BCE3731DD0E22E8EEA584A6F756BED5")
```

That is it. You are now ready to use the Binubuo client.


## Documentation

Client documentation [Available here](https://binubuo.com/ords/r/binubuo_ui/binubuo/binubuo-documentation-page?p23_page_name=Python&p23_section_id=240&p23_section_name=Clients)

Binubuo includes more than 150+ real life data generators: [Data Generators Documentation and API Reference](https://binubuo.com/ords/r/binubuo_ui/binubuo/binubuo-documentation-section?p22_section_name=Reference)

## Quick example

You can go ahead and use the client without an account using a temporary access key, although your data rate and ability to store settings and datasets are limited. Simply start the client and start generating data:

```python
>>> from binubuo import binubuo
>>> b = binubuo()
>>> print(b.generate('person', 'full_name'))
Andrew Howard
>>> print(b.generate('finance', 'bank_account_id'))
GE02Pu5783332775138823
>>> print(b.generate('consumer', 'food_item'))
Pumpkin Spice, Atlantic Salmon, 2 Bonless Fillets
>>> print(b.generate('time', 'date'))
1945-02-10T17:37:09Z
```

## Using the client with a database

One of the strengths of **Binubuo** is that you can use your existing tables and data to very quickly create synthetic data creators, enabling you to create the perfect test data that matches your real data, both the way it looks (data domain) but equally important, also the way the data is distributed and formatted.

Databases currently supported:

- **Oracle** (cx_Oracle library required)
- **Postgres** (psycopg2 library required)
- **Yugabyte** (psycopg2 library required)

Here is a quick postgres example, that will create a copy of the sample schema table customer, called customer_copy with 100 rows of synthetic data:

```python
>>> from binubuo import binubuoPostgres
>>> bo = binubuoPostgres('394129D632B0A4E9913E491286EB428DD80CEFF0', 'binu', 'postgres', 'mypassword')
>>> bo.copy_table(source_table='customer', target_table='customer_copy', copy_method='dataset', drop_target_if_exist=True, alternate_dataset_name=False, use_comments=False, use_infer=True, use_sample_data=True, data_rows=100)
```

That is how quickly you can create test data. For detailed documentation and reference commands, take a look at the [**docs online**](https://binubuo.com/ords/r/binubuo_ui/binubuo/binubuo-documentation)
"""

packages = ['binubuo']

requires = [
    'requests>=2.0.0; python_version >= "3"'
]

setup(
    name='binubuo',
    version='0.0.9',
    description='Client package for Binubuo synthetic data generator',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://binubuo.com',
    author='Morten',
    author_email='morten@binubuo.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing :: Mocking',
        'Topic :: Utilities',
    ],
    keywords='synthetic, testdata, mocking',
    packages=packages,
    package_dir={'binubuo': 'binubuo'},
    install_requires=requires,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    project_urls={  # Optional
        'Documentation': 'https://binubuo.com/ords/r/binubuo_ui/binubuo/resources',
        'Bug Reports': 'https://github.com/morten-egan/binubuo-python-client/issues/new'
    },
)