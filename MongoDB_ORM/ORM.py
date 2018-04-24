from .collections.category import Category
from .collections.user import User
from .collections.question import Question
from .collections.answer import Answer
from .collections.vote import Vote
from .collections.classroomQA import Answer as ClassroomAnswer
from .collections.classroomQA import Question as ClassroomQuestion

class ORM(object):
    def __init__(self, db):
        self.db = db

        self.category = Category(self.db)
        self.user = User(self.db)
        self.question = Question(self.db)
        self.answer = Answer(self.db)
        self.vote = Vote(self.db)
        self.user.check_super_admin()
        self.classroom_answer = ClassroomAnswer(self.db)
        self.classroom_question = ClassroomQuestion(self.db)
