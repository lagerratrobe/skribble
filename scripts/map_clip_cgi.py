#! /usr/bin/python

'''CGI script to create maps based on extents of country geometry stored in PostGIS DB.
   A MapServer project of the entire world exists separately.  The country extents are 
   applied via Python mapscript to that map project, so that only a small amount of the
   entire map is returned.'''

import cgi
import mapscript
import psycopg

def DrawMap(name, bbox):
  min_x, min_y, max_x, max_y = bbox.split(",")
  mapobject = mapscript.mapObj('gis_layers.map')
  mapobject.setExtent(float(min_x), float(min_y), float(max_x), float(max_y))
  country = mapobject.getLayerByName("country")
  country_name = country.getClass(0)
  country_name.setExpression(name)
  country_mask = mapobject.getLayerByName("country_mask")
  mask_country = country_mask.getClass(0)
  expression = "('[NAME]' NE '%s')" % (name)
  mask_country.setExpression(expression)
  mapimage = mapobject.draw()
  #mapimage.save("test.png") # TO TEST MAPSERVER OUTPUT
  image = mapimage.getBytes()
  print "Content-Type: %s" % mapimage.format.mimetype
  print "Content-Length: %d" % len(image)
  print
  print image

def MakeBbox(name):
  """Create dictionary of id/bbox pairs using the coastlines 'id' field."""
  conn = psycopg.connect("host='localhost' dbname='unep' user='randre'")
  cur = conn.cursor()
  sql = "SELECT ST_Extent(the_geom) FROM coastlines WHERE name = '%s'" % (name)
  cur.execute(sql)
  bbox = cur.fetchall()
  coords = bbox[0][0].strip("BOX()")
  new_coords = coords.replace(" ", ",")
  return new_coords

def ParseUrl():
  f = cgi.FieldStorage()
  country = f['name'].value
  return country
  
def main():
  name = ParseUrl()
  bbox = MakeBbox(name)
  DrawMap(name, bbox)

if __name__ == "__main__":
  main()
