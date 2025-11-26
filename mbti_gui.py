import tkinter as tk
from tkinter import messagebox

class MBTIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ 초간단 MBTI 검사기")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # 데이터 초기화
        self.questions = [
            {"q": "1. 휴일에 나는?", "A": "친구들을 만나 밖에서 에너지를 얻는다.", "B": "집에서 혼자 쉬며 에너지를 충전한다.", "types": "EI"},
            {"q": "2. 새로운 모임에 갔을 때 나는?", "A": "먼저 말을 걸고 분위기를 주도한다.", "B": "조용히 앉아 다른 사람의 말을 듣는다.", "types": "EI"},
            {"q": "3. 친구가 갑자기 약속을 취소하면?", "A": "다른 친구에게 연락해 볼까 고민한다.", "B": "오예! 집에서 쉴 수 있다.", "types": "EI"},
            {"q": "4. 노래를 들을 때 나는?", "A": "멜로디와 가사가 현실적인지 본다.", "B": "노래가 주는 느낌과 상상에 빠진다.", "types": "SN"},
            {"q": "5. 길을 설명할 때 나는?", "A": "큰 건물, 거리 이름 등 구체적인 정보를 준다.", "B": "지도 전체의 느낌이나 방향 위주로 설명한다.", "types": "SN"},
            {"q": "6. 영화를 볼 때 더 끌리는 것은?", "A": "실화 바탕, 현실적인 사건.", "B": "판타지, SF, 열린 결말.", "types": "SN"},
            {"q": "7. 친구가 우울해서 머리를 잘랐다고 하면?", "A": "어느 미용실 갔어? 잘 잘랐어?", "B": "무슨 일 있었어? 기분 전환은 좀 됐어?", "types": "TF"},
            {"q": "8. 내가 더 중요하게 생각하는 것은?", "A": "논리적인 사실과 원칙.", "B": "사람들의 감정과 상황 참작.", "types": "TF"},
            {"q": "9. 친구와 말싸움 중 나는?", "A": "누가 옳고 그른지 따지는 게 중요하다.", "B": "친구가 상처받지 않게 말하는 게 중요하다.", "types": "TF"},
            {"q": "10. 여행 계획을 짤 때 나는?", "A": "분 단위로 엑셀에 정리한다.", "B": "큰 틀만 잡고 가서 생각한다.", "types": "JP"},
            {"q": "11. 책상 위 상태는?", "A": "필요한 물건이 딱딱 정리되어 있다.", "B": "어디에 뭐가 있는지 나만 안다.", "types": "JP"},
            {"q": "12. 마감 기한이 주어졌을 때?", "A": "미리미리 해서 여유 있게 끝낸다.", "B": "마지막까지 미루다가 불태운다.", "types": "JP"}
        ]
        
        self.descriptions = {
            "ISTJ": "청렴결백한 논리주의자! 책임감이 강하고 현실적이에요.",
            "ISFJ": "용감한 수호자! 성실하고 온화하며 협조적이에요.",
            "INFJ": "선의의 옹호자! 통찰력이 뛰어나고 공동체의 이익을 중시해요.",
            "INTJ": "용의주도한 전략가! 독창적이고 비판적인 분석가예요.",
            "ISTP": "만능 재주꾼! 과묵하지만 상황 적응력이 뛰어나요.",
            "ISFP": "호기심 많은 예술가! 온화하고 겸손하며 삶의 여유를 즐겨요.",
            "INFP": "열정적인 중재자! 이상적이고 깊은 내면을 지녔어요.",
            "INTP": "논리적인 사색가! 지적 호기심이 많고 잠재력을 봐요.",
            "ESTP": "모험을 즐기는 사업가! 타협을 잘하고 현실적인 문제 해결사예요.",
            "ESFP": "자유로운 영혼의 연예인! 사교적이고 분위기 메이커예요.",
            "ENFP": "재기발랄한 활동가! 열정적이고 상상력이 풍부해요.",
            "ENTP": "뜨거운 논쟁을 즐기는 변론가! 박학다식하고 독창적이에요.",
            "ESTJ": "엄격한 관리자! 구체적이고 사실적이며 지도력이 있어요.",
            "ESFJ": "사교적인 외교관! 친절하고 동료애가 많아요.",
            "ENFJ": "정의로운 사회운동가! 카리스마 있고 충실하며 책임감이 강해요.",
            "ENTJ": "대담한 통솔자! 철저한 준비와 활동적인 리더십이 있어요."
        }

        self.reset_game()

    def reset_game(self):
        """게임을 초기화하는 함수"""
        self.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        self.current_idx = 0
        
        # UI 구성요소들을 화면에 배치 (처음 실행 시)
        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()
            
        self.setup_ui()
        self.update_question()

    def setup_ui(self):
        """화면 디자인 배치"""
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')

        # 진행 상황 표시
        self.progress_label = tk.Label(self.main_frame, text="", font=("Arial", 10), fg="gray")
        self.progress_label.pack(pady=(0, 10))

        # 질문 텍스트
        self.question_label = tk.Label(self.main_frame, text="", font=("Arial", 14, "bold"), wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        # 버튼 A
        self.btn_a = tk.Button(self.main_frame, text="", font=("Arial", 11), width=40, height=2, 
                               command=lambda: self.process_answer('A'), bg="#f0f0f0", activebackground="#e0e0e0")
        self.btn_a.pack(pady=10)

        # 버튼 B
        self.btn_b = tk.Button(self.main_frame, text="", font=("Arial", 11), width=40, height=2, 
                               command=lambda: self.process_answer('B'), bg="#f0f0f0", activebackground="#e0e0e0")
        self.btn_b.pack(pady=10)

    def update_question(self):
        """현재 질문을 화면에 업데이트"""
        q_data = self.questions[self.current_idx]
        
        self.progress_label.config(text=f"Question {self.current_idx + 1} / {len(self.questions)}")
        self.question_label.config(text=q_data['q'])
        self.btn_a.config(text=f"A. {q_data['A']}")
        self.btn_b.config(text=f"B. {q_data['B']}")

    def process_answer(self, choice):
        """사용자 응답 처리"""
        q_data = self.questions[self.current_idx]
        
        # 점수 계산
        target_type = q_data['types'][0] if choice == 'A' else q_data['types'][1]
        self.scores[target_type] += 1
        
        # 다음 질문으로 이동
        self.current_idx += 1
        
        if self.current_idx < len(self.questions):
            self.update_question()
        else:
            self.show_result()

    def show_result(self):
        """결과 화면 출력"""
        mbti_result = ""
        mbti_result += "E" if self.scores["E"] >= self.scores["I"] else "I"
        mbti_result += "S" if self.scores["S"] >= self.scores["N"] else "N"
        mbti_result += "T" if self.scores["T"] >= self.scores["F"] else "F"
        mbti_result += "J" if self.scores["J"] >= self.scores["P"] else "P"
        
        desc = self.descriptions.get(mbti_result, "분석 불가")

        # 결과창 UI로 변경
        self.main_frame.destroy()
        
        result_frame = tk.Frame(self.root, padx=20, pady=40)
        result_frame.pack(expand=True, fill='both')
        
        tk.Label(result_frame, text="당신의 MBTI 유형은", font=("Arial", 12)).pack()
        tk.Label(result_frame, text=mbti_result, font=("Arial", 30, "bold"), fg="#3776AB", pady=10).pack()
        tk.Label(result_frame, text=desc, font=("Arial", 11), wraplength=350, justify="center").pack(pady=20)
        
        tk.Button(result_frame, text="다시 테스트하기", command=self.reset_game, 
                  font=("Arial", 12), bg="#4CAF50", fg="white", width=20).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MBTIApp(root)
    root.mainloop()