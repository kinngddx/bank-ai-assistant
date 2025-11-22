from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, command, banking, otp
from .utils.logger import log_info

app = FastAPI(
    title="AI Voice Banking Assistant API",
    description="Backend for voice-based banking operations using NLP + FastAPI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(command.router, prefix="/command", tags=["Command Processing"])
app.include_router(banking.router, prefix="/bank", tags=["Bank Operations"])
app.include_router(otp.router, prefix="/otp", tags=["OTP Verification"])

@app.on_event("startup")
def startup():
    log_info("AI Voice Banking Backend started")

@app.get("/")
def root():
    return {"message": "AI Voice Banking Backend is running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}