title: Lightbox

author: Arya C. 

description: this project is to create a custom pixel display with speaker! The light should also should be able to adapt with the audio

created: 06/22/2025



# June 22

## 12AM -> 4AM: Research and Sketch (4 hours)

Another nighttime randevoux! A while ago I remember seeing this really cool bitmap display at Ikea which to my dismay I found they don't sell anymore. As it looked cool, I want to create somethign similar. 


### Objective

My objective is to create a 16x16 pixel display that is accompanied by a microphone, speaker, audio controls, and a knob that I can use to rotate between patterns. 

### Form

The form is going to be a 100mm black cube. I want the exterior to look minimalistic, as in if it was just a black cube with a pixel display on the front face and speaker on the top face. There should be "holes" on teh left and right faces as to allow for a more open audio landscape. The controls and power cable should ideally be hidden in the back. 


### Results from Research: BOM

Heres a basic BOM that I gathered from researching possible parts. This will be refined later

- Raspberry Pi Z2W
- HiVi B3N Speaker Module
- 256x LEDs
- Rotary Encoder
- 2x Buttons
- Mic Module
- Audio Amplifier
- Custom PCB
- 3D Printed Case


### Pretty Picture

I know that its been a lot of words so far, so here's a visual I sketched up to communicate my vision. 

![IMG_4877 2](https://github.com/user-attachments/assets/4e15a53c-c225-4a25-a675-7cb84f4d4f93)


## 1PM -> 4PM (3 hours)
For these 3 hours I went down a parts rabbithole! Here's an updated BOM

| Item                            | Qty |
|:--------------------------------|----:|
| Raspberry Pi Zero 2 W           |   1 |
| 40-pin Female Header            |   1 |
| WS2812B-3535 Addressable LED    | 256 |
| 330Ω Resistor (0603)            |   1 |
| 74AHCT125 (SOIC-14)             |   1 |
| 0.1µF Ceramic Capacitor (0603)  |  10 |
| 1000µF 6.3V Electrolytic Cap    |   4 |
| 10µF Ceramic Capacitor (0805)   |   4 |
| MAX98357A I²S Audio Amp         |   1 |
| HiVi B3N 3” 4Ω Speaker          |   1 |
| 100µF Capacitor (Audio)         |   1 |
| MAX9814 Microphone Module       |   1 |
| USB Audio Dongle                |   1 |
| EC11 Rotary Encoder with Button |   1 |
| Tactile Button (6x6mm)          |   2 |
| 10kΩ Resistor (0603)            |   5 |
| XT60 or 5.5mm Barrel Jack       |   1 |
| Polyfuse 6A                     |   1 |
| SMBJ5.0A TVS Diode              |   1 |
| High Current 5V 20A PSU         |   1 |
| JST-SH 6-pin Header             |   1 |
| M2.5 or M3 Brass Inserts        |   4 |
| 94mm x 94mm 2-layer PCB         |   1 |




