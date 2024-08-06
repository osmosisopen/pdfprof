from pdfprof.main_window import MainWindow

if __name__ == '__main__':
    try:
        window = MainWindow()
    except Exception as e:
        print(e)
