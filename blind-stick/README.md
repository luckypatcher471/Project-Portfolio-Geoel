# Smart Assistive Blind Stick

## Overview
An Arduino-based assistive device designed to detect obstacles in close proximity using dual ultrasonic sensors and provide real-time audio alerts.

## Objective
To improve obstacle awareness for visually impaired individuals by detecting nearby objects and generating an audible warning signal.

## Hardware Components
- Arduino microcontroller
- Ultrasonic sensors (HC-SR04)
- Piezo buzzer
- Power supply

## System Logic
1. Two ultrasonic sensors continuously measure distance.
2. Distance is calculated using time-of-flight principle:
   
   Distance = Duration × 0.017

3. If either sensor detects an object within 10 cm:
   - A 1000 Hz tone is generated using the piezo buzzer.
4. If no obstacle is detected:
   - The buzzer remains off.

## Key Learning Outcomes
- Multi-sensor integration
- Real-time signal processing
- Threshold-based alert systems
- Embedded C programming in Arduino
- Hardware debugging and calibration

## Possible Improvements
- Variable alert intensity based on distance
- Vibration motor integration
- Battery efficiency optimization
