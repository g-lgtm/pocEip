const mongoose = require("mongoose");

mongoose.connect(
    //'mongodb+srv://' + process.env.DB_USER_PASS + '@cluster0.ffuat.mongodb.net/AnalyseField',
    'mongodb+srv://Flylens:Eip2024@poc.1v9gy.mongodb.net/AnalyseField?retryWrites=true&w=majority',
    {useNewUrlParser: true, useUnifiedTopology: true,}
).then(() => console.log('connected to mongodb'))
.catch((err) => console.log('Failed to connect mongodb', err));