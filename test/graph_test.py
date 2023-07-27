import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def create_example_plot():
    x = [1, 2, 3, 4, 5]
    y = [10, 6, 8, 4, 7]

    plt.plot(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Example Plot')
    plt.grid(True)
    plt.tight_layout()


def create_donut_chart():
    sizes = [10, 6, 8, 4, 7] # 투두리스트 갯수가 들어가야 함.
    labels = ['A', 'B', 'C', 'D', 'E'] # 이름이 들어가야 함
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    colors_ = ['#0F9B58', '#0FBC74', '#53B83A', '#3EC56B', '#1AA867', '#0FAF52', '#0FAF6B', '#53AF37']

    # Create the pie chart with wedge properties to create a donut shape
    plt.pie(sizes, labels=labels, colors=colors_, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))

    # 도넛 모양으로 그래프 그리기
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')
    plt.tight_layout()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create the main widget and set it as central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a vertical layout to hold the Matplotlib canvas
        layout = QVBoxLayout(main_widget)

        # Create the Matplotlib canvas
        canvas = FigureCanvas(plt.figure())
        layout.addWidget(canvas)

        # Create the example plot
        create_donut_chart()

        # Show the main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Matplotlib in PyQt')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())