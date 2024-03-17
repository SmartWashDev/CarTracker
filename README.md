# CarTracker


## Установака

```bash
python -m venv venv
pip install -r requirements.txt
```

## Активация окружения

Windows:
```bash
venv/Scripts/activate
```

Linux:
```bash
source venv/bin/activate
```

## Запуск
```bash
cd detect
```

```bash
python tracking.py model=yolov8n.pt source="VIDEO_NAME" show=True
```
* source - Путь до видео
* show - Показывать видео или нет, пока идет процесс

Далее видео сохраняется по пути `detect/runs/train*/VIDEO_NAME.mp4`


## Исходник
https://github.com/noorkhokhar99/YOLOv8-Object-Detection-with-DeepSORT-Tracking

