# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['retrrry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'retrrry',
    'version': '3.0.3',
    'description': 'Retry for Python3. No dependency.',
    'long_description': "# Retrrry\n\nDecorate flaky functions with `@retry` to apply retrying logic.\n\nSimplest way to use `retrrry` is actually to copy the code in `retry.py` and use it in your\nproject, since there is no dependencies other than the standard library.\n\n```python\n@retry\ndef unreliable_func():\n    import random\n    if random.randint(0, 10) < 5:\n        raise IOError('Fail')\n    else:\n        return 'Success'\n```\n\n## Configurations\n\n- Specify stop condition (i.e. limit by number of attempts)\n- Specify wait condition (i.e. exponential backoff sleeping between attempts)\n- Specify certain Exceptions\n- Specify expected returned result\n\n## Installation\n\n```sh\npip install retrrry\n```\n\n```python\nfrom retrrry import retry\n```\n\n## Examples\n\nThe default behavior is to retry forever without waiting:\n\n```python\n@retry\ndef never_stop_never_wait():\n    print('Retry forever, ignore Exceptions, no wait between retries')\n    raise Exception\n```\n\nSet the number of attempts before giving up:\n\n```python\n@retry(stop_max_attempt_number=7)\ndef stop_after_7_attempts():\n    print('Stopping after 7 attempts')\n    raise Exception\n```\n\nSet a boundary for time for retry:\n\n```python\n@retry(stop_max_delay=10000)\ndef stop_after_10_s():\n    print('Stopping after 10 seconds')\n    raise Exception\n```\n\nSet wait time between retries:\n\n```python\n@retry(wait_fixed=2000)\ndef wait_2_seconds():\n    print('Wait 2 second between retries')\n    raise Exception\n```\n\nInject some randomness:\n\n```python\n@retry(wait_random_min=1000, wait_random_max=2000)\ndef wait_1_to_2_seconds():\n    print('Randomly wait 1 to 2 seconds between retries')\n    raise Exception\n```\n\nUse exponential backoff:\n\n```python\n@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)\ndef wait_exponential_1000():\n    print(\n        'Wait 2^i * 1000 milliseconds after ith retry, up to 10 seconds, then 10 seconds afterwards'\n    )\n    raise Exception\n```\n\nDeal with specific exceptions:\n\n```python\ndef retry_if_io_error(exception):\n    return isinstance(exception, IOError)\n\n@retry(retry_on_exception=retry_if_io_error)\ndef might_have_io_error():\n    print('Retry if an IOError occurs, raise any other errors')\n    raise Exception\n\n@retry(retry_on_exception=retry_if_io_error, wrap_exception=True)\ndef might_have_io_error_raise_retry_error():\n    print('Retry if an IOError occurs, raise any other errors wrapped in RetryError')\n    raise Exception\n```\n\nAlter the behavior of retry based on a function return value:\n\n```python\ndef retry_if_result_none(result):\n    return result is None\n\n@retry(retry_on_result=retry_if_result_none)\ndef might_return_none():\n    print('Retry if return value is None')\n    import random\n    if random.randint(0, 10) > 1:\n        return None\n    return 'Done'\n\n# Or retry if result is equal to 1\n@retry(retry_on_result=lambda res: res == 1)\ndef might_return_one():\n    print('Retry if return value is 1')\n    import random\n    if random.randint(0, 10) > 1:\n        return 1\n    return 0\n```\n\nFinally, we can always combine all of the configurations.\n",
    'author': 'JC',
    'author_email': 'jc@jucyai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yaojiach/retrrry',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
