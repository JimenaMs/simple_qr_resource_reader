from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
  """docstring for User"""
  user_id = db.Column(db.String(36), primary_key=True)
  username = db.Column(db.String(20), unique=True)
  email = db.Column(db.String(40), unique=True)
  password = db.Column(db.String(80))

  def __init__(self, user_id, username, email, password):
    self.user_id = user_id
    self.username = username
    self.email = email
    self.password = password

  def __repr__(self):
    return '<User %r>' % self.user_id

  def to_dict(self):
    return {
      'user_id': self.user_id,
      'username': self.username,
      'email': self.email
    }

class Resource(db.Model):
  """docstring for Resource"""
  resource_id = db.Column(db.String(36), primary_key=True)
  name = db.Column(db.String(50))
  owner = db.Column(db.String(40))
  model = db.Column(db.String(25))
  brand = db.Column(db.String(25))
  series = db.Column(db.String(30))
  area = db.Column(db.String(20))
  subarea = db.Column(db.String(20))

  def __init__(self, resource_id, name):
    self.resource_id = resource_id
    self.name = name
    self.owner = owner
    self.model = model
    self.brand = brand
    self.series = series
    self.area = area
    self.subarea = subarea

  def __repr__(self):
    return '<Resource %s>' % self.resource_id

  def to_dict(self):
    return {
      'resource_id': self.resource_id,
      'name': self.name,
      'owner': self.owner,
      'model': self.model,
      'brand': self.brand,
      'series': self.series,
      'area': self.area,
      'subarea': self.subarea
    }


class Ticket(db.Model):
  """docstring for Ticket"""
  ticket_id = db.Column(db.String(36), primary_key=True)
  title = db.Column(db.String(100))
  description = db.Column(db.String(8000))
  reporter = db.Column(db.String(36))
  asignee = db.Column(db.String(36))
  status = db.Column(db.String(10))
  resource_id = db.Column(db.String(36), db.ForeignKey('resource.resource_id'))

  def __init__(self, ticket_id, title, description, reporter, asignee, status, resource_id):
    self.ticket_id = ticket_id
    self.title = title
    self.description = description
    self.reporter = reporter
    self.asignee = asignee
    self.status = status
    self.resource_id = resource_id

  def __repr__(self):
    return '<Ticket %s>' % self.ticket_id

  def to_dict(self):
    return {
      'ticket_id': self.ticket_id,
      'title': self.title,
      'description': self.description,
      'reporter': self.reporter,
      'asignee': self.asignee,
      'status': self.status,
      'resource_id': self.resource_id
    }