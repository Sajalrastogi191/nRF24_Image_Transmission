#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

String inputString = "";
bool receiving = false;

void setup() {
  Serial.begin(115200);
  radio.begin();
  radio.setChannel(76);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_LOW);
  radio.openWritingPipe(address);
  radio.stopListening();
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'S') {
      receiving = true;
      inputString = "";
    } else if (receiving) {
      inputString += c;
      if (inputString.length() >= 32) {
        sendChunk(inputString);
        inputString = "";
      }
    }
  }
}

void sendChunk(String chunk) {
  char buffer[33];
  chunk.toCharArray(buffer, 33);
  radio.write(&buffer, 32);
  delay(5);
}