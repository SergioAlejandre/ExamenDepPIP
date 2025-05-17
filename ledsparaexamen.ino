
int fotoR = A0;
int leds[] = {3, 4}; 

void setup() {
  for (int i = 0; i < 2; i++) {
    pinMode(leds[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  int valorfotoR = analogRead(fotoR);
  Serial.println(valorfotoR); 

  // Apaga todos los LEDs
  for (int i = 0; i < 2; i++) {
    digitalWrite(leds[i], LOW);
  }

  
  if (valorfotoR < 400) digitalWrite(leds[0], HIGH);
  if (valorfotoR < 300) digitalWrite(leds[1], HIGH);
  
  delay(100);
}
