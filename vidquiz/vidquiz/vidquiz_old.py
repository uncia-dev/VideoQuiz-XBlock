"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from urlparse import urlparse
from xblock.run_script import run_script
from xblock.fragment import Fragment


class QuizQuestion():

    # kind of question being asked
    kind = 'SA'

    # question being asked
    question = ''

    # options from which to grab an answer
    options = []

    # answers to the question can be an array
    answers = []

    # tries left
    tries = 3

    # student result (fail by default)
    result = False

    # flag for whether or not student dealt with this question
    touched = False

    # used only for development/debugging purposes
    trigger_time = 0

    '''
    Constructor takes in a string for the question, an array of choices as answers (for multiple choice and
    checkboxes only), an array of potential answers, the kind of question (Simple Answer, Multiple Choice, Check Boxes),
    and the number of attempts a student has.

    trigger_time is for development purposes only
    '''
    def __init__(self, question='', options=[], answers=[], kind='SA', tries=3, trigger_time=0):
        self.kind = kind
        self.question = question
        self.options = options
        self.answers = answers
        self.tries = tries
        self.trigger_time = trigger_time

    ''' Set status of this question to touched '''
    def touch(self):
        self.touched = True

    ''' Validate student answer to be used for more precise or lenient validation '''
    def validate(self, ans=''):
        # For now it's just a direct string comparison
        return self.answers == ans

    ''' Student skips the question. Sets tries to 0 and touched to True '''
    def skip(self):
        self.tries = 0
        self.touch()

    ''' Submit student answer and return validity of answer '''
    def submit(ans=''):
        '''
            # Only process submission if the question was never attempted
            if not self.touched():
                self.tries -= 1 # decrement tries
                result = validate(ans) # validate answer
                if (tries == 0 || result) def touch()

        '''
        return False

    ''' For development purposes: Output QuizQuestion variables '''
    def __str__(self):
        return "[Question: " + self.question + ", Kind: " + self.kind + ", Options: " + str(self.options) +\
               ", Answers: " + str(self.answers) + ", Result: " + str(self.result) + ", Tries left: " +\
               str(self.tries) + ", Was it attempted? " + str(self.touched) + "]"

class Quiz():

    # container of quiz questions
    quiz = []
    cue_times = []
    quiz_len = 0

    # strings from current question
    cur_entry = -1
    cur_question = ""
    cur_options = ""
    cur_answers = ""
    cur_tries = ""

    def load_quiz(self, path):
        """Load all questions of the quiz from file located at path"""

        # open quiz file and read its contents to the question container
        handle = open(path, 'r')

        # Quiz file pattern:
        # cue time ~ question kind ~ question ~ optionA|optionB|optionC ~ answerA|answerB ~ tries

        # check if file is valid
        if handle.readline() != "#vidquiz_file\n":
            print("Not a valid vidquiz file!")
            # ignore this file and leave quiz empty
        else:
            handle.readline()  # skip syntax line
            # grab questions, answers, etc from file now and build a quiz
            for line in handle:
                self.quiz_len += 1
                tmp = line.strip('\n').split(" ~ ")
                tmp_opt = tmp[3].split("|")
                tmp_ans = tmp[4].split("|")
                self.cue_times.append(tmp[0])
                self.quiz.append(QuizQuestion(tmp[2], tmp_opt, tmp_ans, tmp[1], int(tmp[5])))

    def update(self, index=-1):
        """Copy quiz details from the self.quiz array located at index self.cur_entry"""

        target = self.cur_entry if index == -1 else index

        if target in range(0, self.quiz_len):

            # got to generate multiple choices here

            self.cur_question = self.quiz[target].question
            self.cur_options = self.quiz[target].options
            self.cur_answers = self.quiz[target].answers
            self.cur_tries = self.quiz[target].tries

                    # will need to change tries when the student loses them

        # else do nothing, quiz not loaded yet or invalid

    def start(self):
        """Begin this quiz. Sets self.cur_entry to 0 and copies quiz details from first entry of self.quiz"""

        if self.quiz_len > 0:
            self.cur_entry = 0
            self.update()

        # else do nothing, quiz not loaded yet or invalid

    def move(self, index=-1):
        """Move to next item in quiz, or the one specified by index"""

        target = self.cur_entry if index == -1 else index

        if target in range(0, self.quiz_len):

            # move to next element if index is -1
            if index == -1:
                self.cur_entry += 1
                self.update()

            # move to item at location index if index is within bounds
            else:
                self.cur_entry = target
                self.update()

class VideoQuiz(XBlock):
    """
    TO-DO: document what your XBlock does.
    """
    href = String(
        help="URL of the video page at the provider",
        default="", scope=Scope.content
    )

    width = Integer(
        help="Width of the video",
        default=640, scope=Scope.content
    )

    height = Integer(
        help="Height of the video",
        default=480, scope=Scope.content
    )

    text_area = String(
        help="Area for custom text",
        default="", scope=Scope.content
    )

    quiz_file = String(
        help="Path to the quiz file being read",
        default="", scope=Scope.content
    )

    index = Integer(
        default=0, scope=Scope.user_state,
        help="Counter that keeps track of the current question being displayed",
    )

    quiz = Quiz()

        # GOT TO FETCH FILE FROM quiz_file

    quiz.load_quiz("/home/raymond/edx/vidquiz/sample_quiz.txt")
    quiz.start()
    # need to use move to index here

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the VideoQuiz, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/vidquiz.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vidquiz.css"))
        frag.add_javascript(self.resource_string("static/js/src/vidquiz.js"))
        frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        frag.initialize_js('VideoQuiz')
        return frag

    @XBlock.json_handler
    def grab_cue_times(self):

        return 0


    def grab_current_question(self):

        content = \
            {
                "index": self.index, "question": self.quiz.cur_question,
                "options": self.quiz.cur_options, "answer": self.quiz.cur_answers,
                "tries": self.quiz.cur_tries

            }

        return content

    @XBlock.json_handler
    def increment_index(self, data, suffix=''):

        if self.index in range(0, self.quiz.quiz_len - 1):
            self.index += 1
            self.quiz.move()

        return self.grab_current_question()

    @XBlock.json_handler
    def goto_index(self, data, suffix=''):

        self.index = data['index']
        self.quiz.move(data['index'])

        return self.grab_current_question()

    @XBlock.json_handler
    def reset_index(self, data, suffix=''):

        self.quiz.start()
        self.index = 0

        content = \
            {
                "index": self.index, "question": self.quiz.cur_question,
                "options": self.quiz.cur_options, "answer": self.quiz.cur_answers,
                "tries": self.quiz.cur_tries

            }

        return content

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("VideoQuiz",
             """
                <vidquiz href="http://videos.mozilla.org/serv/webmademovies/popcornplug.ogv" quiz_file="/home/raymond/edx/vidquiz/vidquiz/vidquiz/static/samplequiz.txt" width="320" height="200"/>

             """),
        ]