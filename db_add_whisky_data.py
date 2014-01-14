#!flask/bin/python
from app import db, models
file_handler = open('db_add_whisky_data.txt', 'r')
for line in file_handler:
  cells = line.split(',')
  row = models.Whisky(
    distillery = cells[1].strip(),
    ci_index = cells[1].strip().lower(),
    body = int(cells[2]),
    sweetness = int(cells[3]),
    smoky = int(cells[4]),
    medicinal = int(cells[5]),
    tobacco = int(cells[6]),
    honey = int(cells[7]),
    spicy = int(cells[8]),
    winey = int(cells[9]),
    nutty = int(cells[10]),
    malty = int(cells[11]),
    fruity = int(cells[12]),
    floral = int(cells[13]),
    postcode = cells[14].strip(),
    latitude = cells[15].strip(),
    longitude = cells[16].strip())
  db.session.add(row)
    
db.session.commit()
