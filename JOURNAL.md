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

| Component                | Qty  | Unit Cost | Total   |
|--------------------------|------|-----------|---------|
| SK6812-Mini-E                  | 256  | $0.12     | $30.72  |
| PCB (2-layer heavy copper)| 1    | $8.00     | $8.00   |
| Pi Zero 2W               | 1    | $15.00    | $15.00  |
| 74AHCT125                | 1    | $0.50     | $0.50   |
| 1000µF EEU-FR1A102         | 4    | $0.75     | $3.00   |
| 0.1µF MLCCs        | 12   | $0.05     | $0.60   |
| XT60H-M connector        | 1    | $2.00     | $2.00   |
| 6A Polyfuse              | 1    | $0.30     | $0.30   |
| SMBJ5.0A TVS             | 1    | $0.40     | $0.40   |
| 40-pin header            | 1    | $1.50     | $1.50   |
| Other components         | --   | --        | $3.00   |
| **Total**               |      |           | **~$65** |


## 10PM->12AM (2 hours)
I was looking around KiCad docs and found that besides flat sheets, there's another layout called Heirarichal Style which is akin to object oriented programing so I spent hte last 2 hours going down that rabbit hole! I'm going to try to implement it in this project instead of the flat sheet style I used for my Hackpad project (also on github--you should totally check it out). On to making the schematic!

# June 23 (7 hours)

## 12AM -> 7AM

Currently making the schematic! 

5:39AM -- here's a quick update screenshot for y'all 


<img width="749" alt="Screenshot 2025-06-23 at 5 39 40 AM" src="https://github.com/user-attachments/assets/1f92c7af-fbff-451b-97c4-f45826a92536" />

will resume later, sleepy


# June 26 ( 0 hours)

So I started working on a instant camera project and really liked learning how to code the firmware. So as of now, I am shelving this project. Hopefully I can get to this later. It's been a blast learning more about LEDs but I feel I want to creaet something actually usable that will help me with everyday life. Till next time, Arya out. 




