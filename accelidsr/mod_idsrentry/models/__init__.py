from accelidsr import db
from bson import ObjectId
from flask import flash
import sys
import bson

def fetch_by_id(id, collection):
    if not id or not collection:
        return None

    col = db.get_collection(collection)
    try:
        doc = col.find_one({'_id':  ObjectId(str(id))})
        if doc:
            return doc
        return None
    except bson.errors.InvalidId:
        # Ops, the id provided is not valid
        return None

def save(dbobj):
    if not dbobj or not dbobj.getCollection():
        flash("No object or collection specifed")
        return None
    col = db.get_collection(dbobj.getCollection())
    objid = dbobj.getId()
    objdict = dbobj.getDict()
    # Remove the _id from the dict to save. We want mongoDB to create the
    # ids automatically (if record doesn't exist yet) or update the record
    # without updating the value for _id
    del objdict['_id']
    if objid:
        #try:
        out = col.update_one(
           {"_id": ObjectId(str(objid))},
           {"$set": objdict },
           upsert=True)
        modifcount = out.modified_count
        if modifcount == 0:
            newid = out.upserted_id
            if newid:
                newid = str(newid)
                objdict['_id'] = newid.toString()
                dbobj.update(objdict)
                return dbobj
            objdict['_id'] = objid
            return None
        if modifcount == 1:
            objdict['_id'] = objid
            return dbobj
        else:
            # More than one record updated?
            objdict['_id'] = objid
            flash("More than one record updated!")
            return None
        #except:
        #    flash('Unexpected error: %s' % sys.exc_info()[0])
        #    return None
    else:
        # This is a new object. Needs to be inserted
        out = col.insert_one(objdict)
        newid = out.inserted_id
        if out:
            newid = str(newid)
            objdict['_id'] = newid
            dbobj.update(objdict)
            return dbobj
        objdict['_id'] = objid
        return False
