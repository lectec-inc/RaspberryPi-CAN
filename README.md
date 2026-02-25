# RaspberryPi-CAN Production Curriculum

This repository is the production image content for the LECTEC Raspberry Pi learning platform.

It contains:
- Student-ready Jupyter notebooks (no coding required for ADAS modules).
- A hardened Wi-Fi setup and fallback workflow.
- A student-facing repo update notebook.
- Shared runtime API used by curriculum notebooks.

## Repository Layout

- `Curriculum/` - all student lessons.
- `Wifi_Update/` - Wi-Fi setup and repo update notebooks.
- `core/` - platform runtime support files.
- `student_api.py` - stable API used by lessons.

## Curriculum Map

### CAN + AI Foundations

1. `Curriculum/01_System_Introduction.ipynb`
2. `Curriculum/02_CAN_Fundamentals.ipynb`
3. `Curriculum/03_Data_Visualization.ipynb`
4. `Curriculum/04_Brake_Control.ipynb`
5. `Curriculum/05_CAN_Capstone.ipynb`
6. `Curriculum/06_AI_Introduction.ipynb`
7. `Curriculum/07_Object_Detection.ipynb`
8. `Curriculum/08_AI_Hardware_Integration.ipynb`
9. `Curriculum/09_System_Integration.ipynb`
10. `Curriculum/10_AI_Capstone.ipynb`

### ADAS Track (Independent Path)

20. `Curriculum/20_ADAS_Introduction.ipynb`
21. `Curriculum/21_ADAS_Foundations.ipynb`
22. `Curriculum/22_ADAS_TTC_Fundamentals.ipynb`
23. `Curriculum/23_ADAS_FCW_AEB_Lab.ipynb`
24. `Curriculum/24_ADAS_Capstone_Validation.ipynb`

## Student Workflow

1. Connect to the Pi (hotspot or known Wi-Fi).
2. Open Jupyter.
3. Run Wi-Fi setup when needed:
   - `Wifi_Update/wifi_setup.ipynb`
4. Run repo update before instruction sessions:
   - `Wifi_Update/update_github_repo.ipynb`
5. Open the assigned lesson in `Curriculum/`.

## Instructor Notes

- ADAS modules are implementation-focused, not code-writing assessments.
- TTC/FCW/AEB behavior is controlled via exposed lesson variables.
- Buzzer control is managed through the API to avoid GPIO pin reuse conflicts.
- Camera-dependent lessons are designed to run safely across notebook restarts.

## Production Expectations

- Use `master` as the classroom deployment baseline.
- Keep local student edits out of Git.
- Update deployed Pi units through `Wifi_Update/update_github_repo.ipynb`.

## Support

If a Pi is out of sync:
1. Launch `Wifi_Update/update_github_repo.ipynb`.
2. Run all cells.
3. Reboot the Pi after update completion.
