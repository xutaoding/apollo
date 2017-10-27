# -*- coding: utf-8 -*-

import six
import hashlib

import subprocess
from os.path import abspath, dirname
from os.path import join as join_path


def gen_md5(s):
    m = hashlib.md5()
    m.update(to_bytes(s))
    return m.hexdigest()


def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of `text`. If `text`
        is already a bytes object, return it as-is."""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)


def obtain_css_selector(html):
    pass


def obtain_xpath():
    pass


def execute_cmd_to_file(command, stdout=None, stderr=None, path=None):
    if path is None:
        path = dirname(dirname(abspath(__file__)))

    stdout_fn = join_path(path, stdout or 'stdout.txt')
    stderr_fn = join_path(path, stderr or 'stderr.txt')
    fd_out, fd_err = open(stdout_fn, 'a'), open(stderr_fn, 'a')

    try:
        child = subprocess.Popen(command, shell=True, stdout=fd_out, stderr=fd_err)
        child.wait()  # program will continue until wait for sub process finished
    except Exception as err:
        fd_err.write('execute subprocess error:' + str(err) + '\n')
    finally:
        fd_out.close()
        fd_err.close()

