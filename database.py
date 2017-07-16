
from pymongo import MongoClient 
import pymongo

def connect( constring, dbname ):
  client = MongoClient( constring )
  return client[ dbname ]

def createindex( db, username ):
  result = db[ username ].create_index( [('date', pymongo.ASCENDING)], unique=True )
  return result


def addnewlog( db, username, data ):
  log = db[ username ]

  # A second entry for that day
  if data.get('start') == None: 
    entry = log.find_one({ 'date': data.get('date') })
    
    # The day record does not exist just create it
    if entry == None:
      result = log.insert_one( data )
      return result.inserted_id

    # update the specific field in record
    elif data.get( 'end' ) != None:
      result = log.update_one({ 'date': data.get('date') }, {
        '$set':{
          'end': data.get( 'end' )
        }
      },
      upsert=True )
    elif data.get( 'break-end' ) != None:  
      result = log.update_one({ 'date': data.get('date') }, {
        '$set':{
          'break-end': data.get( 'break-end' )
        }
      },
      upsert=True )
    elif data.get( 'break-start' ) != None:
      result = log.update_one({ 'date': data.get('date') }, {
        '$set':{
          'break-start': data.get( 'break-start' )
        }
      },
      upsert=True )
    return result.modified_count

  else:
    try:
      result = log.insert_one( data )
      result = 'ok'
    except pymongo.errors.DuplicateKeyError as e:
      result = str(e)
    
    return result


def getlastNlogs( db, username, n ):
  log = db[ username ]
  count = log.count()
  if count <= n:
    logs = log.find()
  else:
    logs = log.find().skip( count - n ) 
  result = []
  for doc in logs:
    result.append( doc )
  return result
  