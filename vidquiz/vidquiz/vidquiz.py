"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Field, List
from xblock.fragment import Fragment
from urlparse import urlparse
from xblock.run_script import run_script
from xblock.fragment import Fragment

from django.template import RequestContext
from django.shortcuts import render_to_response


class QuizQuestion():
    """This object contains the contents of a quiz question/problem"""

    # kind of question being asked
    kind = 'SA'

    # question being asked
    question = ''

    # options from which to grab an answer
    options = []

    # answer(s) to the question can be an array
    answer = []

    # tries left
    tries = 3

    '''
    Constructor takes in a string for the question, an array of choices as answers (for multiple choice and
    checkboxes only), an array of potential answers, the kind of question (Simple Answer, Multiple Choice, Check Boxes),
    and the number of attempts a student has.
    '''
    def __init__(self, question='', options=[], answer=[], kind='SA', tries=3):
        self.kind = kind
        self.question = question
        self.options = options
        self.answer = answer
        self.tries = tries

    ''' For development purposes: Output QuizQuestion variables '''
    def __str__(self):
        return "[Question: " + self.question + ", Kind: " + self.kind + ", Options: " + str(self.options) +\
               ", Answer(s): " + str(self.answer) + ", Result: " + ", Tries: " + str(self.tries) + "]"


class VideoQuiz(XBlock):
    """

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
        default=-1, scope=Scope.user_state,
        help="Counter that keeps track of the current question being displayed",
    )

    '''
    tries = List(
        default=[], scope=Scope.user_state,
        help="",
    )'''

    '''
    results = List(
        default=[], scope=Scope.user_state,
        help="",
    )
    '''

    #TODO convert these to XBlock fields in order to track them
    tries = []
    results = []
    # Result states for each question:
    #   0 - not attempted
    #   1 - attempted, with tries left
    #   2 - just failed (ran out of tries)
    #   3 - just passed
    #   4 - failed
    #   5 - passed
    answers = []
    # container of quiz questions
    quiz = []
    # trigger times for each quiz question
    quiz_cuetimes = []

    def load_quiz(self, path):
        """Load all questions of the quiz from file located at path"""

        if len(self.quiz) == 0:

            # open quiz file and read its contents to the question container
            handle = open(path, 'r')

            # Quiz file pattern:
            # cue time ~ question kind ~ question ~ optionA|optionB|optionC ~ answerA|answerB ~ tries

            # Check if file is valid
            if handle.readline() != "#vidquiz_file\n":
                print("Not a valid vidquiz file!")
                # ignore this file and leave quiz empty
            else:
                handle.readline()  # skip syntax line
                # grab questions, answers, etc from file now and build a quiz
                for line in handle:
                    tmp = line.strip('\n').split(" ~ ")
                    tmp_opt = tmp[3].split("|")
                    tmp_ans = tmp[4].split("|")
                    self.quiz_cuetimes.append(tmp[0])
                    self.quiz.append(QuizQuestion(tmp[2], tmp_opt, tmp_ans, tmp[1], int(tmp[5])))
                    self.tries.append(int(tmp[5]))
                    self.results.append(0)

    @XBlock.json_handler
    def get_to_work(self, data, suffix=''):
        """Perform the actions below when the module is loaded"""

        # load contents of quiz file
        self.load_quiz(self.quiz_file)

        # return cue time triggers
        return {"cuetimes": self.quiz_cuetimes}

    def grab_current_question(self):
        """Return current quiz question and its index"""

        content = {"index": self.index,
                   "question": self.quiz[self.index].question,
                   "kind": self.quiz[self.index].kind,
                   "options": self.quiz[self.index].options,
                   "answer": "away with you, pesky cheater",
                   "student_tries": self.tries[self.index],
                   "result": self.results[self.index]
                   }

        # Send out answers ONLY IF the student answered correctly
        if self.results[self.index] == 5:
            content["answer"] = self.quiz[self.index].answer

        print("Content: " + str(content))
        print("Results: " + str(self.results))
        print("Answers " + str(self.answers))
        print("Tries: " + str(self.tries))

        return content

    def answer_validate(self, left, right, kind="SA"):
        """Validate student answer and return true if the answer is correct, false otherwise"""

        # just a basic string comparison here
        # expand if you wish to allow students some leniency with their answers

        if left in right:
            return True
        else:
            return False

    @XBlock.json_handler
    def answer_submit(self, data, suffix=''):
        """~"""

        # make sure the question is of a familiar kind
        if self.quiz[self.index].kind in ["SA", "MC", "CB"]:

            # record student answers; might be useful
            self.answers.append([self.index, data["answer"]])

            # are there any tries left?
            if self.tries[self.index] > 0:

                # glitch/cheat avoidance here
                if not self.results[self.index] > 1:

                    # decrease number of tries
                    self.tries[self.index] -= 1

                    # student enters valid answer(s)
                    if self.answer_validate(data["answer"], self.quiz[self.index].answer):
                        self.results[self.index] = 3
                    # student enters invalid answer, but may still have tries left
                    else:
                        self.results[self.index] = 1

        else:

            print("Unsupported kind of question.")

        content = self.grab_current_question()

        # If the tries ran out, set this to failed
        if self.tries[self.index] == 0 and self.results[self.index] == 1:
            self.results[self.index] = 2

        # mark this question as attempted, after preparing output
        if self.results[self.index] in range(2, 4):
            self.results[self.index] += 2

        return content

    @XBlock.json_handler
    def index_goto(self, data, suffix=''):
        """Retrieve index from JSON and return quiz question strings located at that index"""

        if self.index in range(0, len(self.quiz)):
            self.index = data['index']

        return self.grab_current_question()

    @XBlock.json_handler
    def index_reset(self, data, suffix=''):
        """Reset index to 0"""

        if self.index in range(0, len(self.quiz)):
            self.index = 0

        return self.grab_current_question()

    # ================================================================================================================ #

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

        '''
        html = self.resource_string("static/html/vidquiz.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vidquiz.css"))
        frag.add_javascript(self.resource_string("static/js/src/vidquiz.js"))
        frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        frag.initialize_js('VideoQuiz')
        '''

        html = self.resource_string("static/html/vidquiz_studio.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vidquiz.css"))
        #frag.add_javascript(self.resource_string("static/js/src/vidquiz.js"))
        #frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        #frag.initialize_js('VideoQuiz')


        return frag

    def studio_view(self, context=None):
        """
        The primary view of the VideoQuiz, shown to students
        when viewing courses.
        """

        html = self.resource_string("static/html/vidquiz_studio.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vidquiz.css"))
        frag.add_javascript(self.resource_string("static/js/src/vidquiz.js"))
        frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        frag.initialize_js('VideoQuiz')

        return frag


    @staticmethod
    def workbench_scenarios():
        """Workbench scenario for development and testing"""
        return [
            ("VideoQuiz",
             """
                <vidquiz href="http://videos.mozilla.org/serv/webmademovies/popcornplug.ogv"
                 quiz_file="/home/raymond/edx/vidquiz/sample_quiz.txt" width="320" height="200"/>
             """),
        ]