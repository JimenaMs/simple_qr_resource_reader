from passlib.hash import sha256_crypt
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from models import User, Resource, Ticket, db
from uuid import uuid4
import yagmail
import StringIO
import qrcode
import yaml

with open("./config.yaml", 'r') as yamlfile:
    cfg = yaml.load(yamlfile)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg['mysql_connect_string']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

yag = yagmail.SMTP(cfg['gmail']['username'], cfg['gmail']['password'])

@app.route("/qr/<id>")
def generate_qr_code(id):
  if Resource.query.filter_by(resource_id=id).first() == None:
    return 'Not Found!', 404
  img = qrcode.make('http://' + cfg['host'] + ':' + str(cfg['port']) + '/' + id)
  base_64_img = StringIO.StringIO()
  img.save(base_64_img, 'PNG')
  value = base_64_img.getvalue()
  base_64_img.close()
  return value, 200, {'Content-Type': 'image/png'}

@app.route("/")
def hello():
  resources = []
  for resource in Resource.query.all():
    resources.append(resource.to_dict())
  return render_template('landing.html', resources=resources)

@app.route("/<id>")
def resource(id):
  resource = Resource.query.filter_by(resource_id=id).first()
  if resource != None:
    return render_template('resource.html', resource = resource)
  else:
    return 'Not Found!', 404

@app.route("/api/resources", methods = ['GET'])
def get_resources():
  resources = []
  for resource in Resource.query.all():
    resources.append(resource.to_dict())
  return jsonify(resources)

@app.route("/api/resources", methods = ['POST'])
def create_resource():
  json = request.get_json()
  resource = Resource(json['resource_id'], json['name'])
  db.session.add(resource)
  db.session.commit()
  return jsonify(resource.to_dict())

@app.route("/api/tickets", methods = ['GET'])
def get_all_tickets():
  tickets = []
  for ticket in Ticket.query.filter_by(status='open').all():
    tickets.append(ticket.to_dict())
  return jsonify(tickets)

@app.route("/api/resources/<id>/tickets", methods = ['GET'])
def get_tickets(id):
  tickets = []
  for ticket in Ticket.query.filter_by(resource_id=id, status='open').all():
    tickets.append(ticket.to_dict())
  return jsonify(tickets)

@app.route("/api/resources/<id>/tickets", methods = ['POST'])
def create_ticket(id):
  json = request.get_json()
  reporter = User.query.filter_by(username=json['reporter'].lower()).first()
  asignee = User.query.filter_by(username=json['asignee'].lower()).first()
  if reporter == None or asignee == None:
    return jsonify({'error': 'bad request'}), 400
  ticket = Ticket(uuid4(), json['title'], json['description'], reporter.user_id, asignee.user_id, 'open', id)

  mail = reporter.username + ' le ha asignado un ticket a ' + asignee.username + ', revisalo en http://' + cfg['host'] + ':' + str(cfg['port']) + '/' + id
  recipients = [str(asignee.email), str(reporter.email)]
  subject = str('Nuevo ticket sobre ' + id)

  print recipients
  print subject
  print mail
  yag.send(to = recipients, subject = subject, contents = [mail, ticket.description])

  db.session.add(ticket)
  db.session.commit()
  return jsonify(ticket.to_dict())

@app.route("/api/resources/<id>/tickets/<ticket>", methods = ['DELETE'])
def close_ticket(id, ticket):
  ticket = Ticket.query.filter_by(resource_id=id, ticket_id=ticket).first()
  ticket.status = 'closed'
  db.session.commit()
  return jsonify(ticket.to_dict())

@app.route("/api/users", methods = ['GET'])
def get_users():
  users = {}
  for user in User.query.all():
    users[user.username] = None
  return jsonify(users)

@app.route("/api/users", methods = ['POST'])
def create_user():
  json = request.get_json()
  hash = sha256_crypt.encrypt("ch4ng3m3")
  user = User(uuid4(), json['username'], json['email'], hash)
  db.session.add(user)
  db.session.commit()
  return jsonify(user.to_dict())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=cfg['debug'], port=cfg['port'])