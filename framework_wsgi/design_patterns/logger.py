class Writer:
    def write(self, text):
        raise NotImplementedError


class ConsoleWriter(Writer):
    def write(self, text, logger):
        print(f"{logger.name}: {text}")


class FileWriter(Writer):
    def __init__(self):
        self.file_name = "log"

    def write(self, text, logger):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"{logger.name}: {text}\n")


class Logger:
    _instances = {}

    def __new__(cls, name, writer=ConsoleWriter()):
        if name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            instance.name = name
            instance.writer = writer
            cls._instances[name] = instance
        return cls._instances[name]

    def log(self, text):
        text = f"log---> {text}"
        self.writer.write(text, self)


if __name__ == "__main__":
    logger1 = Logger("main_1")
    logger2 = Logger("main_2")

    print(logger1 is logger2)

    logger1.log("сообщение")
    logger2.log("сообщение")

    logger3 = Logger("another", writer=FileWriter())
    logger3.log("сообщение")
