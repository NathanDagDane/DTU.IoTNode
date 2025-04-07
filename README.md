<div align="center">
  <h2>Local Web Server + API on Huzzah32 Board</h2>
  <a href="">
    <img src="https://github.com/user-attachments/assets/e21f2d45-6775-48d8-bf8b-9b1cb99d22e5" alt="Logo" height="80">
  </a>
  <h3>For DTU Cyber Systems Intro</h3>
</div>

This project uses an `Adafruit Feather Huzzah32 – ESP32 WiFi` board, for which the pins and specifications can be found [here](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts).  
The pins used in the code refer to our setup with the following connections:

<div align="center">
  
|      Pin      |     IN/OUT     |     Connection     |
|:-----------------|:-------------------:|:-------------------:|
| A4 (34)|    IN     |    Potentiometer     |
</div>

When the server is started, the local site can be accessed via `192.168.4.1:80`.
