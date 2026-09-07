import json
import os

class ArchivoServicio:
    @staticmethod
    def guardar_json(ruta: str, datos: list):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @staticmethod
    def cargar_json(ruta: str) -> list:
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []