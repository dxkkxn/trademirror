const {verify} = require("jsonwebtoken")
const User = require("../models/user")
// middleware to check wether user is logged in

const protected = async (req, res, next) => {

  const authorization = req.headers["authorization"]

  if(!authorization)
    return res.status(500).json({
      message: "No Token",
      type: "error",
    })

  const token = authorization.split(" ")[1]
  let id
  try{
    id = verify(token, process.env.JWS_TOKEN).id
  } catch {
    return res.status(500).json({
      message: "invalid token",
      type: "error",
    })
  }
  if(!id)
    return res.status(500).json({
      message: "invalid token",
      type: "error",
    })
  const user = await User.findById(id)
  if(!user)
    return res.status(500).json({
      message: "invalid user",
      type: "error",
    })
  req.user = user
  next()
}

module.exports = { protected }
