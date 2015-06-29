from unarea_server.core.framework.server import BaseHandler


class MainHandler(BaseHandler):
    def validate(self, arguments, body):
        return arguments

    def handle(self, request):
        result = u"HANDLED"
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})


class AboutHandler(BaseHandler):
    def validate(self, arguments, body):
        return arguments

    def handle(self, request):
        text = """The tornado.options philosophy is that any module may define options, not just the main entry point.
         So if you might need a bluetooth mac address, you'd define that option in the module that
          interacts with bluetooth. (and if you might need more than one you can set multiple=True).
          The only tricky part is that you must import all modules that define options before calling
          parse_command_line. Truly arbitrary options are not supported by tornado.options."""
        result = text
        return result

    def encode(self, request, result):
        return self.send_response(200, {u"status": result})
