import cv2
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class VideoRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 녹화 변수 초기화
        self.recording = False
        self.out = None
        self.save_directory = "D:/Finger_Detection/Videos"

        # Video capture object
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 녹화 파일 저장 폴더와 파일 경로
        self.output_dir = "videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_path = os.path.join(self.output_dir, "output.avi")

        # UI 초기화
        self.initUI()

        # 타이머 설정 (비디오 프레임 캡처)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def initUI(self):
        """UI 초기화 함수."""

        self.app = QApplication(sys.argv)

        self.setWindowTitle('Video Recorder')
        self.setGeometry(100, 100, 800, 600)  # 창 크기 설정

        # 메인 레이아웃 설정
        main_layout = QHBoxLayout()

        # 카메라 화면 표시용 QLabel
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("font-size: 48px; border: 1px solid black;")
        main_layout.addWidget(self.video_label)

        # 오른쪽 버튼 레이아웃
        button_layout = QVBoxLayout()

        # 녹화 시작 버튼
        self.record_button = QPushButton('녹화하기')
        self.record_button.setFixedSize(150, 50)
        button_layout.addWidget(self.record_button)

        # 저장 버튼
        self.save_button = QPushButton('녹화중지')
        self.save_button.setFixedSize(150, 50)
        button_layout.addWidget(self.save_button)

        # 종료 버튼
        self.exit_button = QPushButton('종료')
        self.exit_button.setFixedSize(150, 50)
        button_layout.addWidget(self.exit_button)

        # 버튼 정렬을 위해 여유 공간 추가
        button_layout.addStretch()

        # 녹화 파일 경로 바로가기 버튼
        self.file_path_button = QPushButton('녹화파일 경로 바로가기')
        self.file_path_button.setFixedSize(200, 40)
        button_layout.addWidget(self.file_path_button)

        # 오른쪽 레이아웃에 버튼들 추가
        # main_layout.addWidget(self.video_label)
        main_layout.addLayout(button_layout)

        # 위젯 설정
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 버튼 클릭 이벤트 연결
        self.record_button.clicked.connect(self.start_recording)
        self.save_button.clicked.connect(self.stop_recording)
        self.exit_button.clicked.connect(self.closeEvent)
        self.file_path_button.clicked.connect(self.open_file_path)

    def start_recording(self):
        """녹화를 시작하는 함수."""
        if not self.recording:
            self.recording = True
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(self.output_path, fourcc, 20.0, (self.frame_width, self.frame_height))
            print("녹화가 시작되었습니다.")
            self.timer.start(30)  # 30ms마다 프레임 캡처

    def stop_recording(self):
        """녹화를 중지하는 함수."""
        if self.recording:
            self.recording = False
            self.timer.stop()
            if self.out:
                self.out.release()
                print("녹화가 중지되었습니다.")
            
    def open_file_path(self):
        
        # 경로가 존재하는지 확인
        if os.path.exists(self.save_directory):
            print(f"열려는 폴더 경로: {self.save_directory}")

            # 운영 체제에 맞는 탐색기 명령을 사용하여 경로 열기
            if os.name == 'nt':  # Windows
                os.startfile(self.save_directory)
        else:
            print(f"경로가 존재하지 않습니다: {self.save_directory}")

    def closeEvent(self, event):
        """앱 종료 시 호출되는 함수."""
        self.cap.release()
        cv2.destroyAllWindows()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    recorder = VideoRecorderApp()
    recorder.show()
    sys.exit(app.exec_())
