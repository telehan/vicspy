#!/usr/bin/python
import ics, sys
import getopt, re

linenm = 0
ics.CanSettings(SetBoudrate = 1)
ics.CanSettings(Baud_rate = 500000)
devices = ics.find_devices()
device = devices[0]
pre_rxtm = 0
shift_rxtm = 0
rel_rxtm = 0

def dump_can_chnl(chnl=0,tmformat=1):
    global linenm, devices, pre_rxtm, shift_rxtm
    while True:
        messages, errors = ics.get_messages(device)
        for rxmsg in messages:
            linenm += 1
            msgst = rxmsg.StatusBitField
            msgdir = 'Rx'
            if hex(msgst) == '0x4000000':
                msgdir = 'Rx'
            elif hex(msgst) == '0x4000002':
                msgdir = 'Tx'
            else:
                msgdir = 'Er'
            rxtm = rxmsg.TimeHardware/40000000
            rxtm = shift_rxtm + rxtm
            if rxtm < pre_rxtm:
                delta = rxtm - shift_rxtm
                shift_rxtm += 107.3741824
                rxtm = shift_rxtm + delta
            rel_rxtm = rxtm - pre_rxtm
            pre_rxtm = rxtm
            rxid = format(rxmsg.ArbIDOrHeader,'#04X',).replace('0X','').zfill(3)
            rxds = '[{}]'.format(' '.join(format(i, '#04X').replace('0X','') for i in rxmsg.Data))
            rxds = rxds.replace('[','').replace(']','')
            rxch = rxmsg.NetworkID
            rxdl = rxmsg.NumberBytesData
            rxtm = format(rxtm,'.6f')
            rel_rxtm = format(rel_rxtm,'.6f')
            if tmformat == 1 :
                print(rxtm, rxch, rxid, msgdir, 'd', rxdl, rxds, flush=True)
            else:
                print(rel_rxtm, rxch, rxid, msgdir, 'd', rxdl, rxds, flush=True)
        messages = []

def usage():
        print("Technical Support From", flush=True)
        print("     Shanghai VehInfo Technologies Co.,Ltd.", flush=True)
        print("     support@vehinfo.com", flush=True)
        print("Sample Usage:", flush=True)
        print("    icscandump -c 0 -f [abs|rel]", flush=True)
        print("     -c [Channel Number]", flush=True)
        print("     -f [TimeFormat, rel|abs]", flush=True)

if __name__ == "__main__":
    chnl = 0
    tmfm = 'absolute'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:f:",["channel=","timeformat="])
    except getopt.GetoptError:
        usage()
        exit()
    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit()
        elif opt in ("-c", "--channel"):
            chnl = int(arg)
        elif opt in ("-f", "--timeformat"):
            tmfm = str(arg)
            if len(tmfm) > 5:
                tmfm = tmfm[0:5]

    device = devices[chnl]
    ics.open_device(device)
    if re.search('abs',tmfm,re.IGNORECASE):
        print('Time(abs)\tCAN\tID\tDir\tType\tDLC\tData',flush=True)
        dump_can_chnl(chnl,1)
    elif re.search('rel',tmfm,re.IGNORECASE):
        print('Time(rel)\tCAN\tID\tDir\tType\tDLC\tData',flush=True)
        dump_can_chnl(chnl,0)
    else:
        print('Time(abs)\tCAN\tID\tDir\tType\tDLC\tData',flush=True)
        dump_can_chnl(chnl,1)

