#include <WiFi.h>
void setup() {
  // put your setup code here, to run once:
  char *ssid = "esp32";
  char *pass = "12345678";
  Serial.begin(9600);
  WiFi.softAP(ssid, pass,8`,0,10);
  Serial.print("\n WIFI接入ip：");
  Serial.print(WiFi.softAPIP());
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
