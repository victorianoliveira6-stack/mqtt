// Pino do LED integrado do Arduino
const int pinoLED = 13; 

void setup() {
  // Inicia a comunicação serial na mesma velocidade do Python (9600)
  Serial.begin(9600); 
  
  // Configura o pino 13 como saída
  pinMode(pinoLED, OUTPUT); 
  
  // Garante que o LED comece apagado
  digitalWrite(pinoLED, LOW); 
}

void loop() {
  // Verifica se chegou alguma mensagem vinda do Python pelo cabo USB
  if (Serial.available() > 0) {
    // Lê o caractere recebido
    char comando = Serial.read(); 
    
    // Se receber o comando para ligar (ex: '1' ou 'L')
    if (comando == '1' || comando == 'L' || comando == 'l') {
      digitalWrite(pinoLED, HIGH);
      Serial.println("LED Ligado!");
    } 
    // Se receber o comando para desligar (ex: '0' ou 'D')
    else if (comando == '0' || comando == 'D' || comando == 'd') {
      digitalWrite(pinoLED, LOW);
      Serial.println("LED Apagado!");
    }
  }
}
