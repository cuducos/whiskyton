from app import db

class Whisky(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  distillery = db.Column(db.String(64))
  ci_index = db.Column(db.String(64), index = True, unique = True)
  body = db.Column(db.Integer)
  sweetness = db.Column(db.Integer)
  smoky = db.Column(db.Integer)
  medicinal = db.Column(db.Integer)
  tobacco = db.Column(db.Integer)
  honey = db.Column(db.Integer)
  spicy = db.Column(db.Integer)
  winey = db.Column(db.Integer)
  nutty = db.Column(db.Integer)
  malty = db.Column(db.Integer)
  fruity = db.Column(db.Integer)
  floral = db.Column(db.Integer)
  postcode = db.Column(db.String(16))
  latitude = db.Column(db.Integer)
  longitude = db.Column(db.Integer)
  
  def __repr__(self):
    return '<Distillery: %r>' % (self.distillery)

class Correlation(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  reference = db.Column(db.Integer, index = True)
  whisky = db.Column(db.Integer, db.ForeignKey('whisky.id'))
  r = db.Column(db.Float, index = True)
  
  def __repr__(self):
    return '<Correlation: %r>' % (self.r)
