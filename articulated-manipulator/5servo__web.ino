#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>
#include <Servo.h>

const char* ssid = "Ijjadhi AY";
const char* password = "Nintename";

AsyncWebServer server(80);
Servo servos[5];
int servoPins[5] = {D5, D1, D6, D3, D4}; 
int minAngles[5] = {40, 40, 20, 20, 40};
int maxAngles[5] = {150, 170, 160, 170, 150};
int lastAngles[5] = {90, 90, 90, 90, 90}; // Store last angles to avoid redundant updates

void setup() {
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    WiFi.setSleepMode(WIFI_NONE_SLEEP);  // Prevent WiFi sleep to reduce lag
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(200);
        Serial.print(".");
    }

    Serial.println("\nConnected to WiFi!");
    Serial.print("ESP IP Address: ");
    Serial.println(WiFi.localIP());

    for (int i = 0; i < 5; i++) {
        servos[i].attach(servoPins[i]);
        servos[i].write(lastAngles[i]);
    }

    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
        request->send(200, "text/html", R"rawliteral(
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>ESP8266 Servo Control</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
                    body { font-family: 'Orbitron', sans-serif; text-align: center; background: #0f0f0f; color: #0ff; padding: 20px; }
                    h1 { text-shadow: 0px 0px 10px #0ff; }
                    .container { max-width: 500px; margin: auto; padding: 20px; background: rgba(0, 255, 255, 0.1); border-radius: 10px; box-shadow: 0px 0px 10px #0ff; }
                    .slider-container { margin: 10px 0; padding: 10px; background: rgba(0, 255, 255, 0.2); border-radius: 10px; }
                    input[type=range] { width: 90%; -webkit-appearance: none; background: transparent; }
                    input[type=range]::-webkit-slider-runnable-track { height: 8px; background: #0ff; border-radius: 5px; }
                    input[type=range]::-webkit-slider-thumb { height: 20px; width: 20px; background: #ff0; border-radius: 50%; cursor: pointer; }
                    .status { color: #fff; margin-top: 10px; }
                </style>
            </head>
            <body>
                <h1>ESP8266 Servo Control 🚀</h1>
                <h3 class="status">Connected to WiFi</h3>
                <div class="container">
                    <div class="slider-container">
                        <h3>Servo 1 (D5): <span id="angle0">90</span>°</h3>
                        <input type="range" min="40" max="150" value="90" id="slider0" oninput="updateServo(0, this.value)">
                    </div>
                    <div class="slider-container">
                        <h3>Servo 2 (D1): <span id="angle1">90</span>°</h3>
                        <input type="range" min="40" max="170" value="90" id="slider1" oninput="updateServo(1, this.value)">
                    </div>
                    <div class="slider-container">
                        <h3>Servo 3 (D6): <span id="angle2">90</span>°</h3>
                        <input type="range" min="20" max="160" value="90" id="slider2" oninput="updateServo(2, this.value)">
                    </div>
                    <div class="slider-container">
                        <h3>Servo 4 (D3): <span id="angle3">90</span>°</h3>
                        <input type="range" min="20" max="170" value="90" id="slider3" oninput="updateServo(3, this.value)">
                    </div>
                    <div class="slider-container">
                        <h3>Servo 5 (D4): <span id="angle4">90</span>°</h3>
                        <input type="range" min="40" max="150" value="90" id="slider4" oninput="updateServo(4, this.value)">
                    </div>
                </div>
                <script>
                    function updateServo(id, value) {
                        document.getElementById("angle" + id).innerText = value;
                        fetch(`/slider?id=${id}&value=${value}`);
                    }
                </script>
            </body>
            </html>
        )rawliteral");
    });

    server.on("/slider", HTTP_GET, [](AsyncWebServerRequest *request){
        if (request->hasParam("id") && request->hasParam("value")) {
            int id = request->getParam("id")->value().toInt();
            int angle = request->getParam("value")->value().toInt();

            if (id >= 0 && id < 5) {
                if (angle < minAngles[id]) angle = minAngles[id];
                if (angle > maxAngles[id]) angle = maxAngles[id];

                if (lastAngles[id] != angle) {  // Only update if angle changes
                    servos[id].write(angle);
                    lastAngles[id] = angle;
                    Serial.printf("Servo %d Position: %d°\n", id + 1, angle);
                }
            }
        }
        request->send(200, "text/plain", "OK");
    });

    server.begin();
    Serial.println("Web Server Started");
}

void loop() {
    // Nothing needed in loop since AsyncWebServer handles everything
}
