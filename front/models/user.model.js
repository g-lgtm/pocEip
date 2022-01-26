const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
    {
        name: {
            type: String,
        },
        green: {
            type: String,
            default: "100",
        },
        yellow: {
            type: String,
            default: "0",
        }
    },
    {
        timestamps: true,
    }
);

const UserModel = mongoose.model("field", userSchema);

module.exports = UserModel;

/*module.exports = mongoose => {
    var schema = mongoose.Schema(
      {
        name: String,
        green: String,
        yellow: String,
        png: String
      },
      { timestamps: true }
    );
  
    schema.method("toJSON", function() {
      const { __v, _id, ...object } = this.toObject();
      object.id = _id;
      return object;
    });
  
    const Tutorial = mongoose.model("field", schema);
    return Tutorial;
};*/