from pathlib import Path
import urllib.request
import cv2
import numpy as np
import torch

# Configurações da ESP32-CAM e do modelo
ESP32_IP = "192.168.7.51"  # Substitua pelo IP exibido no Monitor Serial
STREAM_URL = f"http://{ESP32_IP}/cam-hi.jpg"  # Opções: cam-lo.jpg, cam-mid.jpg, cam-hi.jpg
CONFIDENCE_THRESHOLD = 0.50

# Localiza model/best.pt independentemente da pasta de onde o terminal executar o script
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "best.pt"


def carregar_modelo(caminho_pesos: Path):
    if not caminho_pesos.exists():
        raise FileNotFoundError(f"Arquivo de pesos não encontrado em: {caminho_pesos}")

    modelo = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path=str(caminho_pesos),
        trust_repo=True,
    )
    modelo.conf = CONFIDENCE_THRESHOLD
    return modelo


def capturar_frame(url: str, timeout: float = 5.0):
    with urllib.request.urlopen(url, timeout=timeout) as resposta:
        img_bytes = np.asarray(bytearray(resposta.read()), dtype=np.uint8)
    return cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)


def main():
    print("Carregando modelo YOLOv5 customizado...")
    modelo = carregar_modelo(MODEL_PATH)
    print(f"Conectando à ESP32-CAM em {STREAM_URL} (pressione 'q' para sair)...")

    while True:
        try:
            frame_bgr = capturar_frame(STREAM_URL)
            if frame_bgr is None:
                continue

            # YOLOv5 espera entrada em RGB; OpenCV captura em BGR
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            resultados = modelo(frame_rgb)

            # Desenha as caixas delimitadoras e converte de volta para BGR
            frame_anotado_rgb = resultados.render()[0]
            frame_anotado_bgr = cv2.cvtColor(frame_anotado_rgb, cv2.COLOR_RGB2BGR)

            cv2.imshow("ESP32-CAM - Ao Vivo", frame_bgr)
            cv2.imshow("ESP32-CAM - Deteccao YOLOv5", frame_anotado_bgr)

        except Exception as erro:
            print(f"Erro na leitura do frame: {erro}")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()