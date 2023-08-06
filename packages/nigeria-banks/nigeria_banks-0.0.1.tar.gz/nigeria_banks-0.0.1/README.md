📦 nigeria_banks
=======================

Cbn Banks is a basic python package that returns details of particular bank in Nigeria.

## Installation

You can install Cbn Bankss from [PyPI](https://pypi.org/project/nigeria_banks/):

    pip install nigeria_banks



## How to use

    $ from nigeria_banks import core
     bank = core.cbn_code("322")
     print(bank)
     ## {'bank_code': '100018', 'cbn_code': '322', 'name': 'Zenith Mobile', 'bank_short_name': 'zenith-mobile', 'disabled_for_vnuban': None}
     
     print(bank['bank_short_name'])
     ## zenith-mobile

     

