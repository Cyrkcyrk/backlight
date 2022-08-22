//#define VERBOSE

#include <EEPROM.h>
#define EEPROM_SIZE 353
char ssid[33];
char password[64];
char raw_data_src[256];
int len_raw_data_src;

#include <WiFi.h>
#include <DNSServer.h>
#include "ESPAsyncWebServer.h"

#define DNS_PORT 53
IPAddress apIP(8,8,4,4); // The default android DNS
DNSServer dnsServer;
//WebServer server(80);
AsyncWebServer server(80);
#include <HTTPClient.h>

#include <FastLED.h>
#define NUM_LEDS 118
#define DATA_PIN 32
CRGB leds[NUM_LEDS];
int numLed = 0;

bool startup;

void update_eeprom(int adr, int val) {
  int tmp;
  tmp = EEPROM.read(adr);
  if (tmp != val) {
    EEPROM.write(adr, val);  
  }  
}

void tout_eteindre() {
  int i;
  i = -1;
  while (++i < NUM_LEDS) {
    leds[i] = CRGB(0,0,0);
  }
}

int compteur;
double now;

void setup() {
  compteur = 0;
  now = 0;
  #if defined(VERBOSE) || defined(VERBOSE_CAPACITIVE)
    Serial.begin(115200);
    delay(1000);
    Serial.println("Lixie starting");
  #endif
  startup = true;

  EEPROM.begin(EEPROM_SIZE);
  
  for (int i = 0; i < 33; i++) {
      ssid[i] = EEPROM.read(0 + i);
  }
  for (int i = 0; i < 64; i++) {
      password[i] = EEPROM.read(34 + i);
  }
  for (int i = 0; i < 256; i++) {
      raw_data_src[i] = EEPROM.read(98 + i);
  }
  len_raw_data_src = strlen(raw_data_src);

  #ifdef VERBOSE
    Serial.printf("SSID: %s\nPSWD: %s\nRAWD: %s\n", ssid, password, raw_data_src);
  #endif
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
  //FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);  // GRB ordering is typical
  pinMode(DATA_PIN, OUTPUT);
  
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP("Backlight Cyrille", "Colombes/18");
  //WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  
  // if DNSServer is started with "*" for domain name, it will reply with
  // provided IP to all DNS request
  dnsServer.start(DNS_PORT, "*", WiFi.softAPIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    int paramsNr = request->params();
    for(int i = 0; i < paramsNr; i++){
        AsyncWebParameter* p = request->getParam(i);
        char _name[33];
        char _value[256];
        p->name().toCharArray(_name, 31);
        p->value().toCharArray(_value, 255);
        _name[32] = '\0';
        _value[255] = '\0';
        
        if (!strcmp(_name, "SSID")) {
          if (strncmp(_value, ssid, 32)) {
            #ifdef VERBOSE
              Serial.printf("Updating EEPROM for SSID \n%s\n%s\n-----\n", ssid, _value);
            #endif
            strncpy(ssid, _value, 32);
            ssid[32] = '\0';
            for (int i = 0; i < 33; i++) {
              update_eeprom(0 + i, ssid[i]);
            }
            EEPROM.commit();
          }
        }
        else if (! strcmp(_name, "PSWD")) {
          if (strncmp(_value, password, 63)) {
            #ifdef VERBOSE
              Serial.printf("Updating EEPROM for PASSWORD \n%s\n%s\n-----\n", password, _value);
            #endif
            strncpy(password, _value, 63);
            password[63] = '\0';
            for (int i = 0; i < 64; i++) {
              update_eeprom(34 + i, password[i]);
            }
            EEPROM.commit();
          }
        }
        else if (! strcmp(_name, "RAWDATA")) {
          if (strncmp(_value, raw_data_src, 63)) {
            #ifdef VERBOSE
              Serial.printf("Updating EEPROM for RAWDATA \n%s\n%s\n-----\n", raw_data_src, _value);
            #endif
            strncpy(raw_data_src, _value, 255);
            raw_data_src[255] = '\0';
            for (int i = 0; i < 256; i++) {
              update_eeprom(98 + i, raw_data_src[i]);
            }
            EEPROM.commit();
            len_raw_data_src = strlen(raw_data_src);
          }
        }
        #ifdef VERBOSE
          Serial.print("Param name: ");
          Serial.println(_name);
          Serial.print("Param value: ");
          Serial.println(_value);
          Serial.println("------");
        #endif
    }
    AsyncResponseStream *response = request->beginResponseStream("text/html");
    response->printf("<title>LixieClock</title><h1>Lixie Clock</h1>");
    response->printf("<form>SSID : <input type='text' name='SSID' value='%s'/><br>", ssid);
    response->printf("PASSWORD : <input type='text' name='PSWD' value='%s'/><br>", password);
    response->printf("RAW DATA SOURCE : <input type='text' name='RAWDATA' value='%s'/><br>", raw_data_src);
    response->printf("<input type='submit'></form>");
    request->send(response);
  });
  server.on("/off", HTTP_GET, [](AsyncWebServerRequest *request) {
    tout_eteindre();
    FastLED.show();
    #ifdef VERBOSE
      Serial.println("Turning off everything");
    #endif
    AsyncResponseStream *response = request->beginResponseStream("text/html");
    response->printf("ok [%d]", millis());
    request->send(response);
  });
  server.on("/set", HTTP_GET, [](AsyncWebServerRequest *request) {
    int paramsNr = request->params();
    
    int num, r, g, b;
    for(int i = 0; i < paramsNr; i++){
        AsyncWebParameter* p = request->getParam(i);
        char _name[33];
        char _value[256];
        char *v;
        p->name().toCharArray(_name, 31);
        p->value().toCharArray(_value, 255);
        _name[32] = '\0';
        _value[255] = '\0';
        v = _value;
        
        num = (int)strtol(_name, NULL, 10);
        r = (int)strtol(v, &v, 10);
        v++;
        g = (int)strtol(v, &v, 10);
        v++;
        b = (int)strtol(v, &v, 10);

        if (num > 0 && num < NUM_LEDS) {
          leds[num] = CRGB(r,g,b);
        }
        #ifdef VERBOSE
          Serial.print("Param name: ");
          Serial.println(_name);
          Serial.print("Param value: ");
          Serial.println(_value);
          Serial.println("------");
          
          Serial.print("num:");
          Serial.print(num);
          Serial.print("r:");
          Serial.print(r);
          Serial.print(" g:");
          Serial.print(g);
          Serial.print(" b:");
          Serial.print(b);
          Serial.println("\n------");
        #endif
    }
    FastLED.show();
    AsyncResponseStream *response = request->beginResponseStream("text/html");
    response->printf("ok [%d]", millis());
    request->send(response);
  });
  server.begin();

  #ifdef VERBOSE
    Serial.printf("Connecting to |%s| with password |%s| ", ssid, password);
  #endif
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED && millis() < 60000) {
    delay(500);
    #ifdef VERBOSE
      Serial.print(".");
    #endif
  }
  if(WiFi.status() != WL_CONNECTED) {
    #ifdef VERBOSE
      Serial.println("Not connected");
    #endif
  }
  else {
    #ifdef VERBOSE
      Serial.println("Connected");
    #endif
  }
}

void loop() {
  if (startup) {
    dnsServer.processNextRequest();
    
    if (millis() > 300000) {
      WiFi.softAPdisconnect (true);
      dnsServer.stop();
      startup = false;
    }
  }
/*
  if (now < millis()) {
      Serial.println(compteur % NUM_LEDS);
      now = millis() + 500;
      tout_eteindre();
      leds[compteur++ % NUM_LEDS] = CRGB(255, 0, 255);
      FastLED.show();
  }
 */
}
