#!/usr/bin/env python
import os

def main():
    msg = os.environ['MESSAGE']
    web_server = os.environ['WEB_SERVER']

    print("mesg: ", msg)
    print("server: ", web_server)

if __name__ == '__main__':
    main()
