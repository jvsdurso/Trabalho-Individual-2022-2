import re
import requests

lib_name = 'trabalho-individual-2022-2-jvsdurso'

response = requests.get(f'https://pypi.org/pypi/{lib_name}/json')
if response.status_code != 200:
    raise Exception('Error while getting the version')

last_version = response.json()['info']['version']

new_version = last_version.split('.')
new_version[-1] = str(int(new_version[-1]) + 1)
new_version = '.'.join(new_version)

try:
    with open('pyproject.toml', 'r') as f:
        pyproject = f.read()
    pyproject = re.sub(r'version = "(.*)"', f'version = "{new_version}"', pyproject)
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject)
    print(f'New version {new_version} saved on pyproject.toml')
except Exception as e:
    print(f'Error: {e}')
