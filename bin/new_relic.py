#!/usr/bin/env python
import begin
import sys
import logging
import salt.config
import salt.client
from newrelic_ops import newrelic as newrelic


@begin.start(auto_convert=True)
@begin.logging
def main(install=False, key=''):
    if not install:
        logging.error('Try -h/--help option for usage info!')
        sys.exit(1)
    else:
        if not key:
            logging.error('Please provide newrelic license key via --key option')
            sys.exit(1)
        caller = newrelic.salt_init()
        if 'redhat' in caller.sminion.functions['grains.get']('os_family').lower():
            newrelic.install_redhat(key)
        if 'debian' in caller.sminion.functions['grains.get']('os_family').lower():
            newrelic.install_debian(key)
        else:
            newrelic.install_linux(key)
