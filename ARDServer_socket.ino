

/********************************************************************
 * Programmed by Elliott Watson
 * March 5, 2018
 * 
 * Team: Amar Haqqi, Michelle Jagelid, Cameron Scott, Elliott Watson
 * 
 * This program is the basis for an Ardunio Uno-based temperature/humidity
 * station. It is part of a larger networked smart mirror project for
 * CS576: Networks at SDSU.
 * 
 * It uses libraries for the AM2321 heat sensor and the W5500 Ethernet
 * Shield; example code was consulted to help construction of this program
 * Also requirs the Adafruit Unifies Sensor library to be installed in
 * the Arduino.cc IDE (adafruit_sensor.h)
 * 
 */


// DHT (AM2321 with DHT22) Sensor Wiring Instructions:
// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor



#include "DHT.h" //AM2321 Heat Sensor library
#include "Ethernet2.h" // W5500 Ethernet Shield library

#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321


byte mac[] = {0xDE, 0xAD, 0xDE, 0xAF, 0xCA, 0xFA}; //just hard coded a mac address (not globally unique)
IPAddress ip(169,254,100,247); //working on LAN currently
EthernetServer server(50007); //unused port matched with client
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor.


void setup() {
  Serial.begin(9600);
  Ethernet.begin(mac, ip);
  server.begin();
  
  Serial.print("server is at: ");
  Serial.println(Ethernet.localIP());
  Serial.println("DHT22 initialized!");

  dht.begin();
}

void loop() {
  EthernetClient client = server.available();

  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.println(client.status());

  if (client){
    Serial.println("new client");
    //Serial.println("client is at: ");
    //Serial.print();

    while(client.connected()){
      Serial.println("client connected");
      if (client.available()){
        delay(2000);
        h = dht.readHumidity();
        // Read temperature as Celsius (the default)
        t = dht.readTemperature();
        // Read temperature as Fahrenheit (isFahrenheit = true)
        f = dht.readTemperature(true);
        hif = dht.computeHeatIndex(f, h);

        Serial.println("client available");
        char c = '\0';
        c = client.read();
        Serial.write(c);

        if (c == 'v'){
          client.println(f);
          client.println(t);
          client.println(h);
          client.println(hif);
        }
       
        //client.println(hic);
        
        
      }
      //client.println("Recieved message: success");
      //client.println("Temperature in Farenheit: " + f);
      //client.println(f);
      //client.println(h);
    }
    
    Serial.println("client disconnected");
  }
  client.stop();
  
  //Serial lines like these just print to the Arduino.cc IDE's serial
  //monitor for testing purposes; we may want to comment this chunk out
  //eventually

  
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.print(" *F\t");
  Serial.print("Heat index: ");
  Serial.print(hic);
  Serial.print(" *C ");
  Serial.print(hif);
  Serial.println(" *F");
  

}
