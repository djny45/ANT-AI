import express from "express";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/health", (req,res)=>{
  res.json({status:"ok", service:"ANT-AI"});
});

app.post("/api/chat", async(req,res,next)=>{
  try {
    const message = req.body?.message;

    if (typeof message !== "string" || message.trim() === "") {
      return res.status(400).json({
        error: "invalid_request",
        message: "field 'message' must be a non-empty string"
      });
    }

    res.json({
      reply:`ANT online: ${message}`,
      state:"response"
    });
  } catch (error) {
    next(error);
  }
});

// JSON body parse failures and route errors must not hang the request
app.use((error, req, res, next)=>{
  console.error("ANT API request failed", error);
  if (res.headersSent) {
    return next(error);
  }
  const status = error.status && error.status >= 400 && error.status < 600 ? error.status : 500;
  res.status(status).json({
    error: error.type || error.name || "internal_error",
    message: error.message || "unexpected server error"
  });
});

const server = app.listen(3000,()=>{
 console.log("ANT API running on 3000");
});

server.on("error",(error)=>{
  console.error("ANT API failed to start", error);
  process.exitCode = 1;
});

process.on("unhandledRejection",(reason)=>{
  console.error("Unhandled promise rejection in ANT API", reason);
});

process.on("uncaughtException",(error)=>{
  console.error("Uncaught exception in ANT API", error);
  process.exitCode = 1;
  server.close(()=>process.exit(1));
});
