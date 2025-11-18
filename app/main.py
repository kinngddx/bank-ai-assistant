from fastapi import FastAPI
from .routers import auth, command, banking, otp

app = FastAPI(
    title="AI Voice Banking Assistant API",
    description="Backend for voice-based banking operations using NLP + FastAPI.",
    version="1.0.0"
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(command.router, prefix="/command", tags=["Command Processing"])
app.include_router(banking.router, prefix="/bank", tags=["Bank Operations"])
app.include_router(otp.router, prefix="/otp", tags=["OTP Verification"])

@app.get("/")
def root():
    return {"message": "AI Voice Banking Backend is running 🚀"}
