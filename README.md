DSP sampling

- 여러 신호를 합쳐서 샘플링 하는 것 구현
- signal 클래스
    > init
        - amplitude, frequency, phase, time 단위를 저장
        - signal 클래스를 받으면 값 그대로 저장
        - 저장 후 sinusoid(Cosine) 식을 return
    > set_sinusoid
        - sinusoid식을 재설정
    > __str__
        - 출력 시 객체 멤버변수들을 return
- 함수
    > get_signal : amplitude, frequency, phase 주면 Cos 신호식 return하는 함수
    > shift_frequency : 앨리어싱을 체크해서 frequency 바꾸는 함수
    > set_axes : 그래프에 출력할 축 값들을 정의하는 함수
- 과정
    > 입력 : 신호 수, 신호 별로 frequency, amplitude, phase 입력
    > 처리
        - 입력받은 신호를 객체화
        - 아날로그 신호, 샘플링한 신호, 앨리어싱제거 후 복원한 신호를 구함
        - 여러 신호를 입력받은 경우 신호값을 모두 더함
    > 출력
        - 합친 아날로그 신호, 그 신호를 샘플링한 신호, 앨리어싱 제거 후 복원한 신호
        - 아날로그 신호의 주파수 그래프, 앨리어싱된 신호의 주파수 표시, 앨리어싱 제거된 신호의 주파수

test
2
20

10
120
60

15
60
40
