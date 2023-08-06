#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time

import urequests as requests


class Sonos():

    def __init__(self, ip):
        self.ip = ip
        self.host = f'http://{ip}:1400'

    def pause(self):
        sonosAction(self.ip, self.host, '/MediaRenderer/AVTransport/Control',
                    'AVTransport:1', 'Pause', '<InstanceID>0</InstanceID>')

    def stop(self):
        sonosAction(self.ip, self.host, '/MediaRenderer/AVTransport/Control',
                    'AVTransport:1', 'Stop', '<InstanceID>0</InstanceID>')

    def play(self, speed: int = 1):
        sonosAction(self.ip, self.host, '/MediaRenderer/AVTransport/Control',
                    'AVTransport:1', 'Play',
                    f'<InstanceID>0</InstanceID><Speed>{speed}</Speed>')

    def next(self):
        sonosAction(self.ip, self.host, '/MediaRenderer/AVTransport/Control',
                    'AVTransport:1', 'Next', '<InstanceID>0</InstanceID>')

    def setVolume(self, volume: int):
        sonosAction(
            self.ip, self.host, '/MediaRenderer/RenderingControl/Control',
            'RenderingControl:1', 'SetVolume',
            f'<InstanceID>0</InstanceID><Channel>Master</Channel><DesiredVolume>{volume}</DesiredVolume>'
        )

    def setRelativeVolume(self, delta: int):
        sonosAction(
            self.ip, self.host, '/MediaRenderer/RenderingControl/Control',
            'RenderingControl:1', 'SetRelativeVolume',
            f'<InstanceID>0</InstanceID><Channel>Master</Channel><Adjustment>{delta}</Adjustment>'
        )

    def setLEDState(self, mode: int):
        sonosAction(
            self.ip, self.host, '/DeviceProperties/Control',
            'DeviceProperties:1', 'SetLEDState',
            f'<DesiredLEDState>{ "On" if mode else "Off" }</DesiredLEDState>')

    def getZoneName(self):
        resp = sonosAction(self.ip, self.host, '/DeviceProperties/Control',
                           'GroupRenderingControl:1', 'GetZoneAttributes', '')
        return getXMLTagValue(resp, 'CurrentZoneName')

    @property
    def playbackState(self) -> str:
        resp = sonosAction(self.ip, self.host,
                           '/MediaRenderer/AVTransport/Control',
                           'AVTransport:1', 'GetTransportInfo',
                           '<InstanceID>0</InstanceID>')
        return getXMLTagValue(resp, 'CurrentTransportState')

    def playpause(self):
        s = self.playbackState
        if s == 'PLAYING':
            self.pause()
        elif s == 'PAUSED_PLAYBACK' or s == 'STOPPED':
            self.play()

    def blink(self):
        for i in range(3):
            self.setLEDState(1)
            time.sleep(0.1)
            self.setLEDState(0)


def sonosAction(ip, host, url, service, action, arguments):
    headers = {
        'Host': ip + ':1400',
        'Soapaction': f'urn:schemas-upnp-org:service:{service}#{action}',
        'Content-Type': 'text/xml; charset="utf-8"',
    }
    data = f'''<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <u:{action} xmlns:u="urn:schemas-upnp-org:service:{service}">
                    {arguments}
                </u:{action}>
            </s:Body>
        </s:Envelope>'''
    resp = requests.post(
        host + url,
        headers=headers,
        data=data,
    )
    return resp.text


def getXMLTagValue(xml: str, tag: str) -> str:
    if not tag.endswith('>'):
        tag += '>'
    startindex = xml.find(tag) + len(tag)
    endindex = xml.find(f'</{tag}')
    if not startindex or not endindex:
        return None

    return xml[startindex:endindex]


def isGroupCoordinator(ip: str) -> bool:
    resp = sonosAction(ip, f'http://{ip}:1400',
                       '/MediaRenderer/GroupRenderingControl/Control',
                       'GroupRenderingControl:1', 'GetGroupMute',
                       '<InstanceID>0</InstanceID>')
    if getXMLTagValue(resp, 'errorCode') == "701":
        return False
    if getXMLTagValue(resp, 'CurrentMute'):
        return True
    return False


def discoverSonos() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    search = ('M-SEARCH * HTTP/1.1\r\n' + 'HOST: 239.255.255.250:1900\r\n' +
              'MAN: ssdp:discover\r\n' + 'MX: 1\r\n' +
              'ST: urn:schemas-upnp-org:device:ZonePlayer:1\r\n')

    sock.sendto(search.encode('ASCII'), ('239.255.255.250', 1900))

    sock.settimeout(5)
    try:
        print('starting discovery')
        while True:
            _, addr = sock.recvfrom(1024)
            print(f'found sonos at {addr[0]}')
            if isGroupCoordinator(addr[0]):
                Sonos(addr[0]).blink()
                print(f'{addr[0]} is group coordinator')
                sock.close()
                return addr[0]
    except OSError:
        sock.close()
    print('discovery ended')
    return None


def writeToConfig(key: str, data: str):
    with open('/config.py', 'r') as file:
        lines = file.readlines()

    file = None
    with open('/config.py', 'w') as file:
        for line in lines:
            if key not in line:
                file.write(line)
        file.write(f'{key} = "{data}"\n')
