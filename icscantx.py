#!/usr/bin/python

import ics, sys, getopt, re, string
import random, time, sched, threading

linenm = 0
startime = time.time()
schd = sched.scheduler(time.time, time.sleep)
devices = ics.find_devices()
msg = ics.SpyMessage()
pre_miltm = 0.0

def tx_random_message(chnl=0,msgid=None,tmfm=None):
    global linenm, startime, devices, msg, msgdtstr, msgcyc, pre_miltm
    linenm += 1
    msg.NetworkID = ics.NETID_HSCAN
    txch = msg.NetworkID
    if msgid == None:
        msg.ArbIDOrHeader = random.randint(0,0x7FF)
    else:
        msg.ArbIDOrHeader = msgid

    if msgdtstr != None :
        msgtxstr = re.sub(r'[^0-9a-fA-F]',random.choice(string.hexdigits),msgdtstr)
    else:
        msgtxstr = ''.join(random.choice(string.hexdigits) for i in range(16))

    if len(msgtxstr) > 16:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:8],16),
                 int(msgtxstr[8:10],16), int(msgtxstr[10:12],16), int(msgtxstr[12:14],16), int(msgtxstr[14:16],16) )
    elif len(msgtxstr) > 14:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:8],16),
                 int(msgtxstr[8:10],16), int(msgtxstr[10:12],16), int(msgtxstr[12:14],16), int(msgtxstr[14:],16) )
    elif len(msgtxstr) > 12:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:8],16),
                 int(msgtxstr[8:10],16), int(msgtxstr[10:12],16), int(msgtxstr[12:],16), int('00',16) )
    elif len(msgtxstr) > 10:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:8],16),
                 int(msgtxstr[8:10],16), int(msgtxstr[10:],16), int('00',16), int('00',16) )
    elif len(msgtxstr) > 8:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:8],16),
                 int(msgtxstr[8:],16), int('00',16), int('00',16), int('00',16) )
    elif len(msgtxstr) > 6:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:6],16), int(msgtxstr[6:],16),
                 int('00',16), int('00',16), int('00',16), int('00',16) )
    elif len(msgtxstr) > 4:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:4],16), int(msgtxstr[4:],16), int('00',16),
                 int('00',16), int('00',16), int('00',16), int('00',16) )
    elif len(msgtxstr) > 2:
        msgdt = (int(msgtxstr[:2],16), int(msgtxstr[2:],16), int('00',16), int('00',16),
                 int('00',16), int('00',16), int('00',16), int('00',16) )
    elif len(msgtxstr) > 0:
        msgdt = (int(msgtxstr[0:],16), int('00',16), int('00',16), int('00',16),
                 int('00',16), int('00',16), int('00',16), int('00',16) )
    else:
        msgdt = (random.randint(0,0xFF), random.randint(0,0xFF),
                 random.randint(0,0xFF), random.randint(0,0xFF),
                 random.randint(0,0xFF), random.randint(0,0xFF),
                 random.randint(0,0xFF), random.randint(0,0xFF))
    msg.Data = msgdt

    miltm = time.time() - startime
    rel_miltm = miltm - pre_miltm
    pre_miltm = miltm
    txid = format(msg.ArbIDOrHeader,'#04x').replace('0X','').zfill(3)
    txds = '[{}]'.format(' '.join(format(i, '#04x') for i in msg.Data))
    txds = txds.replace('[','').replace(']','').replace('0x','')

    if re.search('rel',tmfm,re.IGNORECASE):
        print(linenm, format(rel_miltm,'.9f'), txch, 'Tx', txid, txds,flush=True)
    else:
        print(linenm, format(miltm,'.9f'), txch, 'Tx', txid, txds,flush=True)

def tx_cycle_message(chnl,msgid,msgcyc=None,tmfm='absolute'):
    tx_random_message(chnl,msgid,tmfm)
    if msgcyc == None:
        time.sleep(random.random())
    else:
        time.sleep(msgcyc)

def usage():
        print("Technical Support From", flush=True)
        print("     Shanghai VehInfo Technologies Co.,Ltd.", flush=True)
        print("     support@vehinfo.com", flush=True)
        print("Sample Usage:", flush=True)
        print("    icscantx -c 0 -i 0x100 -t 0.1 -d 1122334455667788", flush=True)
        print("         -c [Channel Number]", flush=True)
        print("         -i [Message Identification]", flush=True)
        print("         -d [Message Data Content String]", flush=True)
        print("         -n [Count Number to send]", flush=True)
        print("         -t [Cycle Time by second]", flush=True)
        print("    icscantx -c 0 -i 0x7C0 -t 0.1 -d 02100x1122334455", flush=True)
        print("                                          | ", flush=True)
        print("                                          x for random hex", flush=True)
        print("    icscantx -c 0 -i 0x100 -t 0.1 ", flush=True)
        print("             witout -d fill random hex string", flush=True)
        print("    icscantx -c 0 -i 0x100 ", flush=True)
        print("             witout -d fill random hex string", flush=True)
        print("             witout -t with random time", flush=True)

# start main process
if __name__ == "__main__":
    chnl = 0
    msgid = None
    msgcyc = None
    msgdtstr = None
    tmfm = 'absolute'
    txcnt = 0
    i = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:i:t:d:f:n:",["channel=","id=","cycletime=","datafield=","timeformat=","countnum="])
    except getopt.GetoptError:
        usage()
        exit()
    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit()
        elif opt in ("-c", "--channel"):
            chnl = int(arg)
        elif opt in ("-i","--id"):
            msgid = int(arg,16)
        elif opt in ("-t","--cycletime"):
            msgcyc = float(arg)
        elif opt in ("-d", "--datafield"):
            msgdtstr = str(arg)
            if len(msgdtstr) > 16:
                msgdtstr = msgdtstr[0:16]
        elif opt in ("-f", "--timeformat"):
            tmfm = str(arg)
            if len(tmfm) > 5:
                tmfm = tmfm[0:5]
        elif opt in ("-n", "--countnum"):
            txcnt = int(arg)

    ics.open_device(devices[chnl])
    if re.search('abs',tmfm,re.IGNORECASE):
        print('Count\tSysTime(abs)\tMsgID\tData',flush=True)
    elif re.search('rel',tmfm,re.IGNORECASE):
        print('Count\tSysTime(rel)\tMsgID\tData',flush=True)
    else:
        print('Count\tSysTime(abs)\tMsgID\tData',flush=True)

    while True:
        if txcnt <= 0:
            tx_cycle_message(chnl,msgid,msgcyc,tmfm)
        elif txcnt > i:
            i += 1
            tx_cycle_message(chnl,msgid,msgcyc,tmfm)
        else:
            exit()

