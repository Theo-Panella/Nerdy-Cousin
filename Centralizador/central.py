import falcon

class Resource:
    def on_get(self, req, resp):
        """Handle GET requests."""
        resp.media = {'message': "Hello world"}
        resp.status = falcon.HTTP_200

app = falcon.App()
app.add_route('/', Resource())
