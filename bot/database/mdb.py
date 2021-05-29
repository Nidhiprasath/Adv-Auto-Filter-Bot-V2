From: <Saved by Blink>
Snapshot-Content-Location: https://raw.githubusercontent.com/TroJanzHEX/Auto-Filter-Bot-V2/main/database/mdb.py
Subject: 
Date: Sat, 29 May 2021 07:19:06 -0000
MIME-Version: 1.0
Content-Type: multipart/related;
	type="text/html";
	boundary="----MultipartBoundary--jEqLfnsM9oNb4ZGEk7dPj5fDwQgP5UcWMcdjXwhLYr----"


------MultipartBoundary--jEqLfnsM9oNb4ZGEk7dPj5fDwQgP5UcWMcdjXwhLYr----
Content-Type: text/html
Content-ID: <frame-7F7AD1ABE0A73A1F93E945836F9551AA@mhtml.blink>
Content-Transfer-Encoding: quoted-printable
Content-Location: https://raw.githubusercontent.com/TroJanzHEX/Auto-Filter-Bot-V2/main/database/mdb.py

<html><head><meta http-equiv=3D"Content-Type" content=3D"text/html; charset=
=3DUTF-8"></head><body><pre style=3D"word-wrap: break-word; white-space: pr=
e-wrap;">#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


import re
import pymongo

from pymongo.errors import DuplicateKeyError
from marshmallow.exceptions import ValidationError

from config import DATABASE_URI, DATABASE_NAME


myclient =3D pymongo.MongoClient(DATABASE_URI)
mydb =3D myclient[DATABASE_NAME]



async def savefiles(docs, group_id):
    mycol =3D mydb[str(group_id)]
   =20
    try:
        mycol.insert_many(docs, ordered=3DFalse)
    except Exception:
        pass


async def channelgroup(channel_id, channel_name, group_id, group_name):
    mycol =3D mydb["ALL DETAILS"]

    channel_details =3D {
        "channel_id" : channel_id,
        "channel_name" : channel_name
    }

    data =3D {
        '_id': group_id,
        'group_name' : group_name,
        'channel_details' : [channel_details],
    }
   =20
    if mycol.count_documents( {"_id": group_id} ) =3D=3D 0:
        try:
            mycol.insert_one(data)
        except:
            print('Some error occured!')
        else:
            print(f"files in '{channel_name}' linked to '{group_name}' ")
    else:
        try:
            mycol.update_one({'_id': group_id},  {"$push": {"channel_detail=
s": channel_details}})
        except:
            print('Some error occured!')
        else:
            print(f"files in '{channel_name}' linked to '{group_name}' ")


async def ifexists(channel_id, group_id):
    mycol =3D mydb["ALL DETAILS"]

    query =3D mycol.count_documents( {"_id": group_id} )
    if query =3D=3D 0:
        return False
    else:
        ids =3D mycol.find( {'_id': group_id} )
        channelids =3D []
        for id in ids:
            for chid in id['channel_details']:
                channelids.append(chid['channel_id'])

        if channel_id in channelids:
            return True
        else:
            return False


async def deletefiles(channel_id, channel_name, group_id, group_name):
    mycol1 =3D mydb["ALL DETAILS"]

    try:
        mycol1.update_one(
            {"_id": group_id},
            {"$pull" : { "channel_details" : {"channel_id":channel_id} } }
        )
    except:
        pass

    mycol2 =3D mydb[str(group_id)]
    query2 =3D {'channel_id' : channel_id}
    try:
        mycol2.delete_many(query2)
    except:
        print("Couldn't delete channel")
        return False
    else:
        print(f"filters from '{channel_name}' deleted in '{group_name}'")
        return True


async def deletealldetails(group_id):
    mycol =3D mydb["ALL DETAILS"]

    query =3D { "_id": group_id }
    try:
        mycol.delete_one(query)
    except:
        pass


async def deletegroupcol(group_id):
    mycol =3D mydb[str(group_id)]

    if mycol.count() =3D=3D 0:
        return 1

    try:   =20
        mycol.drop()
    except Exception as e:
        print(f"delall group col drop error - {str(e)}")
        return 2
    else:
        return 0


async def channeldetails(group_id):
    mycol =3D mydb["ALL DETAILS"]

    query =3D mycol.count_documents( {"_id": group_id} )
    if query =3D=3D 0:
        return False
    else:
        ids =3D mycol.find( {'_id': group_id} )
        chdetails =3D []
        for id in ids:
            for chid in id['channel_details']:
                chdetails.append(
                    str(chid['channel_name']) + " ( &lt;code&gt;" + str(chi=
d['channel_id']) + "&lt;/code&gt; )"
                )
            return chdetails


async def countfilters(group_id):
    mycol =3D mydb[str(group_id)]

    query =3D mycol.count()

    if query =3D=3D 0:
        return False
    else:
        return query

       =20
async def findgroupid(channel_id):
    mycol =3D mydb["ALL DETAILS"]

    ids =3D mycol.find()
    groupids =3D []
    for id in ids:
        for chid in id['channel_details']:
            if channel_id =3D=3D chid['channel_id']:
                groupids.append(id['_id'])
    return groupids


async def searchquery(group_id, name):

    mycol =3D mydb[str(group_id)]

    filenames =3D []
    filelinks =3D []

    # looking for a better regex :(
    pattern =3D name.lower().strip().replace(' ','.*')
    raw_pattern =3D r"\b{}\b".format(pattern)
    regex =3D re.compile(raw_pattern, flags=3Dre.IGNORECASE)

    query =3D mycol.find( {"file_name": regex} )
    for file in query:
        filename =3D "[" + str(file['file_size']//1048576) + "MB] " + file[=
'file_name']
        filenames.append(filename)
        filelink =3D file['link']
        filelinks.append(filelink)
    return filenames, filelinks


</pre></body></html>
------MultipartBoundary--jEqLfnsM9oNb4ZGEk7dPj5fDwQgP5UcWMcdjXwhLYr------
