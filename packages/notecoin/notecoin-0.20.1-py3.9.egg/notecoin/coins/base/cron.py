import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from ccxt import okex
from notecoin.coins.base.file import DataFileProperty

path_root = '/home/bingtao/workspace/tmp'

file_pro = DataFileProperty(exchange=okex(), freq='weekly', path=path_root, timeframe='1m')

file_pro.load()
#nohup /home/bingtao/opt/anaconda3/bin/python /home/bingtao/workspace/notechats/notecoin/notecoin/coins/base/cron.py >>/notechats/notecoin/logs/notecoin-$(date +%Y-%m-%d).log 2>&1 &
