#!/usr/bin/env python

" Serves the application "

import argparse

def parse_hostname(hostname, default_port=80):
    if hostname.find(':') > 0:
        host, port = hostname.split(':', 1)
        return host, int(port)
    else:
        return hostname, default_port

def serve(app, args):
    host, port = parse_hostname(args.host or 'localhost', default_port=5000)
    if args.port is not None:
        port = args.port

    app.run(host=host, port=port,
            debug=app.config["DEBUG"],
            use_debugger=app.config["DEBUG"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serves the Flask Blog web interface.")
    parser.add_argument("--host", action='store',
                        help="Which address the application is listening to.")
    parser.add_argument("--port", type=int, action='store',
                        help="Which port the application is listening on.")

    from web import app as flask_app
    serve(flask_app, parser.parse_args())
