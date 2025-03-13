#!/usr/bin/env python3


from uvicorn import Config as UvicornConfig, Server

config = UvicornConfig("src.main:app", host="127.0.4.107", port=54247, reload=True)
server = Server(config)

if __name__ == "__main__":
    server.run()
