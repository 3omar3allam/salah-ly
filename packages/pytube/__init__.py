# -*- coding: utf-8 -*-
# flake8: noqa
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = 'pytube'
__version__ = '9.4.0'
__author__ = 'Nick Ficano'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 Nick Ficano'

from packages.pytube.logging import create_logger
from packages.pytube.query import CaptionQuery
from packages.pytube.query import StreamQuery
from packages.pytube.streams import Stream
from packages.pytube.captions import Caption
from packages.pytube.contrib.playlist import Playlist
from packages.pytube.__main__ import YouTube

logger = create_logger()
logger.info('%s v%s', __title__, __version__)
