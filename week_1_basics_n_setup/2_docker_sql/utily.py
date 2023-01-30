import logging as log
import os
import sys
import traceback

from bash import bash

# logi = log.info
logi = print

logi(f"{sys.executable=}", bash(f"python -V\npwd"), sep='\t')


def handle_exc(skip_errors=False): traceback.print_exc() if skip_errors else raise_()


def check_file_size(file_path, *, skip_err=False):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) == 0:
            return 0  # "File exists but is empty."
        else:
            return os.path.getsize(file_path)  # "File exists and is not empty."
    else:
        return None if skip_err else raise_(
            FileExistsError(f"File <{file_path}> does not exist."))


def fprint(csv_name):
    with open(csv_name, 'r') as f:
        print(f"Bad data in file?.. <{csv_name}> content:\n",
              '<empty>' if not len(f.read()) else
              # ('\n'.join(f.readlines(111)[:2]) + '\n...')
              ('\n'.join(f.readlines(111)[:2]) + '\n...')

              )


def fread(fname, i=-1):
    with open(fname, 'r') as r: return r.read(i) + ('...' if i > 0 else '')


def flines(fname, i=-1):
    # return len(fread(fname).splitlines())
    with open(fname, 'rb') as f:
        return (f.readlines(i)
                # + [('...' if i > 0 else ''), ]
                )


def flines_count(fname):
    return len(flines(fname))


def raise_(exc: Exception = None, *a, **k):
    if exc:
        raise (
            exc(*a, **k) if a and k else
            exc(*a) if not k else
            exc(**k) if not a
            else exc()
        )
    else:
        raise


def test1():
    fname = 'green_tripdata_2019-01.csv'
    print(f"{fname=}")
    print(f"{flines_count(fname)=}")
    print(f"{fread(fname, 222)=}")
    # fprint(fname)


if __name__ == '__main__': print(f"""# some test:..
    {test1()=}
""")
