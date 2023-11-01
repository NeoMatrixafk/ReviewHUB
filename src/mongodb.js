const mongoose=require("mongoose")

mongoose.connect("mongodb://127.0.0.1:27017/MiniProject")
.then(() => {
    console.log("MongoDB connected");
})
.catch((error) => {
    console.error("Failed to connect to MongoDB:", error);
});

const LogInSchema=new mongoose.Schema({
    name:{
        type:String,
        required:true
    },
    password:{
        type:String,
        required:true
    }
})


const collection=new mongoose.model("LogInCollection",LogInSchema)

module.exports=collection