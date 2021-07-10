import picoweb
import network

sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()

app = picoweb.WebApp(__name__)
 
htmlContent = '''
<table>
  <tr>
    <th>value</th>
    <th>timestamp</th>
  </tr> 
  <tr>
    <td>10</td>
    <td>10:00</td>
  </tr>
  <tr>
    <td>11</td>
    <td>11:00</td>
  </tr>
</table>
'''
import network

def qs_parse(qs):
 
  parameters = {}
  ampersandSplit = qs.split("&")
 
  for element in ampersandSplit:
    equalSplit = element.split("=")
    parameters[equalSplit[0]] = equalSplit[1]
 
  return parameters


@app.route("/html")
def html(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")
    yield from resp.awrite(htmlContent)
 
@app.route("/text")
def text(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/plain")
    yield from resp.awrite(htmlContent)


@app.route("/hello")
def hello(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")
 

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")
 
    htmlFile = open('tables.html', 'r')
 
    for line in htmlFile:
      yield from resp.awrite(line)


@app.route("/query")
def query(req, resp):
    queryString = req.qs
 
    parameters = qs_parse(queryString)
 
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Parameter 1 value: " + parameters["param1"] + "\n")
  
# Main program

app.run( host = '192.168.178.53', port=80, debug=-1, lazy_init=False, log=None)
