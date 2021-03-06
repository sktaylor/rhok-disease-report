#!/usr/bin/python

import os
import tornado.ioloop
import tornado.web

from clientlogin import ClientLogin
from sqlbuilder import SQL
import ftclient
from fileimporter import CSVImporter

settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}

USERNAME = 'rhokdiseasereport@gmail.com'
PASSWORD = 'diseasereport'
TABLE_ID = 948691
DISEASE_TABLE_ID = 949444

TOKEN = ClientLogin().authorize(USERNAME, PASSWORD)
FT_CLIENT = ftclient.ClientLoginFTClient(TOKEN)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

class DiseaseHandler(tornado.web.RequestHandler):
  def get(self):
    diseases = FT_CLIENT.query(SQL().select(DISEASE_TABLE_ID, ['DiseaseID', 'Disease']))
    print diseases
    diseases = diseases.split('\n')
    print diseases
    options = []
    print diseases
    for disease in diseases[2:]:
      disease = disease.split(",")
      try:
        option = {
          'id' : disease[0],
         'disease' : disease[1]
        }
        options.append(option)
      except:
        pass
    self.write(str(options))

class MapHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("map.html")

class DiseaseReportHandler(tornado.web.RequestHandler):
  def post(self):
    arguments = {
      'Latitude' : str(self.get_argument('lat')[0]),
      'Longitude' : str( self.get_argument('lon')[0]),
      'DiagnosisTime' : str(self.get_argument('date')[0]),
      'DiseaseID' : str(self.get_argument('diseaseId')[0])
    }
    print 'arguments', arguments  
    
    print FT_CLIENT.query(SQL().select(int(TABLE_ID)))

    results = FT_CLIENT.query(SQL().showTables())
    print results
    print(self.request.arguments)
    
    rowid = int(FT_CLIENT.query(SQL().insert(TABLE_ID, arguments)).split("\n")[1])
    print 'rowid:', rowid
    self.render('index.html')



application = tornado.web.Application([
  (r"/", IndexHandler),
  (r"/index", IndexHandler),
  (r"/map", MapHandler),
  (r"/report", DiseaseReportHandler),
  (r"/disease", DiseaseHandler)
], **settings)

if __name__ == "__main__":
  application.listen(80)
  print("Server listening on all addresses, port 80")
  tornado.ioloop.IOLoop.instance().start()

