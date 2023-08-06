import asyncio
import getopt
import json
import sys
import socket

TRV = {}

sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
UDP_IP = socket.gethostbyname(socket.getfqdn())  

DEFAULT_PROXY_IP = UDP_IP
DEFAULT_PROXY_PORT = 6000
LW_PORT = 6000

light=[]


class TrvCollector:
    """UDP proxy to collect Lightwave traffic."""

    def __init__(self, verbose):
        """Initialise Collector entity."""
        self.transport = None
        self.verbose = verbose

    def connection_made(self, transport):
        """Start the proxy."""
        self.transport = transport

    # pylint: disable=W0613, R0201
    def datagram_received(self, data, addr):
        """Manage receipt of a UDP packet from Lightwave."""

        #print(self.add_space(self.convert_hex(data)))
        self.store_data(self.convert_hex(data))


    def add_space(self,a):
        # split address to 6 character
        pac=' '.join([a[i:i+2] for i in range(0, len(a), 2)])
        # format to 00:00:00:00:00:00
        return pac

    def convert_hex(self, data):
        res = ""
        for b in data:
            res += "%02x" % b
        return res
    def enquiry(self,list1): 

        return not list1

    def store_data(self, data):

        if(str(data[42:46])=="0034"):
            print("your packet is right 0034",self.add_space(data))
        elif(str(data[42:46])=="0032"):
            print("your packet is right 0032 ",self.add_space(data))
            status_data=data[34:-1]
            print(status_data)
            subnet_id=status_data[0:2]
            device_id=status_data[2:4]
            channel_id=status_data[16:18]
            concat=status_data[0:2]+status_data[2:4]+status_data[16:18]
            level=status_data[20:22]

            if self.enquiry(light): 
                print("The list is Empty") 
                light.append({"level":level,"device_id":concat})
                print(light)
            else: 
                 print("The list isn't empty")
                 for value in light:
                    if(concat==value["device_id"]):
                        value["level"]=level
                        print(light)
                        return 


                
class TrvResponder:
    """UDP Listner, for connections from HomeAssistant."""

    def __init__(self, verbose):
        """Initialise Responder entity."""
        self.transport = None
        self.verbose = verbose

    def connection_made(self, transport):
        """Start the listner."""
        self.transport = transport

    def datagram_received(self, data, addr):
        """Respond to query from HomeAssistant."""
        message = data.decode()
        if self.verbose:
            print(message)
        if message in TRV.keys():
            reply = TRV[message]
        else:
            reply = '{"error":"trv ' + message + ' not found"}'
            if self.verbose:
                print("Not found")
        self.transport.sendto(reply.encode("UTF-8"), addr)


def proxy(proxy_ip, port, verbose):
    """Run the LW Proxy."""
    loop = asyncio.get_event_loop()

    if verbose:
        print(f"Starting UDP servers: {proxy_ip}:{port} & 0.0.0.0:{LW_PORT}")

    # One protocol instance will be created to serve all client requests
    collect = loop.create_datagram_endpoint(
        lambda: TrvCollector(verbose), local_addr=("0.0.0.0", LW_PORT)
    )
    collect_transport, dummy = loop.run_until_complete(collect)

    respond = loop.create_datagram_endpoint(
        lambda: TrvResponder(verbose), local_addr=(proxy_ip, port)
    )
    respond_transport, dummy = loop.run_until_complete(respond)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    collect_transport.close()
    respond_transport.close()

    loop.close()


def main(argv=None):
    """Start the proxy."""
    if argv is None:
        argv = sys.argv[1:]

    proxy_ip = DEFAULT_PROXY_IP
    proxy_port = DEFAULT_PROXY_PORT
    verbose = False

    print("success ")
    proxy(proxy_ip, proxy_port, verbose)


if __name__ == "__main__":
    main()