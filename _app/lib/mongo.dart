//
//
//
//
//

import 'package:mongo_dart/mongo_dart.dart';
import 'package:flutter/material.dart';

class mongoDb {
    static String host = "localhost";
    static String port = "3000";
    static String pass = "Eip2024";
  

  static Future<Db> dbConnexion()  async
  {
    var db;
    
    try {
      db = Db('mongodb://$host:$port/Analysefield');
      await db.open();
    }catch (e) {
      print(e);
    }

    var collection = db.collection('fields');
    await collection.find().forEach((v) {
      print (v);
    });

    return(db);
  }
}

// mongodb+srv://Flylens:<password>@cluster0.ffuat.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
