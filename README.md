# Sistema de Detecção de Objetos Embarcado para Drone (ESP32-CAM + YOLOv5)

Solução de visão computacional em tempo real projetada para monitoramento aéreo e identificação de equipamentos e indícios associados a atividades irregulares em áreas de mata. O sistema combina captura de imagem embarcada via **ESP32-CAM** com inferência baseada em **YOLOv5s** em uma estação base Python.

## Arquitetura do Sistema

1. **Módulo Embarcado (`firmware/`):** A placa ESP32-CAM (modelo Ai-Thinker) conecta-se a uma rede Wi-Fi de 2.4 GHz, inicializa um servidor web HTTP e disponibiliza frames JPEG sob demanda em três resoluções, além de controlar o LED de flash integrado.
2. **Estação Base (`src/` + `model/`):** Um script Python consome o stream de imagens via requisições HTTP, executa a inferência com o modelo customizado (`best.pt`) e exibe em tempo real as detecções com *bounding boxes* e índices de confiança.

## Classes Detectadas (`best.pt`)

O modelo customizado foi treinado sobre a arquitetura **YOLOv5s** para reconhecer as seguintes 8 classes:

| ID | Classe | Descrição |
| :-: | :--- | :--- |
| 0 | `Motosserra` | Equipamento de corte motorizado |
| 1 | `Galão de Gasolina` | Recipiente de combustível |
| 2 | `Corrente grossa` | Correntes metálicas pesadas para tração/arraste |
| 3 | `Bote` | Embarcação inflável ou de pequeno porte |
| 4 | `Machado` | Ferramenta manual de corte |
| 5 | `Tronco de palmeira` | Madeira/palmito extraído |
| 6 | `Barraca` | Estrutura temporária de acampamento |
| 7 | `Walk-talk (rádio)` | Rádio comunicador portátil |

## Estrutura do Repositório

```text
├── firmware/
│   └── ESP32-CAM-DetectorObj/
│       └── ESP32-CAM-DetectorObj.ino   # Código-fonte do servidor HTTP na ESP32-CAM
├── model/
│   └── best.pt                         # Pesos treinados do modelo customizado (YOLOv5s)
├── src/
│   └── ReconheceObj.py                 # Script de captura de frames e detecção em tempo real
├── .gitignore
├── requirements.txt
└── README.md
```

## Pré-requisitos

* **Hardware:** Módulo ESP32-CAM (Ai-Thinker) + gravador FTDI USB-Serial.
* **Rede:** Roteador ou ponto de acesso Wi-Fi operando em **2.4 GHz** (a ESP32-CAM não possui suporte a redes 5 GHz).
* **Software:**
  * Arduino IDE com suporte às placas ESP32 e biblioteca `esp32cam` instalada.
  * Python 3.9 ou superior.

## Instalação e Execução

### 1. Gravação do Firmware (ESP32-CAM)

1. Abra o arquivo `firmware/ESP32-CAM-DetectorObj/ESP32-CAM-DetectorObj.ino` na Arduino IDE.
2. Insira as credenciais da sua rede Wi-Fi 2.4 GHz:
   ```cpp
   const char* WIFI_SSID = "seu_ssid";
   const char* WIFI_PASS = "sua_senha";
   ```
3. *(Opcional)* Ajuste a intensidade do LED de flash em `nivelBrilho` (0 a 100 — evite valores acima de 100 para não superaquecer o componente).
4. Selecione a placa **AI Thinker ESP32-CAM**, faça o upload e abra o **Monitor Serial** (`115200 baud`) para copiar o endereço IP atribuído ao dispositivo.

#### Endpoints Disponíveis na ESP32-CAM
* `http://<IP_ESP32>/cam-lo.jpg` — Resolução `320x240`
* `http://<IP_ESP32>/cam-mid.jpg` — Resolução `350x530`
* `http://<IP_ESP32>/cam-hi.jpg` — Resolução `800x600`

### 2. Execução da Detecção (Python)

1. Clone o repositório e instale as dependências:
   ```bash
   git clone [https://github.com/Davi-AI7/drone-object-detector.git](https://github.com/Davi-AI7/drone-object-detector.git)
   cd SEU-REPOSITORIO
   pip install -r requirements.txt
   ```
2. Atualize o endereço IP da câmera no arquivo `src/ReconheceObj.py` com o IP exibido no Monitor Serial da ESP32-CAM.
3. Execute o script:
   ```bash
   python src/ReconheceObj.py
   ```
4. Pressione a tecla **`q`** nas janelas de visualização para encerrar a execução.