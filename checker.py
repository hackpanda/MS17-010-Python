from mysmb import MYSMB
from impacket import smb, smbconnection, nt_errors
from impacket.uuid import uuidtup_to_bin
from impacket.dcerpc.v5.rpcrt import DCERPCException
from struct import pack
import sys
import argparse
import logger
from netaddr import *
'''
Script for:
- checking if target has MS17-010 patch or not.
- find accessible named pipe

Logic written by @sleepya_

User friendliness by @mez0cc
'''

parser = argparse.ArgumentParser(description='MS17-010 Checker script',epilog="Example: python checker.py -t 192.168.0.1")
parser.add_argument("-u", "--user", type=str, metavar="",help="Username to authenticate with")
parser.add_argument("-p", "--password", type=str, metavar="",help="Password for specified user")
parser.add_argument("-t", "--target", type=str, metavar="", help="Specify a host or a subnet")
parser.add_argument("-f", "--file", type=str, metavar="", help="Specify a list of subnets or hosts from a file")
parser.add_argument('--version', action='version', version='%(prog)s 0.2')
args = parser.parse_args()


if args.user:
	USERNAME = args.user
else:
	USERNAME = ''

if args.user:
	PASSWORD = args.password
else:
	PASSWORD = ''

target = args.target
NDR64Syntax = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

MSRPC_UUID_BROWSER  = uuidtup_to_bin(('6BFFD098-A112-3610-9833-012892020162','0.0'))
MSRPC_UUID_SPOOLSS  = uuidtup_to_bin(('12345678-1234-ABCD-EF00-0123456789AB','1.0'))
MSRPC_UUID_NETLOGON = uuidtup_to_bin(('12345678-1234-ABCD-EF00-01234567CFFB','1.0'))
MSRPC_UUID_LSARPC   = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AB','0.0'))
MSRPC_UUID_SAMR     = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AC','1.0'))

pipes = {
	'browser'  : MSRPC_UUID_BROWSER,
	'spoolss'  : MSRPC_UUID_SPOOLSS,
	'netlogon' : MSRPC_UUID_NETLOGON,
	'lsarpc'   : MSRPC_UUID_LSARPC,
	'samr'     : MSRPC_UUID_SAMR,
}

def checker(host):
	try:
		conn = MYSMB(host)
		try:
			conn.login(USERNAME, PASSWORD)
		except smb.SessionError as e:
			logger.error('LOGIN FAILED: ' + nt_errors.ERROR_MESSAGES[e.error_code][0])
			sys.exit()
		finally:
			logger.info('CONNECTED TO {}'.format(logger.BLUE(host)))
			logger.info('TARGET OS: ' + conn.get_server_os())

		tid = conn.tree_connect_andx('\\\\'+target+'\\'+'IPC$')
		conn.set_default_tid(tid)

		# test if target is vulnerable
		TRANS_PEEK_NMPIPE = 0x23
		recvPkt = conn.send_trans(pack('<H', TRANS_PEEK_NMPIPE), maxParameterCount=0xffff, maxDataCount=0x800)
		status = recvPkt.getNTStatus()
		if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
			logger.success('{} IS NOT PATCHED!'.format(target))
		else:
			logger.error('{} IS PATCHED!'.format(target))
			sys.exit()


		logger.action('CHECKING NAMED PIPES...')
		for pipe_name, pipe_uuid in pipes.items():
			try:
				dce = conn.get_dce_rpc(pipe_name)
				dce.connect()
				try:
					dce.bind(pipe_uuid, transfer_syntax=NDR64Syntax)
					logger.success('{}: OK (64 bit)'.format(pipe_name))
				except DCERPCException as e:
					if 'transfer_syntaxes_not_supported' in str(e):
						logger.success('{}: OK (32 bit)'.format(pipe_name))
					else:
						logger.success('{}: OK ({})'.format(pipe_name, str(e)))
				dce.disconnect()
			except smb.SessionError as e:
				logger.error('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error_code][0]))
			except smbconnection.SessionError as e:
				logger.error('{}: {}'.format(pipe_name, nt_errors.ERROR_MESSAGES[e.error][0]))


		conn.disconnect_tree(tid)
		conn.logoff()
		conn.get_socket().close()
	except:
		logger.error('COULD NOT CONNECT TO {}'.format(logger.RED(host)))

def check_subnet(addr):
	sub_range = IPNetwork(addr)
	for i in sub_range:
		checker(str(i))

# def fromFile(file):
# 	hosts_file = open(file,"r")
# 	for line in hosts_file:
# 		if "/" in line:
# 			check_subnet(line)
# 		elif "/" not in line:
# 			sub_range = IPNetwork(line)
# 			for i in sub_range:
# 				checker(str(i))

if args.target:
	if "/" in args.target:
		check_subnet(target)

	elif "/" not in args.target:
		checker(target)

elif args.file:	
	logger.error('This option is currently broken. See GitHub for more information.')
	# fromFile(args.file)

else:
	logger.error('No host specified. Use either -f or -t for hosts.\n')
	parser.print_help()
