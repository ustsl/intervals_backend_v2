#!/usr/bin/env python3


from uvicorn import Config as UvicornConfig
from uvicorn import Server

config = UvicornConfig("src.main:app", host="127.0.4.107", port=58461, reload=True)
server = Server(config)

if __name__ == "__main__":
    server.run()
