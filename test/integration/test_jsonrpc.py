import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sucrd import SucrDaemon
from sucr_config import SucrConfig


def test_sucrd():
    config_text = SucrConfig.slurp_config_file(config.sucr_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000046cb013dfeaa9d545f64beef4a069c2f588d3c6bf7101dbb296976580b9'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000020bd6b39b55154ff396d35e5216726198fb456f31c765a223d47b8bda3e'

    creds = SucrConfig.get_rpc_creds(config_text, network)
    sucrd = SucrDaemon(**creds)
    assert sucrd.rpc_command is not None

    assert hasattr(sucrd, 'rpc_connection')

    # Sucr testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = sucrd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sucrd.rpc_command('getblockhash', 0) == genesis_hash
