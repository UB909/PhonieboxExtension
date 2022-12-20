#include <Arduino.h>
#include <RotaryEncoder.h>

#define PIN_IN1 2
#define PIN_IN2 3

// A pointer to the dynamic created rotary encoder instance.
// This will be done in setup()
RotaryEncoder *encoder = nullptr;

// This interrupt routine will be called on any change of one of the input signals
void checkPosition()
{
  encoder->tick(); // just call tick() to check the state.
}



void setup()
{
  Serial.begin(115200);
  while (!Serial)
    ;
  Serial.println("InterruptRotator example for the RotaryEncoder library.");

  // setup the rotary encoder functionality

  // use FOUR3 mode when PIN_IN1, PIN_IN2 signals are always HIGH in latch position.
  // encoder = new RotaryEncoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::FOUR3);

  // use FOUR0 mode when PIN_IN1, PIN_IN2 signals are always LOW in latch position.
  // encoder = new RotaryEncoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::FOUR0);

  // use TWO03 mode when PIN_IN1, PIN_IN2 signals are both LOW or HIGH in latch position.
  encoder = new RotaryEncoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::TWO03);

  // register interrupt routine
  attachInterrupt(digitalPinToInterrupt(PIN_IN1), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN2), checkPosition, CHANGE);

  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
} // setup()


// Read the current position of the encoder and print out when changed.
void loop()
{
  static int pos = 0;

  encoder->tick(); // just call tick() to check the state.

  int newPos = encoder->getPosition();
  if (pos != newPos) {
    if(encoder->getDirection() == RotaryEncoder::Direction::CLOCKWISE) {
      Serial.print('+');
    }
    else {
      Serial.print('-');
    }
    pos = newPos;
  } 

  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    int incomingByte = Serial.read();

    // say what you got:
    digitalWrite(4, (incomingByte & 0x01) != 0);
    digitalWrite(5, (incomingByte & 0x02) != 0);
    digitalWrite(6, (incomingByte & 0x04) != 0);
    digitalWrite(7, (incomingByte & 0x08) != 0);
    digitalWrite(8, (incomingByte & 0x10) != 0);
    digitalWrite(9, (incomingByte & 0x20) != 0);
    digitalWrite(10, (incomingByte & 0x40) != 0);
    digitalWrite(11, (incomingByte & 0x80) != 0);
  }

} // loop ()


// To use other pins with Arduino UNO you can also use the ISR directly.
// Here is some code for A2 and A3 using ATMega168 ff. specific registers.

// Setup flags to activate the ISR PCINT1.
// You may have to modify the next 2 lines if using other pins than A2 and A3
//   PCICR |= (1 << PCIE1);    // This enables Pin Change Interrupt 1 that covers the Analog input pins or Port C.
//   PCMSK1 |= (1 << PCINT10) | (1 << PCINT11);  // This enables the interrupt for pin 2 and 3 of Port C.

// The Interrupt Service Routine for Pin Change Interrupt 1
// This routine will only be called on any signal change on A2 and A3.
// ISR(PCINT1_vect) {
//   encoder->tick(); // just call tick() to check the state.
// }

// The End