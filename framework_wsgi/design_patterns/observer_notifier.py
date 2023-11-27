from typing import List


from framework_wsgi.design_patterns.domain_courses import CoursesStudents


class CourseSubject:
    def __init__(self, course_id):
        self.course_id = course_id

        self.observers: List[Observer] = self.get_observers()

    def get_observers(self) -> list:
        from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
        from framework_wsgi.design_patterns.connector import ConnectorDB
        from framework_wsgi.design_patterns.domain_users import Students

        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            return [
                repo(Students).find_by_id(c_s.student_id)
                for c_s in repo(CoursesStudents).all()
                if c_s.course_id == self.course_id
            ] or []

    # def add_observer(self, observer):
    #     self.observers.append(observer)

    # def remove_observer(self, observer):
    #     self.observers.remove(observer)

    def notify_students_on_course(self, message: str):
        for item in self.observers:
            item.update(message=message)


class Observer:
    def update(self, subject: CourseSubject):
        pass


class SMSNotifier(Observer):
    def update(self, message):
        print(f"SMS -> {message})")


class EMAILNotifier(Observer):
    def update(self, message):
        print(f"EMAIL -> {message})")


if __name__ == "__main__":
    subject = CourseSubject(course_id=12)

    subject.notify_students_on_course(
        f"some message from course_id: {subject.course_id}"
    )
    # EMAIL -> some message from course_id: 12)
    # EMAIL -> some message from course_id: 12)
    # EMAIL -> some message from course_id: 12)
