# SmartHelmetX Demo Checklist & Setup Guide

This document ensures that the prototype is fully aligned and ready for a smooth demonstration.

## 1. Environment & Setup Consistency
Before starting the demo, verify that all components are using the exact same credentials and identifiers.

- **Prototype User**: `rider1`
- **Prototype Password**: `rider123`
- **Device ID**: `helmet_001`
- **Device Secret**: `smarthelmet-proto-secret-123`

### Run Database Seed
To guarantee the database is in the perfect state for the demo:
```bash
cd backend
python manage.py seed_data --reset
```
*This creates the `admin` user, the `rider1` prototype user, dummy riders, and links `helmet_001` to `rider1`.*

## 2. Startup Checklist
Run these in separate terminal windows:

- [ ] **Backend**:
  ```bash
  cd backend
  python manage.py runserver 0.0.0.0:8000
  ```
- [ ] **Frontend**:
  ```bash
  cd frontend
  npm run dev
  ```
- [ ] **Hardware**:
  - Connect the ESP32 to power.
  - Open the Serial Monitor (115200 baud).
- [ ] **Hardware Simulator (Fallback)**:
  - If hardware is not available, you can simulate a helmet in a new terminal:
  ```bash
  cd backend
  python manage.py simulate
  ```

## 3. Core Functionality Checklist
Verify each of these flows works flawlessly:

### A. Web Application (Frontend & Backend)
- [ ] **Login**: Can successfully log in as `rider1` (password: `rider123`).
- [ ] **Rider Dashboard**: Loads correctly, displays "Waiting for live sensor data...", and map centers gracefully.
- [ ] **Admin Dashboard**: Log out and log back in as `admin` (password: `admin123`). Verify you can view the system overview and the detail view for `rider1`.
- [ ] **WebSocket Real-time**: When the device sends data (or using the simulator), the charts and map on the Dashboard update instantly without a page refresh.

### B. Hardware (Firmware)
Watch the Serial Monitor to verify:
- [ ] **Firmware Login**: You see `[AUTH] Login OK`.
- [ ] **Device Config Fetch**: You see `[CONFIG] Updated fall threshold`. (Confirms HTTP & device verification is working).
- [ ] **Sensor Upload**: You see `[SENSOR] Sent OK` every 10 seconds.
- [ ] **GPS Upload**: You see `[GPS] Sent OK` every 30 seconds.

### C. Alerts & SOS Flow
- [ ] **Web SOS**: Clicking the "SOS" button in the web dashboard successfully creates an alert.
- [ ] **Hardware Fall/SOS**: 
  1. Shake the helmet hard to trigger the MPU6050.
  2. Hold the helmet perfectly still for 2 seconds (Stillness Confirmation).
  3. Wait for the 8-second cancel window to expire (Buzzer will sound).
  4. Verify the Serial Monitor says `[ALERT] Server alert sent OK` and `[SMS] Sent!`.
- [ ] **Alert UI**: The new alert immediately pops up on the web dashboard (via WebSocket).
- [ ] **Alert Resolution**: Clicking the green "Resolve" button on the Alerts page correctly updates the alert status.

## 4. Recommended Demo Order
For the best narrative flow during your presentation:

1. **The Rider Experience (Web)**: Log in as `rider1`. Show the clean UI, the live map, and the real-time sensor charts.
2. **The Hardware Connection (ESP32)**: Turn on the helmet. Show the Serial Monitor connecting. Watch the web dashboard instantly light up with live chart data and GPS movement.
3. **The Accident Simulation (Fall)**: 
   - Simulate a crash (shake + hold still).
   - Let the 8-second buzzer play out to show the "cancel window" safety feature.
   - Show the immediate SMS delivery on your phone.
   - Show the real-time critical alert appearing on the web dashboard.
4. **The Admin Perspective (Web)**: Log out and log in as `admin`. Show the global overview, focusing on how an administrator can monitor all riders and view the precise location and history of the crash that just occurred.

---
**Troubleshooting Tip:** If the firmware fails with `[HTTP] POST failed: 403`, verify that `DEVICE_SECRET` in `config.h` exactly matches `EXPECTED_DEVICE_SECRET` in `backend/api/permissions.py`.
