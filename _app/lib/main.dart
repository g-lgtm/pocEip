//
//
//
//
//
import 'package:flutter/material.dart';
import 'dart:async';
import 'package:camera/camera.dart';
import 'camera.dart';

import 'package:mongo_dart/mongo_dart.dart' as dart_mongo;

late final CameraDescription camera_f;

Future<void> main() async {
  // Ensure that plugin services are initialized so that availableCameras()
  // can be called before runApp()
  WidgetsFlutterBinding.ensureInitialized();

  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();

  // Get a specific camera from the list of available cameras.
  camera_f = cameras.first;

  runApp(
    MyApp(),
  );
}


class MyApp extends StatelessWidget {

  static const String _title = 'Flutter Code Sample';

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
        debugShowCheckedModeBanner: false,
      title: _title,
      home: MyStatefulWidget(),
    );
  }
}

class DashBoard extends StatelessWidget{
    Widget build(BuildContext context) {
        return MaterialApp(
            debugShowCheckedModeBanner: false,
            title: 'first_route',
            home: Scaffold(
                body: SingleChildScrollView(
                    child: Column(
                        children: [
                            foo,
                        ],
                    ),
                ),
            ),
        );
    }
}

/// This is the stateful widget that the main application instantiates.
class MyStatefulWidget extends StatefulWidget {
    const MyStatefulWidget({Key? key}) : super(key: key);

    @override
    State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget>
    with TickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green,
        title: const Center(
          child: Text(
            "FLYLENS",
            textAlign: TextAlign.center,
          )
        ),
        bottom: TabBar(
          indicatorColor: Colors.white,
          controller: _tabController,
          tabs: const <Widget>[
            Tab(
              icon: Icon(Icons.dashboard_rounded),
            ),
            Tab(
              icon: Icon(Icons.photo_camera),
            ),
            Tab(
              icon: Icon(Icons.brightness_5_sharp),
            ),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: <Widget>[
          Center(
            child: DashBoard(),
          ),
          Center(
            child: TakePictureScreen(camera: camera_f),
          ),
          Center(
            child: dbfuture(),
          ),
        ],
      ),
    );
  }
}

Widget foo = new GestureDetector(
    onTap: () async {
        dart_mongo.Db db = dart_mongo.Db("mongodb://localhost:27017/test");

        await db.open();

        print("connected to mongodb");

        dart_mongo.DbCollection collection = db.collection('images');

        var data = await collection.find(dart_mongo.where.limit(5)).toList();
        print(data);
    },
    child: new Container(
        height: 40,
        width: 100,
        // decoration: BoxDecoration(
        //     borderRadius: BorderRadius.circular(30),
        //     color: Colors.white,
        // ),
        child: Center(
            child: Text(
                'goToDb',
                style: TextStyle(
                    color: Colors.blue,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1,
                ),
            ),
        ),
    ),
);

class dbfuture extends StatefulWidget {
  const dbfuture({Key? key}) : super(key: key);

  @override
  State<dbfuture> createState() => _dbfuture();
}

class _dbfuture extends State<dbfuture> {
  final Future<String> _calculation = Future<String>.delayed(
    const Duration(seconds: 2),
    () => 'db connected',
  );

  @override
  Widget build(BuildContext context) {
    return DefaultTextStyle(
      style: Theme.of(context).textTheme.headline2!,
      textAlign: TextAlign.center,
      child: FutureBuilder<String>(
        future: _calculation, // a previously-obtained Future<String> or null
        builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
          List<Widget> children;
          if (snapshot.hasData) {                              // loaded
            children = <Widget>[
              const Icon(
                Icons.check_circle_outline,
                color: Colors.green,
                size: 20,
              ),
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text('Result: ${snapshot.data}',
                  style: TextStyle(height: 5, fontSize: 10),
                ),
              )
            ];
          } else if (snapshot.hasError) {                       // error
            children = <Widget>[
              const Icon(
                Icons.error_outline,
                color: Colors.red,
                size: 60,
              ),
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text('Error: ${snapshot.error}'),
              )
            ];
          } else {                                              // loading
            children = const <Widget>[
              SizedBox(
                width: 30,
                height: 30,
                child: CircularProgressIndicator(),
              ),
              Padding(
                padding: EdgeInsets.only(top: 16),
                child: Text('Connecting to mongoDB...',
                  style: TextStyle(height: 5, fontSize: 10),
                ),
              )
            ];
          }
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: children,
            ),
          );
        },
      ),
    );
  }
}
