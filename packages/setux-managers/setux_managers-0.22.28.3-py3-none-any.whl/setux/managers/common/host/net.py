from pybrary.func import memo

from setux.core.manage import Manager
from setux.logger import logger


class Distro(Manager):
    '''Net Infos
    '''
    manager = 'net'

    @memo
    def addr(self):
        self.target.pip.install('pybrary', verbose=False)
        ret, out, err = self.run('pybrary get_ip_adr')
        if ret == 0:
            return out[0]
        else:
            error = '\n'.join(err)
            logger.debug(f'\n\n ! host.net.addr ERROR !\n\n{error}\n')

