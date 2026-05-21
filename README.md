# Introduction
우비 인식 시스템 개발

# Structure
```text
./
├── compare
│  └── compare.py               - 백터값을 입력받아 데이터베이스에 해당 가중치를 가진 항목이 있는지 반환
├── database
│  ├── info.py                  - 사용자 정보 클래스를 위한 파일
│  └── database.py              - 데이터베이스와의 상호작용
├── extraction
│  └── extraction.py            - AI를 활용하여 우비의 특징을 벡터값으로 반환
├── ui
│  └── ui.py                    - 사용자와의 상호작용을 위한 UI 설계
└── main.py                     - 프로그램 시작점
```

# Architecture