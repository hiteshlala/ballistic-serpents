#! python3
"""

  Author: Hitesh Lala
  
  Description: Main Server file

"""

import sys
import time
import json

from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

# my code files
import config
import database

app = Flask( __name__ )

print( 'Python Version: ' + sys.version  )
print( 'Application Name: ' +  config.name )
print( 'Application Running on Port: ' + str(config.port) )

up_since = time.asctime()
db = database.connect( config.mongo, config.dbname )

# each user has her own log collection and will need indexing
index = database.createindex( db, 'hiteshlala' )

@app.route( '/status' )
def status():
  if request.headers['Accept'].find( 'html') == -1 :
    data = {
      'up_since': up_since,
      'name': config.name,
      'version': config.version,
      'status': 'ok'
    }
    # return json.JSONEncoder().encode( data ) # this took a really long time!!
    return str( data )    
  else :
    return render_template( 'status.html', version=config.version, name=config.name, upsince=up_since)


@app.route( '/' )
def home():
  # right now assume only one user: hiteshlala
  user = 'hiteshlala'
  count = 20

  # get user times from DB and pass to front end - process on front end
  logs = database.getlastNlogs( db, user, count ) # an array of dcouments

  # display error message if one exists
  if request.args.get('error', '') != None:
    error = request.args.get('error', '')
  else:
    error = ''
  
  return render_template( 'home.html', version=config.version, name=config.name, user=user, error=error, logs=logs )



@app.route( '/times', methods=['GET', 'POST'] )
def times():
  if request.method == 'POST':
    if not request.form or not request.form['mytime'] or not request.form['event']:
      return redirect( url_for( 'home' ) )

    orignal = request.form['mytime']
    event = request.form['event']
    date = orignal.split('T')[0]
    time = orignal.split('T')[1]
    data = {
      'orignal': orignal,
      'date': date,
      'user': 'hiteshlala'
    }
    data[ event ] = time

    # save the data in DB
    result = database.addnewlog( db, 'hiteshlala', data )
    if result == 'ok':
      return redirect( url_for( 'home' ) )
    else:
      return redirect( url_for( 'home', error='Unable to log time: '+ result ) )
  
  else :
    return render_template( 'times.html', version=config.version, name=config.name, user="hiteshlala" )


if __name__ == '__main__':
  app.run( port = config.port )

