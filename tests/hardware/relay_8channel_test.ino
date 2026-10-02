#include <Arduino.h>
#include <esp_system.h>

RTC_DATA_ATTR uint32_t bootCounter = 0;

constexpr uint8_t RELAY_PINS[] = {
  13,
  14,
  18,
  19,
  23,
  25,
  26,
  27
};

constexpr size_t RELAY_COUNT =
    sizeof(RELAY_PINS) / sizeof(RELAY_PINS[0]);

constexpr uint8_t RELAY_ON = LOW;
constexpr uint8_t RELAY_OFF = HIGH;

constexpr unsigned long ON_DURATION_MS = 1000;
constexpr unsigned long BETWEEN_CHANNELS_MS = 500;

void setAllRelaysOff() {
  for (size_t index = 0; index < RELAY_COUNT; ++index) {
    digitalWrite(RELAY_PINS[index], RELAY_OFF);
  }
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  ++bootCounter;

  Serial.println();
  Serial.println("=== CyberHunter Stage 16 Relay Test ===");
  Serial.printf("BOOT_COUNT=%lu\n", bootCounter);
  Serial.printf(
      "RESET_REASON=%d\n",
      static_cast<int>(esp_reset_reason())
  );
  Serial.println("ACTIVE_LEVEL=LOW");
  Serial.println("INACTIVE_LEVEL=HIGH");
  Serial.printf("CHANNEL_COUNT=%u\n", RELAY_COUNT);

  for (size_t index = 0; index < RELAY_COUNT; ++index) {
    digitalWrite(RELAY_PINS[index], RELAY_OFF);
    pinMode(RELAY_PINS[index], OUTPUT);

    Serial.printf(
        "INITIALIZED CHANNEL=%u GPIO=%u STATE=OFF\n",
        static_cast<unsigned int>(index + 1),
        RELAY_PINS[index]
    );
  }

  delay(1000);

  Serial.println();
  Serial.println("TEST_START");

  for (size_t index = 0; index < RELAY_COUNT; ++index) {
    const uint8_t channel = index + 1;
    const uint8_t pin = RELAY_PINS[index];

    Serial.printf(
        "CHANNEL=%u GPIO=%u COMMAND=LOW EXPECTED=ON\n",
        channel,
        pin
    );

    digitalWrite(pin, RELAY_ON);
    delay(ON_DURATION_MS);

    Serial.printf(
        "CHANNEL=%u GPIO=%u READBACK=%s\n",
        channel,
        pin,
        digitalRead(pin) == RELAY_ON ? "LOW" : "UNEXPECTED"
    );

    digitalWrite(pin, RELAY_OFF);

    Serial.printf(
        "CHANNEL=%u GPIO=%u COMMAND=HIGH EXPECTED=OFF\n",
        channel,
        pin
    );

    delay(BETWEEN_CHANNELS_MS);
  }

  setAllRelaysOff();

  bool allRelaysOff = true;

  for (size_t index = 0; index < RELAY_COUNT; ++index) {
    if (digitalRead(RELAY_PINS[index]) != RELAY_OFF) {
      allRelaysOff = false;
    }
  }

  Serial.println();
  Serial.printf(
      "FINAL_OUTPUT_STATE=%s\n",
      allRelaysOff ? "ALL_OFF" : "FAILED"
  );

  if (allRelaysOff) {
    Serial.println("TEST_RESULT=PASS");
  } else {
    Serial.println("TEST_RESULT=FAIL");
  }

  Serial.println("TEST_COMPLETE");
}

void loop() {
  delay(1000);
}
