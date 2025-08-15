from django.shortcuts import render

# Create your views here.


from .serializers import AtencionSerializer, EmocionesSerializer
from .models import atencion, emociones

from preguntas.models import Prueba



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
    """Procesa imágenes para detectar emociones y guarda los resultados en la base de datos.
    """     
    @torch.no_grad()
    def post(self, request, pk):
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

        # Preprocesar imagen
        try:
            inputs = processor(images=image, return_tensors="pt").to(device)
        except Exception:
            return Response({"error": "No se pudo procesar la imagen"}, status=400)

        # Obtener predicciones
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        confidence, predicted_class_idx = torch.max(probs, dim=-1)
        confidence = confidence.item()
        predicted_emotion = model.config.id2label[predicted_class_idx.item()]

        # Si la confianza es muy baja, se considera que no se detectó emoción clara
        if confidence < 0.15:
            return Response({"error": "No se detectó una emoción con suficiente confianza"}, status=200)

        # Guardar en DB
        prueva= Prueba.objects.filter(id=pk).first()
        if not prueva:
            return Response({"error": "Prueba no encontrada"}, status=404)
        
        emocionDB = emociones.objects.get_or_create(prueba=prueva, defaults={
            'emociones': {},
            'emocionPredominante': None,
            'numImgProsesadas': 0,
            })[0]
        JSON_emociones = emocionDB.emociones or {}
        JSON_emociones[predicted_emotion] = JSON_emociones.get(predicted_emotion, 0) + 1
        emocionDB.emociones = JSON_emociones

        # Obtener la emoción predominante
        mayor_valor = max(JSON_emociones.values())
        emocion_predominante = [key for key, value in JSON_emociones.items() if value == mayor_valor]
        emocionDB.emocionPredominante = emocion_predominante[0] if emocion_predominante else None
        emocionDB.numImgProsesadas += 1
        emocionDB.save()

        return Response({
            "emocion_predicha": predicted_emotion,
            "confianza": round(confidence, 3)
        })

        