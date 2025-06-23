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
For these 3 hours I went down a parts rabbithole! Here's an updated BOM for the LED PCB

- 256x WS2812B LEDs (16x16 grid)
- 1x Raspberry Pi Zero 2W
- 1x Level Shifter (74AHCT125 single gate)
- 4x Bulk Capacitors (1000µF electrolytic - one per quadrant)
- 8-12x Decoupling Capacitors (0.1µF MLCC - distributed across grid)
- 1x High-Current Power Connector (XT60H-M)
- 1x Protection Fuse (6A Polyfuse)
- 1x TVS Diode (SMBJ5.0A for surge protection)
- 1x Data Resistor (330Ω for signal integrity)
- 1x 40-pin Female Header (Pi mounting)



