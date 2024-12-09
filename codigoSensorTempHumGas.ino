#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <DHT.h>

#define DHTPIN D1       
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);

#define MQ3_PIN A0  

//#define LED_PIN D2

const char* ssid = "Batcaverna";    
const char* password = "EleBatiPalma101211";   

WiFiServer server(80); 

String header;

void setup() {
  Serial.begin(115200); 
  dht.begin();          

  //pinMode(LED_PIN, OUTPUT);
  //digitalWrite(LED_PIN, HIGH);
  
  Serial.println("Conectando ao Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
  server.begin(); 
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Cliente conectado!");
    String request = client.readStringUntil('\r');
    Serial.println(request);
    client.flush();

    // Leitura dos sensores
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int mq3_value = analogRead(MQ3_PIN);

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Erro ao ler o sensor DHT11.");
      temperature = -1; 
      humidity = -1;    
    }

    // Formatar os dados
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["temperature"] = temperature;
    jsonDoc["humidity"] = humidity;
    jsonDoc["gas"] = mq3_value;
    Serial.println(temperature);

    String jsonResponse;
    serializeJson(jsonDoc, jsonResponse);


    // Verifica se o cliente solicitou JSON
     if (request.indexOf("GET /json") >= 0) {
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: application/json");
      client.println("Connection: close");
      client.println();
      client.println(jsonResponse);
    } else {
      client.println("HTTP/1.1 404 Not Found");
      client.println("Connection: close");
      client.println();
      client.println("Página não encontrada");
    }

    //client.stop(); 
    Serial.println("Cliente desconectado.");
  }
}
