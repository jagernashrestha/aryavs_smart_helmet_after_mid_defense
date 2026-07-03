#ifndef CONFIG_H
#define CONFIG_H

// ---------- PIN CONFIGURATION (ESP32) ----------
#define GPS_RX      16
#define GPS_TX      17
#define GSM_RX      26  // SIM800L TX -> ESP32 GPIO26
#define GSM_TX      27  // SIM800L RX -> ESP32 GPIO27
#define MPU_SDA     21
#define MPU_SCL     22
#define BUZZER_PIN  5
#define CANCEL_BTN  4

// ---------- COMMUNICATION MODES ----------
#define USE_WIFI_HTTP true
#define USE_GPRS_HTTP false
#define USE_SMS_ALERT true

// ---------- WI-FI CONFIG ----------
#define WIFI_SSID         "Sumit House_2.4"
#define WIFI_PASSWORD     "Sumit123456"

// ---------- DEMO LED & SENSOR PINS ----------
#define RED_LED         12  // Fall/Alert active
#define GREEN_LED       13  // System powered
#define BLUE_LED        14  // GPS fix valid
#define YELLOW_LED      25  // Backend auth/login OK
#define IR_SENSOR_PIN   34  // Optional helmet-worn indicator (Input only)

// ---------- FALL DETECTION THRESHOLDS ----------
#define FALL_THRESHOLD    2.5f     // 2.5G reduces false alarms from bumps
#define NO_MOVE_TIME_MS   8000     // 8 seconds of no movement after impact = Fall Confirmed

// ---------- BLE CONFIG ----------
#define BLE_DEVICE_NAME   "SmartHelmet"
#define BLE_SERVICE_UUID  "0000FFE0-0000-1000-8000-00805F9B34FB"
#define BLE_CHAR_UUID     "0000FFE1-0000-1000-8000-00805F9B34FB"

// ---------- EMERGENCY CONTACT ----------
// Enter the phone number to receive SOS SMS
#define EMERGENCY_NUMBER  "+9779841240126"   

// ---------- SERVER CONFIG ----------
// Enter your backend's IPv4 address
#define SERVER_IP         "192.168.1.64"      
#define SERVER_PORT       8000
#define API_USERNAME      "rider1"     // Django username
#define API_PASSWORD      "rider123"   // Django password
#define DEVICE_ID         "helmet_001" // Unique ID for this helmet
#define DEVICE_SECRET     "smarthelmet-proto-secret-123" // Shared secret for device verification

// ---------- GSM / SIM CONFIG ----------
// Change to match your SIM provider APN
#define GSM_APN           "ncell"              

// ---------- TIMING ----------
#define GPS_SEND_INTERVAL_MS      20000UL    // GPS updates every 30s
#define SENSOR_SEND_INTERVAL_MS   10000UL    // Sensor updates every 10s
#define LOGIN_INTERVAL_MS         39600000UL // Server login refresh every 11 hours

#endif