# KNUE Obsidian Task Manager

이 프로그램은 한국교원대학교(KNUE) 구성원들이 Obsidian에서 사용할 수 있는 업무 관리 마크다운 파일을 생성합니다.

## 기능

사용자로부터 다음 정보를 입력받아 Obsidian 호환 마크다운(.md) 파일을 생성합니다:

1. 대상자
2. 할일 제목
3. 관련 내용
4. 현황 및 문제점
5. 해결 방안
6. 향후 추진 일정

## 사용 방법

1. 이 저장소를 클론하거나 다운로드합니다.
2. 필요한 의존성 패키지를 설치합니다 (필요한 경우).
3. 프로그램을 실행합니다.
4. 프롬프트에 따라 필요한 정보를 입력합니다.
5. 생성된 마크다운 파일을 Obsidian 볼트에 추가합니다.

## 요구 사항

- Python 3.11
- Obsidian (마크다운 파일을 열어볼 수 있는 다른 에디터도 가능)

## 설치

```bash
git clone https://github.com/kadragon/knue-obsidian-task-manager.git
cd knue-obsidian-task-manager
pip install -r requirements.txt  # 의존성 패키지가 있는 경우
```

## 사용 예시

python main.py
프로그램 실행 후, 요청되는 정보를 순서대로 입력하면 마크다운 파일이 생성됩니다.

## 기여

버그 리포트, 기능 요청, 풀 리퀘스트는 언제나 환영합니다. 큰 변경사항의 경우, 먼저 이슈를 열어 논의해주세요.
