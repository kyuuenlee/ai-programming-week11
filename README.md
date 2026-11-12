# 성적 CSV 검증 프로그램

## ① 무엇을 하나요
성적 CSV의 이름과 0~100점 정수를 읽어 유효한 행과 제외 기록을 나눕니다. 입력 순서를 유지하고 동명이인도 모두 남깁니다.

## ② 왜 만들었나요
실습 자료에는 빈 점수, 정수가 아닌 점수, 범위 밖 점수와 잘못된 열 개수가 섞여 있습니다. 잘못된 행 때문에 전체 작업이 중단되지 않게 하고 제외 이유를 확인하기 위해 만들었습니다. 출력값을 눈으로만 확인하는 대신 정상·예외·경계값을 반복 검증하는 것이 이번 실습의 목적입니다.

## ③ 어떻게 쓰나요
Python 3.10 이상이 필요합니다. 저장소를 내려받아 README가 있는 폴더에서 실행합니다.
```bash
git clone https://github.com/kyuuenlee/ai-programming-week11.git
cd ai-programming-week11
python -m pip install -r requirements.txt
python load_scores.py scores.csv
```
이미 저장소 폴더에 있으면 clone과 cd는 생략합니다. Windows에서 필요하면 python 대신 py, macOS에서는 python3를 사용합니다.
예상 출력: 유효 행 5개, 제외 행 5개. 빈 줄은 제외 기록에 포함하지 않습니다.

## ④ 어떻게 테스트하나요
```bash
python -m pytest test_load_scores.py -q
python -m pytest test_ai_A.py -q
python -m pytest test_ai_B.py -q
python -m pytest test_ai_bug.py -q
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
```

| 묶음 | 함수 수 | 실행 수 | 통과 | 실패 | load_scores.py 커버리지 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 설계표 기반 | 8 | 18 | 18 | 0 | 80% |
| A: 코드 제공 | 12 | 26 | 26 | 0 | 80% |
| B: 명세 제공 | 11 | 12 | 11 | 1 | 80% |
| 함정: find_max | 2 | 7 | 5 | 2 | 해당 없음 |

검증 환경: Python 3.12.14, pytest 9.2.0. pytest -q로 전체를 실행하면 **60 passed, 3 failed**입니다. AI가 생성한 테스트와 배포 함수의 관찰 결과를 그대로 보존했으므로 모든 테스트가 통과하는 프로젝트는 아닙니다.

B의 실패: `"홍길동, 2반",101`을 원본 그대로 기록할 것으로 기대했지만 배포 함수는 `홍길동, 2반,101`로 기록합니다. csv.reader로 읽은 필드를 다시 쉼표로 합치기 때문에 따옴표를 보존하지 않습니다. ‘원본줄’의 문자 그대로 보존 여부에 관한 명세와 구현의 차이를 발견했습니다.

함정의 실패: `[1, 3, 9]`에서 기대 9 / 실제 3, `[2, 9]`에서 기대 9 / 실제 2입니다. 마지막 원소를 검사하지 않는 버그를 잡았고 잘못된 결과를 정답으로 굳히지 않았습니다.

A/B 모두 커버리지는 80%지만 발견한 문제는 다릅니다. 누락 줄 77, 79~86은 명령행 실행 부분입니다. 함수 테스트의 커버리지와 별개로 프로그램 실행도 확인했습니다.

![실제 테스트 출력 요약](results/테스트_실행결과.png)

전체 원문 출력은 results의 manual.txt, A.txt, B.txt, ai_bug.txt, all.txt에 있습니다. 이미지에는 원문을 요약한 실행 결과를 표시했습니다.

의도적 실패 관찰은 별도로 실행할 수 있습니다.
```bash
python -m pytest experiments/intentional_failure.py -q
```
이 테스트는 유효 행 수를 99로 가정하여 1개가 실패합니다.

## ⑤ 파일 구성
| 파일 | 역할 |
| --- | --- |
| load_scores.py | 변경하지 않은 배포 CSV 처리 코드 |
| scores.csv, empty.csv, weird.csv | 배포 입력 파일 |
| test_load_scores.py | 설계표 기반 검증, AI 작성 지원 |
| test_ai_A.py | 새 대화에서 코드를 제공해 받은 응답 원본 |
| test_ai_B.py | 새 대화에서 명세를 제공해 받은 응답 원본 |
| test_ai_bug.py | 새 대화에서 함정 코드를 제공해 받은 응답 원본 |
| find_max.py | 함정 테스트의 import를 위해 원본 함수를 그대로 분리한 파일 |
| bug3_logic.py | 배포 함정 파일 원본 |
| experiments/ | 초기 추가 버그 관찰과 의도적 실패 실험 |
| results/ | 실행 로그, 커버리지와 실험 이력 |
| requirements.txt | 테스트 의존성 |
| prompts.txt | 배포 프롬프트 원문 |
| LICENSE | MIT 라이선스 |

## ⑥ 만든 사람 / AI 사용
- 제출자: 이규은 / 2026100320
- AI 사용: 설계표 기반 테스트 작성 지원, 별도 대화 A/B/함정 테스트 생성, 실행 검증 및 문서 초안 정리.
- 사용자가 별도 대화의 A/B/함정 응답을 전달했으며 응답 코드는 수정 없이 보존했습니다. B는 전달된 뒷부분과 일치하는 전체 생성 파일을 사용했습니다.
- find_max.py는 테스트가 요구하는 모듈명을 맞추기 위해 함정 함수만 그대로 옮겼습니다. 함수의 버그와 테스트 기대값은 변경하지 않았습니다.
- A/B/함정에서 실제 선택한 모델·설정의 동일 여부는 제출자가 확인해야 합니다.
- 설계표를 학생이 코드를 보기 전에 독립적으로 작성했다는 이력은 확인되지 않았습니다. 제작 동기와 소감은 제출자가 검토해야 합니다.
- GitHub에 최초 3개 커밋 업로드를 확인했습니다. 현재 실험 결과 변경분의 업로드와 실제 짝 교차 검증이 남아 있습니다.

## 라이선스
MIT License. 배포된 수업 자료의 원저작자 권리는 유지됩니다.
