import begin
import twill.commands as tc
import salt.config
import salt.client
import logging


def salt_init():
    opts = salt.config.apply_minion_config()
    opts['file_client'] = 'local'
    caller = salt.client.Caller(mopts=opts)
    return caller

@begin.logging
def install_redhat(key):
    caller = salt_init()
    info = dict(
        newrelic_url='http://download.newrelic.com/pub/newrelic/el5/i386/newrelic-repo-5-3.noarch.rpm',
        newrelic_package='newrelic-sysmond',
        newrelic_license_cmd=r"nrsysmond-config --set license_key='%(l_key)s'"
        % {'l_key': key},
        newrelic_start_cmd=r"/etc/init.d/newrelic-sysmond restart",
        newrelic_chkconfig_cmd='chkconfig newrelic-sysmond on')
    logging.info(caller.sminion.functions['pkg.install'](sources=[
        {'repo': info['newrelic_url']}
    ]))
    logging.info(caller.sminion.functions['pkg.install'](
        info['newrelic_package'],
        require=[{'pkg': info['newrelic_url']}]))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_license_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_start_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_chkconfig_cmd'])
    )

def install_debian(key):
    caller = salt_init()
    info = dict(
        apt_repo_cmd = 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list',
        repo_trust_cmd = 'wget -O- https://download.newrelic.com/548C16BF.gpg | apt-key add -',
        apt_update_cmd = 'apt-get update',
        newrelic_package='newrelic-sysmond',
        newrelic_license_cmd=r"nrsysmond-config --set license_key='%(l_key)s'"
        % {'l_key': key},
        newrelic_start_cmd=r"/etc/init.d/newrelic-sysmond restart",
        newrelic_chkconfig_cmd='chkconfig newrelic-sysmond on'
    )
    logging.info(
        caller.sminion.functions['cmd.run'](info['apt_repo_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['repo_trust_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['apt_update_cmd']))
    logging.info(caller.sminion.functions['pkg.install'](
        info['newrelic_package'],
        require=[{'cmd': info['apt_update_cmd']}]))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_license_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_start_cmd']))
    logging.info(
        caller.sminion.functions['cmd.run'](info['newrelic_chkconfig_cmd'])
    )

def install_linux(key):
    caller = salt_init()
    tc.go('http://download.newrelic.com/server_monitor/release/')
    tc.follow('.*-linux.tar.gz')
    info = dict(
        newrelic_url = tc.browser.get_url()
    )
    caller.sminion.functions['cp.get_url'](dest='/usr/local/src/newrelic.tgz', path=info['newrelic_url'])
    caller.sminion.functions['archive.tar'](options='xf', tarfile='/usr/local/src/newrelic.tgz', dest='/usr/local/src/newrelic_src')
    caller.sminion.functions['flie.directory_exists']('/etc/newrelic')
    caller.sminion.functions['flie.copy'](src='/usr/local/src/newrelic_src/daemon/nrsysmond.x64', dst='/usr/local/bin/nrsysmond')
    caller.sminion.functions['flie.copy'](src='/usr/local/src/newrelic_src/scripts/nrsysmond-config', dst='/usr/local/bin')
    caller.sminion.functions['flie.copy'](src='/usr/local/src/newrelic_src/nrsysmond.cfg', dst='/etc/newrelic/nrsysmond.cfg')
    caller.sminion.functions['cmd.run']('/usr/local/bin/nrsysmond -c /etc/newrelic/nrsysmond.cfg')
    
