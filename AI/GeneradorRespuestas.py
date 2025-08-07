import openai
from openai import OpenAI

client = OpenAI(api_key="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")

def completar_respuestas_ia_con_contexto(pregunta_texto, dificultad, respuestas_existentes, instrucciones_ia):
  
    

    contexto = "\n".join([
        f"- {r['texto']} [{'✔' if r['corecta'] else '✖'}]"
        for r in respuestas_existentes
    ])

    instrucciones = "\n".join([
        f"{i+1}. {instr['texto']} [{'✔' if instr['corecta'] else '✖'}]"
        for i, instr in enumerate(instrucciones_ia)
    ])

    prompt = f"""
    Pregunta: {pregunta_texto}
    Dificultad: {dificultad} (0=fácil, 10=difícil)

    Ya existen estas respuestas:
    {contexto}

    Ahora genera nuevas respuestas según estas instrucciones:

    {instrucciones}

    La dificultad es {dificultad}, así que ajusta la sutileza o claridad de los distractores y respuestas correctas según ese nivel.
    Devuelve una respuesta por línea, en el mismo orden. Solo texto, sin numeración ni comentarios ni marcas de corecto o incorecto.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Eres un generador experto de respuestas para preguntas de opción múltiple. Ajusta el nivel de dificultad de las respuestas generadas según el valor numérico."},
            {"role": "user", "content": prompt}
        ]
    )

    texto = response.choices[0].message.content
    return [line.strip("- ").strip() for line in texto.splitlines() if line.strip()]
