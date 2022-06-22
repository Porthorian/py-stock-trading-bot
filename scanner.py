#!/usr/bin/python3

import logging

def initializeLogger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='scanner.log',
        filemode='a'
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger().addHandler(console)

initializeLogger()

import tradingbot
import json

def main():
    file = open('keys.json')
    attributes = json.load(file)
    file.close()

    scanner = tradingbot.scanner.Scanner(attributes['ApiKey'], attributes['ApiSecret'], attributes['BaseURL'])
    scanner.get_potentials()

if __name__ == "__main__":
    main()
