from sanic import Sanic
from sanic.response import json

app = Sanic('TestApp')


@app.route('/')
async def index(request):
    return json({'status': 'request'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
