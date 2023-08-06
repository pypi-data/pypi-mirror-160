"""Handle network calls from Heptapod to the system running the tests.

This necessary to test such things as outbound web hooks and integrations.
"""
from multiprocessing import Process, Queue
from wsgiref.simple_server import make_server


def http_server(queue):
    """Create an HTTP server to receive calls from Heptapod.

    This is intended to run as a child process, with the
    The given `queue` been used to return information to the parent process.

    The first message is the bound port (as an integer)
    """
    def app(environ, start_response):
        status = '204 No Content'
        headers = [('Content-type', 'text/plain; charset=utf-8')]

        start_response(status, headers)
        meth = environ['REQUEST_METHOD']
        if meth in ('POST', 'PUT'):
            length = int(environ['CONTENT_LENGTH'])
            body = environ['wsgi.input'].read(length)
        else:
            body = None

        queue.put(dict(method=meth,
                       body=body,
                       environ={k: v for k, v in environ.items()
                                if isinstance(v, str)}))
        return ''

    with make_server('0.0.0.0', 0, app) as httpd:
        port = httpd.server_address[1]
        queue.put(port)
        httpd.handle_request()


class HttpListener():
    """An HTTP server to listen to HTTP requests from Heptapod.

    The response given by this server is always a `204 No Content`

    Adter init, `self.queue` will receive messages corresponding to
    the handled requests. Each is a `dict` with the following keys:

    - method: the HTTP method (POST, GET etc.)
    - environ: string-valued elements of the WSGI environment (in particular
      all HTTP headers should be there)
    - body: the request body (bytes), or `None` according to `method`
    """

    def __init__(self, heptapod):
        self.queue = Queue()
        self.process = Process(target=http_server,
                               args=(self.queue,))
        self.process.start()
        self.port = self.queue.get()
        self.heptapod = heptapod

    def join(self, timeout):
        self.process.join(timeout)
        if self.process.exitcode is None:  # we've reached the timeout
            self.process.terminate()
        return self.process.exitcode

    def url(self, heptapod):
        """The URL as seen from Heptapod."""
        host = heptapod.reverse_call_host
        if ':' in host:  # should happen only with IPv6 address
            host = '[%s]' % host
        return 'http://%s:%d' % (host, self.port)
