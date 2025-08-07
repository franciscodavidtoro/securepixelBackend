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
    Devuelve una respuesta por línea, en el mismo orden. Solo texto, sin numeración ni comentarios.
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
