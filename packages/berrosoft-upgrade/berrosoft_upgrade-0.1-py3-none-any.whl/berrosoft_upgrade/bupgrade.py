#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Auteur: manuel BERROCAL
# <manu.berrocal@absolacom.com>
# Date: 23/07/2022
# Description : Manage updates for berrosoft softwares
# Options : no options
#
#  berrosoft_upgrade.py
#
#  Copyright 2022 manuel BERROCAL <manu.berrocal@absolacom.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
import sys
import shutil
import urllib.request
import configparser
import tempfile
from zipfile import ZipFile
import tarfile


class MyColors:
    """
    Definition of colors used in printed messages (usefull for debug)
    """
    RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, NORMAL = ("[1;31m",
                                                              "[1;32m",
                                                              "[1;33m",
                                                              "[1;34m",
                                                              "[1;35m",
                                                              "[1;36m",
                                                              "[1;37m",
                                                              "[0;39m")


COL = MyColors()


def download_update(config, verbose=False):

    url = config['update']['download']
    try:
        with urllib.request.urlopen(url) as response:
            if verbose:
                print("Downloading %s" % url)
            # with tempfile.TemporaryDirectory() as sys.tmp_dir:
            #     shutil.copyfileobj(response, "%s/%s" % (sys.tmp_dir, filename))
            filename = url.split('/')[-1]
            sys.tmp_dir = tempfile.mkdtemp(prefix="berrosoftupgrade_")
            with urllib.request.urlopen(url) as response, open("%s/%s" % (sys.tmp_dir, filename), 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

    except urllib.error.URLError as e:
        if verbose:
            print("%sError collecting update file at %s%s: %s" % (COL.RED, url, COL.NORMAL, e.reason))
        return None

    return out_file


def apply_update(config, update_file, verbose=False):
    """
    Apply update from file
    """
    if update_file is None:
        return
    else:
        if verbose:
            print(update_file.name)
        if config['update']['mode'] == 'alone':
            shutil.move(update_file.name, 'toto.zip')
        else:
            os.chdir(sys.tmp_dir)

            if ".zip" == update_file.name[-4:]:
                print("--fichier zip--")
                with ZipFile(update_file.name, 'r') as zipObj:
                    # Extract all the contents of zip file in current directory
                    zipObj.extractall()
            elif ".tar" == update_file.name[-4:] or ".tar.gz" == update_file.name[-7:]:
                print("--fichier tar--")
                mytar = tarfile.open(update_file.name)
                mytar.extractall()
                mytar.close()

            # execute setup command
            setupfile = "%s/%s" % (sys.tmp_dir, config['setup']['setup'].replace('"', '').replace("'", ""))
            print(setupfile)
            if os.path.isfile(setupfile):
                os.system(setupfile)
            else:
                raise FileNotFoundError("%sSetup file %s%s%s not found! Please report it to software developer%s" % (COL.RED, COL.YELLOW, setupfile, COL.RED, COL.NORMAL))


def check_update(version, config=None, url=None, verbose=False):
    """
    Dowload update file
    """
    if config is None:
        config = get_update_infos(url, version, verbose)
    if config is None:
        return False

    if str(version).strip() != config['general']['version'].strip():
        if verbose:
            print("%supdate required%s (%s => %s)" % (COL.MAGENTA, COL.NORMAL, version, config['general']['version'].strip()))
            return True
    else:
        if verbose:
            print("%sUp to date%s" % (COL.GREEN, COL.NORMAL))
        return False


def get_update_infos(url, version=0, verbose=False):

    try:
        with urllib.request.urlopen("%s/update.txt" % url) as response:
            datas = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if verbose:
            print("%sError collecting update file at %s%s: %s" % (COL.RED, url, COL.NORMAL, e.reason))
        return None

    # Convert data file to dict
    config = configparser.RawConfigParser()
    config.read_string(datas)
    return config


def update(url="", version="0", verbose=False, clean=True):
    config = get_update_infos(url, version, verbose=True)
    if config is not None:
        if check_update(version, config, url, verbose):
            update_file = download_update(config, verbose)
            apply_update(config, update_file, verbose)

            # os.system('ls -ailh %s' % sys.tmp_dir)
            # do clean, remove temporary directory
            if clean:
                shutil.rmtree(sys.tmp_dir)


def main(url="", version="0", verbose=False):
    # ONLY FOR TEST. NOT REAL VALUE
    url = "http://dldivers.absolacom.com/backup"
    version = "2.0.1"
    verbose = True
    update(url, version, verbose, False)

    return 0


if __name__ == '__main__':
    sys.version = "0.1"
    from optparse import OptionParser
    USAGE_ = "see %prog --help for help \nDescription du logiciel"
    PARSER = OptionParser(usage=USAGE_, version=sys.version)
    # PARSER.add_option("-f", "--file", dest="configfile", default="/etc/program.conf",
    #                   help="Configuration file to use",
    #                   metavar="CONFIGFILE")

    PARSER.add_option("-v", "--verbose", default=False, action="store_true",
                      dest="verbose",
                      help=u"Rend le programme bavard")

    (OPTIONS, ARGS) = PARSER.parse_args()

    # if OPTIONS.configfile == "" or OPTIONS.configfile == None:
    #     OPTIONS.configfile = ""
    main(OPTIONS.verbose)
