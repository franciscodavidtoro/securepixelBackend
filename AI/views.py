from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AtencionSerializer, EmocionesSerializer
from .models import atencion, emociones


import base64
from io import BytesIO
from PIL import Image


import torch.nn.functional as F
from transformers import AutoImageProcessor, AutoModelForImageClassification

processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")


class AtencionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AtencionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class ProcesarImgEmocionesAPIView(APIView):
    def post(self, request):
        base64_image = request.data.get("image")
        if not base64_image:
            return Response({"error": "No se recibió imagen"}, status=400)

        # Decodificar imagen base64
        format, imgstr = base64_image.split(';base64,')
        image_bytes = base64.b64decode(imgstr)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Preprocesar y predecir
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # Obtener emoción más probable
        predicted_class_idx = outputs.logits.argmax(-1).item()
        predicted_emotion = model.config.id2label[predicted_class_idx]

        # Obtener probabilidades de todas las emociones
        probabilities = F.softmax(outputs.logits, dim=-1)[0]
        emociones = {
            model.config.id2label[idx]: float(prob * 100)
            for idx, prob in enumerate(probabilities)
        }

        # Ordenar de mayor a menor
        emociones_ordenadas = sorted(
            emociones.items(), key=lambda x: x[1], reverse=True
        )

        return Response({
            "emocion_predicha": predicted_emotion,
            "emociones": emociones_ordenadas
        })
        