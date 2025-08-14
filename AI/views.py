from django.shortcuts import render
from .serializers import AtencionSerializer, EmocionesSerializer
from .models import atencion, emociones
from preguntas.models import Prueba

from rest_framework.views import APIView
from rest_framework.response import Response

from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
from io import BytesIO
import base64
import os

# ===== CONFIGURACIÓN IA =====
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_DIR = "/tmp/emotion_model"

# Descargar y cargar el modelo solo una vez por ciclo de vida del dyno
def load_emotion_model():
    global processor, model
    if not os.path.exists(MODEL_DIR):
        print("📥 Descargando modelo de Hugging Face...")
        processor = AutoImageProcessor.from_pretrained(
            "dima806/facial_emotions_image_detection",
            cache_dir=MODEL_DIR
        )
        model = AutoModelForImageClassification.from_pretrained(
            "dima806/facial_emotions_image_detection",
            cache_dir=MODEL_DIR
        )
    else:
        print("✅ Cargando modelo desde cache temporal...")
        processor = AutoImageProcessor.from_pretrained(MODEL_DIR)
        model = AutoModelForImageClassification.from_pretrained(MODEL_DIR)

    model.eval()
    model.to(device)

# Cargar modelo al iniciar el servidor
load_emotion_model()

# ===== VISTAS =====
class AtencionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AtencionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProcesarImgEmocionesAPIView(APIView):
    """Procesa imágenes para detectar emociones y guarda los resultados en la base de datos."""
    @torch.no_grad()
    def post(self, request, pk):
        base64_image = request.data.get("image")
        if not base64_image:
            return Response({"error": "No se recibió imagen"}, status=400)

        # Decodificar imagen base64
        try:
            _, imgstr = base64_image.split(';base64,')
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

        # Si la confianza es muy baja
        if confidence < 0.15:
            return Response({"error": "No se detectó una emoción con suficiente confianza"}, status=200)

        # Guardar en DB
        prueba = Prueba.objects.filter(id=pk).first()
        if not prueba:
            return Response({"error": "Prueba no encontrada"}, status=404)

        emocionDB = emociones.objects.get_or_create(prueba=prueba, defaults={
            'emociones': {},
            'emocionPredominante': None,
            'numImgProsesadas': 0,
        })[0]

        JSON_emociones = emocionDB.emociones or {}
        JSON_emociones[predicted_emotion] = JSON_emociones.get(predicted_emotion, 0) + 1
        emocionDB.emociones = JSON_emociones

        # Obtener emoción predominante
        mayor_valor = max(JSON_emociones.values())
        emocion_predominante = [key for key, value in JSON_emociones.items() if value == mayor_valor]
        emocionDB.emocionPredominante = emocion_predominante[0] if emocion_predominante else None
        emocionDB.numImgProsesadas += 1
        emocionDB.save()

        return Response({
            "emocion_predicha": predicted_emotion,
            "confianza": round(confidence, 3)
        })
