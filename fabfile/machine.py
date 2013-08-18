import cuisine
from fabric.api import task, roles, run, sudo, cd, local
from fabric.contrib.files import uncomment
from utilities import notify
from conf import MACHINE, KEY
import templates


@task
@roles('web')
def new():
    local('')


@task
@roles('web')
def delete():
    local('')


@task
@roles('web')
def bootstrap():
    notify('Configuring the server.')
    tz_conf()
    locale_conf()
    apt_update()
    apt_upgrade()
    hosts_conf()
    dir_conf()
    package_conf()
    nonmanaged_package_conf()
    python_package_conf()
    profile_conf()
    firewall_conf()
    link_conf()
    reboot()


def apt_update():
    sudo('apt-get update')


def apt_upgrade():
    sudo('apt-get upgrade')


def tz_conf():
    notify('Configuring timezone defaults.')
    sudo('echo "Etc/UTC" > /etc/timezone')
    sudo('dpkg-reconfigure -f noninteractive tzdata')


def locale_conf():
    notify('Configuring locale defaults.')
    sudo('locale-gen --purge en_US.UTF-8')
    sudo('echo -e "LANG=\'en_US.UTF-8\'\nLANGUAGE=\'en_US:en\'\n" > /etc/default/locale')
    sudo('dpkg-reconfigure -f noninteractive locales')


def hosts_conf():
    notify('Writing hostname and hosts files.')
    cuisine.mode_sudo()
    run('echo "{NAME}" > /etc/hostname'.format(NAME=MACHINE['KEY']))
    run('hostname -F /etc/hostname')
    hosts = cuisine.text_template(templates.hosts, MACHINE)
    cuisine.file_append('/etc/hosts', hosts)

    # Want to do an ensure here, the current method is not good for repeated
    # runs.
    #print 'GOING TO GO IN LINES'
    #for l in hosts.splitlines():
    #    print 'LINE:'
    #    print l
    #    text_ensure_line(f, l)
    #file_write('/etc/hosts', f)


def dir_conf():
    notify('Creating the working directory structure.')
    cuisine.mode_sudo()
    cuisine.dir_ensure(MACHINE['DIR_WORKSPACE'])
    cuisine.dir_ensure(MACHINE['DIR_ENVIRONMENTS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=KEY, group=MACHINE['OWNER_GROUP'])
    cuisine.dir_ensure(MACHINE['DIR_PROJECTS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=KEY, group=MACHINE['OWNER_GROUP'])
    cuisine.dir_ensure(MACHINE['DIR_SSL'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=KEY, group=MACHINE['OWNER_GROUP'])
    cuisine.dir_ensure(MACHINE['DIR_LOGS'], recursive=True, mode=MACHINE['DIR_MODE'],
               owner=KEY, group=MACHINE['OWNER_GROUP'])


def package_conf(databases=MACHINE['DATABASES']):
    notify('Installing all required system packages.')
    cuisine.package_ensure('ufw')
    cuisine.package_ensure('supervisor')
    cuisine.package_ensure('python-dev')
    cuisine.package_ensure('python-setuptools')
    cuisine.package_ensure('python-software-properties')
    cuisine.package_ensure('g++')
    cuisine.package_ensure('make')
    cuisine.package_ensure('cmake')
    cuisine.package_ensure('build-essential')
    cuisine.package_ensure('checkinstall')
    cuisine.package_ensure('libxml2-dev')
    cuisine.package_ensure('libjpeg8-dev')
    cuisine.package_ensure('libpng-dev')
    cuisine.package_ensure('zlib1g-dev')
    cuisine.package_ensure('libfreetype6-dev')
    cuisine.package_ensure('liblcms1-dev')
    cuisine.package_ensure('python')
    cuisine.package_ensure('python-pip')
    cuisine.package_ensure('nginx')
    cuisine.package_ensure('git-core')
    cuisine.package_ensure('mercurial')

    if databases:
        if 'postgres' in databases:
            cuisine.package_ensure('postgresql')
            cuisine.package_ensure('postgresql-contrib')
            cuisine.package_ensure('postgresql-server-dev-all')
            # Not working, do manually
            #postgres_conf()

        if 'redis' in databases:
            cuisine.package_ensure('redis-server')


def nonmanaged_package_conf():
    notify('Installing required non-managed packages.')

    notify('Installing PhantomJS')
    cuisine.mode_sudo()
    cuisine.dir_ensure(MACHINE['DIR_USER_HOME'])
    with cd(MACHINE['DIR_USER_HOME']):
        sudo('wget -N https://phantomjs.googlecode.com/files/phantomjs-1.9.1-linux-x86_64.tar.bz2')
        sudo('tar xzvf phantomjs-1.9.1-linux-x86_64.tar.bz2')
        with cd('phantomjs-1.9.1-linux-x86_64'):
            cuisine.file_link(
                MACHINE['DIR_USER_HOME'] + 'phantomjs-1.9.1-linux-x86_64/bin/phantomjs',
                '/usr/local/bin/phantomjs', symbolic=True)

    notify('Installing CasperJS')
    cuisine.mode_sudo()
    cuisine.dir_ensure(MACHINE['DIR_USER_HOME'])
    with cd(MACHINE['DIR_USER_HOME']):
        sudo('wget -N https://github.com/n1k0/casperjs/tarball/1.0.3')
        sudo('tar xzvf n1k0-casperjs-1.0.3-0-g76fc831.tar.gz')
        with cd('n1k0-casperjs-1.0.3-0-g76fc831'):
            cuisine.file_link(
                MACHINE['DIR_USER_HOME'] + 'n1k0-casperjs-1.0.3-0-g76fc831.tar.gz/bin/casperjs',
                '/usr/local/bin/casperjs', symbolic=True)


def python_package_conf():
    notify('Installing required system python packages.')
    cuisine.mode_sudo()
    cuisine.python_package_ensure('virtualenv')
    cuisine.python_package_ensure('virtualenvwrapper')


def postgres_conf():
    uncomment('/etc/postgresql/9.1/main/postgresql.conf', 'listen_addresses',
              use_sudo=True, char='#', backup='.bak')
    sudo('passwd postgres')
    with sudo('su - postgres'):
        run('psql')
        run('CREATE EXTENSION adminpack;')
        #
        # get out of postgresq shell here
        #
        run('createuser ' + KEY)
        run('exit')
        run('createdb ' + KEY)


@task
@roles('web')
def profile_conf():
    notify('Configuring .profile settings.')
    profile = cuisine.text_template(templates.profile, MACHINE)
    cuisine.file_append(MACHINE['OWNER_PROFILE'], profile)
    run('source ' + MACHINE['OWNER_PROFILE'])


def firewall_conf():
    sudo('ufw default deny')
    sudo('ufw allow 80')
    sudo('ufw allow 443')
    sudo('ufw allow 587')
    sudo('ufw enable')


def link_conf():
    notify('Configuring necessary symlinks for our libraries.')
    cuisine.mode_sudo()
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libjpeg.so', '/usr/lib/libjpeg.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libpng.so', '/usr/lib/libpng.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libz.so', '/usr/lib/libz.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/libfreetype.so', '/usr/lib/libfreetype.so', symbolic=True)
    cuisine.file_link('/usr/lib/x86_64-linux-gnu/liblcms.so', '/usr/lib/liblcms.so', symbolic=True)


def reboot():
    sudo('reboot')
