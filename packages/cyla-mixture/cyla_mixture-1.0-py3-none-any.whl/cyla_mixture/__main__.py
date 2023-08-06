from application import App


def main():
    app = App([])

    app.main_window.show()
    app.exec_()


if __name__ == "__main__":
    exit(main())
