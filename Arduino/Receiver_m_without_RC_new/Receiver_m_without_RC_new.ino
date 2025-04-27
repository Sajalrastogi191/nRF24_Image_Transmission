#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setChannel(76);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_LOW);
  radio.openReadingPipe(0, address);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    char buffer[33] = {0};
    radio.read(&buffer, 32);
    Serial.print(buffer);
  }
}