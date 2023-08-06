# pytmpfile

Extremely simple helper for [memory-tempfile](https://github.com/mbello/memory-tempfile). Intended to use in non-Python programs requiring files (e.g., GCC).

Usage:
```
from pytmpfile import get_tmp_path
import os


if __name__ == '__main__':
    with get_tmp_path(content='print("hello")\n', suffix='.py') as tmp_path:
        print(f'{tmp_path} exists inside context manager: {os.path.exists(tmp_path)}')
        print('And it has this content:')
        with open(tmp_path, 'r') as f:
            print(f.read())
    print(f'{tmp_path} exists outside context manager: {os.path.exists(tmp_path)}')

```

Output:

```
/run/user/1000/tmpemeg9rhm.py exists inside context manager: True
And it has this content:
print("hello")

/run/user/1000/tmpemeg9rhm.py exists outside context manager: False
```

