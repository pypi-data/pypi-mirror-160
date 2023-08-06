# coding: utf-8
import os
import sunday.core.paths as paths
from configparser import ConfigParser

__all__ = ['getConfig']

defaultConfig = {
    'LOGGING.level': 'ERROR',
    'LOGIN.cookieFile': '.cookies',
    'LOGIN.envFile': '.env',
    # 密钥
    'CRYPTO.key': 'HOWDUUDU'
}

def getConfig(name, file='config.ini', default={}):
    '''返回能获取全局配置文件值的函数'''
    configPwd = os.path.join(paths.rootCwd, file)
    cfg = ConfigParser()
    cfg.read(configPwd, encoding='utf-8')
    def getval(key):
        if cfg.has_option(name, key):
            return cfg.get(name, key)
        return default.get(key) or defaultConfig.get('.'.join([name, key]))
    return getval

if __name__ == "__main__":
    print(getConfig('CRYPTO')('key'))
