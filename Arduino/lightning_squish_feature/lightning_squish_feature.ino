/*
 * 16-223: Reach for the Sky by Jen Kwang and Jessica Lew
 * Uses flex sensor inside arificial cloud and modulates LEDs to produce a pattern when squished.
 *
 * Code for LEDs modified from tutorial found here:
 * https://randomnerdtutorials.com/guide-for-ws2812b-addressable-rgb-led-strip-with-arduino/
 */

#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    96
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 1000

const int flex_count_thresh = 30;

unsigned long time;

const int FLEX_PIN = A1;

int value; //cur value of flex sensor
int sec;
int flex_init = 0;
int count = 0; //loop counter used to calibrate flex sensor/time the lightning

CRGBPalette16 currentPalette;
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;


void setup() {
    Serial.begin(9600);
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;
}


void loop()
{
  FastLED.clear ();
    if (flex_init == 0)
  {
    delay(10);
   flex_init = analogRead(FLEX_PIN); 
  }

  Serial.print("  Time: ");
  time = millis();
  Serial.println(time);

  Serial.print("  Sec var: ");
  
  sec = time / 1000;
  Serial.println(sec);
  
  value = analogRead(FLEX_PIN); 
  Serial.print("          flex value:  ");
  Serial.println(value);  
  Serial.print("FLEX INIT:    ");
  Serial.print(flex_init);
  Serial.print("    ");

  // if squished, turn on LED
  if (flex_init - 30 > value || flex_init + 30 < value)
  {
    Serial.print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~flex init value: ");
    Serial.print(flex_init);
    Serial.print("__________flex cur value: ");
    Serial.print(value);
    count = count + 1;

    //turn on led color depending on count
    /////

    ChangePalettePeriodically();
    
    static uint8_t startIndex = 0;
    startIndex = startIndex + 50; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    FastLED.show();
    FastLED.delay(100 / UPDATES_PER_SECOND);

    // if flex sensor permanently bent out of shape, reset its neutral state value.
    if (count >= flex_count_thresh)
    {
      flex_init = value;
      count = 0;
    }

  }

  // if not squished, update the flex neutral state value.
  else
  {
    flex_init = value;
    for (int i = 0; i < NUM_LEDS; i++){
      leds[i] = CRGB::White;
    }
    FastLED.show();
  }
}

void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}

void ChangePalettePeriodically()
{
  currentPalette = CRGBPalette16(CRGB::LightBlue, CRGB::Aqua,  CRGB::Aqua);;  currentBlending = LINEARBLEND;
    
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
    CRGB purple = CHSV( HUE_PURPLE, 255, 255);
    CRGB green  = CHSV( HUE_BLUE, 255, 255);
    CRGB black  = CRGB::Black;
    
    currentPalette = CRGBPalette16(
                                   green,  green,  black,  black,
                                   purple, purple, black,  black,
                                   green,  green,  black,  black,
                                   purple, purple, black,  black );
}
