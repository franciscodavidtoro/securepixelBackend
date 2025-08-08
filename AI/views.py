from django.shortcuts import render

# Create your views here.


from .serializers import AtencionSerializer, EmocionesSerializer
from .models import atencion, emociones





from rest_framework.views import APIView
from rest_framework.response import Response
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch.nn.functional as F
import torch
from PIL import Image
from io import BytesIO
import base64




class AtencionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AtencionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    


# Precarga
processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

class ProcesarImgEmocionesAPIView(APIView):
    @torch.no_grad()
    def post(self, request):
        base64_image = request.data.get("image")
        if not base64_image:
            return Response({"error": "No se recibió imagen"}, status=400)

        # Decodificar imagen base64
        try:
            format, imgstr = base64_image.split(';base64,')
            image_bytes = base64.b64decode(imgstr)
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except Exception:
            return Response({"error": "Imagen inválida"}, status=400)

        # Preprocesar y predecir
        inputs = processor(images=image, return_tensors="pt").to(device)
        outputs = model(**inputs)

        # Obtener emoción más probable
        predicted_class_idx = outputs.logits.argmax(-1).item()
        predicted_emotion = model.config.id2label[predicted_class_idx]

        # Obtener probabilidades
        probabilities = F.softmax(outputs.logits, dim=-1)[0]
        emociones = {
            model.config.id2label[idx]: float(prob * 100)
            for idx, prob in enumerate(probabilities)
        }
        emociones_ordenadas = sorted(emociones.items(), key=lambda x: x[1], reverse=True)

        return Response({
            "emocion_predicha": predicted_emotion,
            "emociones": emociones_ordenadas
        })

        