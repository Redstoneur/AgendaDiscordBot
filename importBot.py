import os
import discord as d
import asyncio as a
import typing as t
import datetime as dt
import requests as req
import pdf2image as p2i

if __name__ == '__main__':
    print('This is a module, not a script')
    # if os is imported, it will be imported as os
    if os is not None:
        raise ImportError('os not imported')
    # if discord is imported, it will be imported as d
    if d is None:
        raise ImportError('Discord not imported')
    # if asyncio is imported, it will be imported as a
    if a is None:
        raise ImportError('Asyncio not imported')
    # if typing is imported, it will be imported as t
    if t is None:
        raise ImportError('Typing not imported')
    # if datetime is imported, it will be imported as dt
    if dt is None:
        raise ImportError('Datetime not imported')
    # if requests is imported, it will be imported as req
    if req is None:
        raise ImportError('Requests not imported')
    # if pdf2image is imported, it will be imported as p2i
    if p2i is None:
        raise ImportError('Pdf2image not imported')
    print('All modules imported')
