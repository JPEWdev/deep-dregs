#! /usr/bin/env python3
#
# Copyright 2019 Joshua Watt <JPEW.hacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#
# A sample client showing how to use both synchronus and asynchronous APIs to
# send data to the server
#
import argparse
import sys

def async_main(args):
    import aiofiles
    import aiohttp
    import asyncio

    async def stdio_stream(stream):
        reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_running_loop().connect_read_pipe(lambda: reader_protocol, stream)

        chunk = await reader.read(512)
        while chunk:
            yield chunk
            chunk = await reader.read(512)

    async def file_reader(f):
        chunk = await f.read(1024)
        while chunk:
            yield chunk
            chunk = await f.read(1024)

    async def main(args):
        async with aiohttp.ClientSession() as session:
            if args.file == '-':
                response = await session.post(args.target, data=stdio_stream(sys.stdin))
            else:
                # Note: Async currently always chunks, so don't bother checking
                # the argument
                async with aiofiles.open(args.file, 'rb') as f:
                    response = await session.post(args.target, data=file_reader(f))

            print(await response.text())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))

def sync_main(args):
    import requests

    def stream_file(f):
        chunk = f.read(1024)
        while chunk:
            yield chunk
            chunk = f.read(1024)

    if args.file == '-':
        r = requests.post(args.target, data=stream_file(sys.stdin.buffer), stream=True)
    else:
        with open(args.file, 'rb') as f:
            source = f
            if args.chunk:
                source = stream_file(f)
            r = requests.post(args.target, data=source, stream=True)

    print(r.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test client')
    parser.add_argument('file', help='File to stream')
    parser.add_argument('target', help='Target URL')
    parser.add_argument('--async', dest='use_async', action='store_true', help='Use asynchronous backend')
    parser.add_argument('--chunk', action='store_true', help='Force HTTP chunking')

    args = parser.parse_args()

    if args.use_async:
        async_main(args)
    else:
        sync_main(args)

