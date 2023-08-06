# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.staticfiles.management.commands.runserver import Command as DefaultRunserver
from importlib.util import find_spec
has_channels = find_spec('channels') is not None
if has_channels:
    from channels.management.commands.runserver import Command as ASGIRunserver

from lino.api import dd

if dd.is_installed('notify') and dd.plugins.notify.use_websockets and has_channels:
    class Command(ASGIRunserver):
        pass
else:
    class Command(DefaultRunserver):
        pass
