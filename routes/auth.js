const protected = require("../utils/protected")
const { hash, compare } = require("bcryptjs");
// importing the helper functions
const {
  createAccessToken,
  sendAccessToken,
} = require("../utils/tokens");

const User = require("../models/user")

router.post("/signin", async(req, res) => {
  try {
    const { username, password } = req.body
    const user = await User.findOne({where:{username:username}})
    
    if(!user) 
      return res.status(500).json({
        message: "L'utilisateur n'existe pas",
        type: "error",
      })

    //compare
    const match = await compare(password, user.password)

    if(!match)
       return res.status(500).json({
         message: "mot de passe incorrect"
        type: "error",
      })

    // OK !
    const token = createAccessToken(user._id)
    
    sendAccessToken(req, res, token)

  } catch (error) {
    res.status(500).json({
      type:"error",
      message:"Internal error",
    })
  }
}

router.post("/register", async(res, req) => {
  try {
    const { username, password } = req.body
    const user = await User.findOne({where:{username:username}})

    if(user)
      return res.status(500).json({
        message: "cet utilisateur existe déjà",
        type: "wrong data",
      })

    if(!checkPassword(password))
      return res.status(500).json({
        message: "mot de passe invalide",
        type: "wrong data",
      })


    const resultat = await createUser(username, password);
    if(resultat < 0)
      res.status(500).json({
        message:"internal error",
        type: "error",
    })

    res.status(200).json({
      message: "user created",
      type: "success",
    )}
  } catch(error) {
    res.status(500).json({
      message: "internal error",
      type: "error",
    })
  }
}

router.get("/protected", protected, async(req, res) => {
  try {
    // if user exists in the request, send the data
    if (req.user)
      return res.json({
        message: "You are logged in! 🤗",
        type: "success",
        user: req.user,
      });
    // if user doesn't exist, return error
    return res.status(500).json({
      message: "You are not logged in! 😢",
      type: "error",
    });
  } catch (error) {
    res.status(500).json({
      type: "error",
      message: "Error getting protected route!",
      error,
    });
  }
});
