import sys
import datetime
import json
import logging
import hpfeeds
import socket
import struct
import logstash

HOST = 'hpfriends.honeycloud.net'
PORT = 20000
CHANNELS = ['']
IDENT = ''
SECRET = ''

def main():
	try:
		hpc = hpfeeds.new(HOST, PORT, IDENT, SECRET)
		glastopf_logger = logging.getLogger('python-logstash-logger')
	        glastopf_logger.setLevel(logging.INFO)
        	glastopf_logger.addHandler(logstash.LogstashHandler('127.0.0.1', 8070, version=1))

	except hpfeeds.FeedException, e:
		print >>sys.stderr, 'feed exception:', e
		return 1

	print >>sys.stderr, 'connected to', hpc.brokername


	def on_message(identifier, channel, payload):
  	 glastopf_logger.info(payload)

	def on_error(payload):
		print >>sys.stderr, ' -> errormessage from server: {0}'.format(payload)
		hpc.stop()

	hpc.subscribe(CHANNELS)
	try:
		hpc.run(on_message, on_error)
	except hpfeeds.FeedException, e:
		print >>sys.stderr, 'feed exception:', e
	except KeyboardInterrupt:
		pass
	finally:
		hpc.close()
	return 0

if __name__ == '__main__':
	try: sys.exit(main())
	except KeyboardInterrupt:sys.exit(0)

