import sys
sys.path.append('..')
import valpy
import time


connector = valpy.henrikdev.HenrikdevConnector()
connector.add_synchronize_target(
    valpy.henrikdev.SynchronizeConfig(
        name='dcmatos', tag='euw'))
connector.add_synchronize_target(
    valpy.henrikdev.SynchronizeConfig(
        name='Beełzzz', tag='EUW'))


try:
    connector.start()
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    connector.stop()
