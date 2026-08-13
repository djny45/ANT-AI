import express from "express";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/health", (req,res)=>{
  res.json({status:"ok", service:"ANT-AI"});
});

app.post("/api/chat", async(req,res)=>{
  const message = req.body.message || "";

  res.json({
    reply:`ANT online: ${message}`,
    state:"response"
  });
});

app.listen(3000,()=>{
 console.log("ANT API running on 3000");
});
