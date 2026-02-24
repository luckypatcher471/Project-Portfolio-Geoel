# Ultrasonic Presence-Based Study Timer

## Overview
An embedded system designed to monitor user presence using ultrasonic distance sensing and provide visual/audio feedback based on proximity.

## Objective
To create a basic accountability mechanism during study sessions by detecting whether the user remains within a predefined range.

## Hardware Components
- Arduino microcontroller
- Ultrasonic sensor (HC-SR04)
- LED indicator
- Piezo buzzer

## Working Principle
1. The ultrasonic sensor emits a pulse.
2. Echo duration is measured using time-of-flight principle.
3. Distance is calculated:

   Distance (cm) = Duration × 0.034 / 2

4. If the measured distance is below 40 cm:
   - LED and buzzer are activated.
5. Otherwise:
   - Outputs remain off.

## Key Learning Outcomes
- Distance measurement using ultrasonic sensors
- Real-time threshold-based control
- Basic embedded signal processing
- Serial monitoring for debugging

## Future Improvements
- Timer-based study session tracking
- Data logging for performance monitoring
- Adjustable threshold configuration
