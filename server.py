from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import StringIO
import qrcode
import uuid
import yaml

with open("config.yaml", 'r') as yamlfile:
    cfg = yaml.load(yamlfile)

app = Flask(__name__)

resources = {}

resources['MAQX09'] = {
  'id': 'MAQX09',
  'description': 'Quirofano',
  'tickets': [
    {
      'id': 'd2274dcc-f588-4f2c-a6b8-044c2e450295',
      'title': 'Fuga en la toma de oxigeno',
      'description': 'Hay una fuga, reparala',
      'reporter': 'Jimena',
      'asignee': 'Un Chango'
    }
  ]
}

@app.route("/qr/<id>")
def generate_qr_code(id):
  img = qrcode.make('http://' + cfg['host'] + ':' + str(cfg['port']) + '/' + id)
  base_64_img = StringIO.StringIO()
  img.save(base_64_img, 'PNG')
  value = base_64_img.getvalue()
  base_64_img.close()
  return value, 200, {'Content-Type': 'image/png'}

@app.route("/")
def hello():
  return render_template('landing.html', resources=resources)

@app.route("/<id>")
def resource(id):
  if id in resources:
    return render_template('resource.html', resource=resources[id])
  else:
    return 'Not Found!', 404

@app.route("/api/resources", methods = ['GET'])
def get_resources():
  return jsonify(resources)

@app.route("/api/resources", methods = ['POST'])
def create_resource():
  global resources
  json = request.get_json()
  if 'id' not in json or 'description' not in json:
    return 'Bad Request!', 400
  resources[json['id']] = json if id not in resources else resources[id]
  return jsonify(resources[json['id']])

@app.route("/api/resources/<id>/tickets", methods = ['GET'])
def get_tickets(id):
    return jsonify(resources[id]['tickets'])

@app.route("/api/resources/<id>/tickets", methods = ['POST'])
def create_ticket(id):
  global resources
  json = request.get_json()
  json['id'] = str(uuid.uuid4());
  resources[id]['tickets'].append(json)
  return jsonify(json)

@app.route("/api/resources/<id>/tickets/<ticket>", methods = ['DELETE'])
def delete_ticket(id, ticket):
  global resources
  for i in xrange(len(resources[id]['tickets'])):
    print resources[id]['tickets'][i]['id']
    if resources[id]['tickets'][i]['id'] == ticket:
      deleted_ticket = resources[id]['tickets'][i]
      resources[id]['tickets'].pop(i)
      return jsonify(deleted_ticket)
  return 'Not Found', 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=cfg['debug'], port=cfg['port'])