const UserModel = require('../models/user.model');
const ObjectID = require('mongoose').Types.ObjectId;

module.exports.getFieldsInfos = async (req, res) => {
    const fields = await UserModel.find().select();
    res.status(200).json(fields);
}