import time
import paho.mqtt.client as mqtt
import serial

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================
PORTA_SERIAL = 'COM5'              # Ajustar conforme a porta do Arduino do aluno
BAUD_RATE = 9600
BROKER_MQTT = 'broker.hivemq.com'  
PORTA_MQTT = 1883                  # Porta padrão para MQTT estável no Python
TOPICO = 'andrya_exclusivo/arduino' 

# ==========================================
# 2. CONEXÃO HARDWARE (ARDUINO)
# ==========================================
try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2) # Tempo necessário para o Arduino reiniciar após abrir a serial
    print(f"[HARDWARE] Conectado com sucesso na porta {PORTA_SERIAL}!")
except Exception as e:
    print(f"[ERRO HARDWARE] Falha ao conectar na {PORTA_SERIAL}: {e}")
    exit()

# ==========================================
# 3. FUNÇÕES DE CALLBACK DO MQTT
# ==========================================

# Executada automaticamente quando o Python conecta ao Broker
def ao_conectar(client, userdata, flags, razão_retorno, properties=None):
    if razão_retorno == 0:
        print("\n" + "="*40)
        print(" [MQTT] CONECTADO COM SUCESSO AO BROKER! ")
        print("="*40)
        # É vital se inscrever no tópico LOGO APÓS a conexão ser estabelecida
        client.subscribe(TOPICO)
        print(f"[MQTT] Inscrito com sucesso no tópico: {TOPICO}")
        print("[STATUS] Aguardando comandos vindos do site HiveMQ...")
    else:
        print(f"[ERRO MQTT] Falha na conexão. Código de retorno: {razão_retorno}")

# Executada automaticamente toda vez que chega uma mensagem no tópico inscrito
def ao_receber_mensagem(client, userdata, msg):
    # Decodifica os bytes recebidos para texto limpo
    comando = msg.payload.decode('utf-8').strip()
    
    if not comando:
        return 

    print(f"\n[NUVEM] Mensagem recebida no tópico: '{comando}'")
    
    # Validação do comando antes de enviar para o hardware
    if comando == '1':
        arduino.write(b'1') 
        print("[HARDWARE] Comando enviado ao Arduino: LIGAR LED")
    elif comando == '0':
        arduino.write(b'0') 
        print("[HARDWARE] Comando enviado ao Arduino: DESLIGAR LED")
    else:
        print(f"[AVISO] Comando inválido ('{comando}'). Use apenas '1' ou '0'.")

# =========================================
# 4. INICIALIZAÇÃO DO CLIENTE MQTT (Paho v2.x)
# ==========================================

def ao_receber_mensagem(client, userdata, msg):
    # Decodifica os bytes recebidos para texto limpo
    comando = msg.payload.decode('utf-8').strip()
    
    if not comando:
        return 

    print(f"\n[NUVEM] Mensagem recebida no tópico: '{comando}'")
    
    # Validação do comando antes de enviar para o hardware
    if comando == '1':
        arduino.write(b'1') 
        print("[HARDWARE] Comando enviado ao Arduino: LIGAR LED")
    elif comando == '0':
        arduino.write(b'0') 
        print("[HARDWARE] Comando enviado ao Arduino: DESLIGAR LED")
    else:
        print(f"[AVISO] Comando inválido ('{comando}'). Use apenas '1' ou '0'.")

# ==========================================
# 4. INICIALIZAÇÃO DO CLIENTE MQTT (Paho v2.x)
# ==========================================
# ATENÇÃO PROFESSOR: É aqui que resolvemos o travamento da biblioteca v2.x!
# Usamos explicitamente o padrão 'VERSION2' exigido pelas versões recentes do Python.
cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Vincula as funções de controle criadas acima aos eventos da biblioteca
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem

print(f"[STATUS] Tentando conectar ao broker em {BROKER_MQTT}:{PORTA_MQTT}...")
cliente.connect(BROKER_MQTT, PORTA_MQTT, 60)

# Inicia o loop infinito que escuta a rede em segundo plano
try:
    cliente.loop_forever()
except KeyboardInterrupt:
    print("\n[STATUS] Encerrando o programa pelo usuário...")
    arduino.close()
    print("[STATUS] Porta serial fechada com segurança.")

