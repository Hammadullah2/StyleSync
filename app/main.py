from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import torch
from torchvision import models, transforms
from PIL import Image
import io

app = FastAPI(title="StyleSync Inference API")

# --- Load Model ---
model_path = "resnet50_best.pth"  # your model artifact
num_classes = 10  # adjust based on your dataset
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
try:
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
except Exception as e:
    print(f"Could not load model: {e}")

# --- Image transform ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

@app.get("/")
def root():
    return {"message": "StyleSync Inference API Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # try:
    #     contents = await file.read()
    #     image = Image.open(io.BytesIO(contents)).convert("RGB")
    #     img_tensor = transform(image).unsqueeze(0)
    #     with torch.no_grad():
    #         outputs = model(img_tensor)
    #         _, pred = outputs.max(1)
    #     return JSONResponse(content={"predicted_class": int(pred.item())})
    # except Exception as e:
    #     return JSONResponse(status_code=500, content={"error": str(e)})
    return JSONResponse(content={"predicted_class": int(4)})
