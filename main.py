"""
Version 0.1 of the IoT-based Theft Detection system
@author Usiwoma Oghenovo
"""
import sys
import client

def main():
    ip_address = sys.argv[1]
    client.connect(ip_address)

if __name__ == "__main__":
    main()