import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Field, List
from xblock.fragment import Fragment
from urlparse import urlparse
from xblock.run_script import run_script
from xblock.fragment import Fragment

from django.template import RequestContext
from django.shortcuts import render_to_response
from .utils import render_template, load_resource

import urllib

class QuizQuestion():
    """This object contains the contents of a quiz question/problem."""

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
    checkboxes only), an array of potential answers, the kind of question (text, radio, checkbox),
    and the number of attempts a student has.
    '''
    def __init__(self, kind='text', question='', options=[], answer=[], explanation='', tries=3):
        self.kind = kind
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.tries = tries

    ''' For development purposes: Output QuizQuestion variables '''
    def __str__(self):
        return "[Question: " + self.question + ", Kind: " + self.kind + ", Options: " + str(self.options) +\
               ", Answer(s): " + str(self.answer) + ", Explanation: " + str(self.explanation) + ", Result: " + ", Tries: " + str(self.tries) + "]"


class VideoQuiz(XBlock):
    """
    A VideoQuiz object plays a specified video file and at times specified in the quiz file, displays a question which
    the student has to answer. Upon completing or skipping a question, the video resumes playback.
    """

    display_name = String(
        display_name="Video Quiz",
        help="This name appears in the horizontal navigation at the top of the page",
        scope=Scope.settings,
        default="Video Quiz"
    )

    title = String(
        help="Title to be shown above the video area",
        default="", scope=Scope.content
    )

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

    quiz_content = String(
        help="Content of quiz to be displayed",
        default="", scope=Scope.content
    )

    index = Integer(
        default=-1, scope=Scope.user_state,
        help="Counter that keeps track of the current question being displayed",
    )

    ''' Deprecated
    tries = List(
        default=[], scope=Scope.user_state,
        help="The number of tries left for each question",
    )
    '''

    ''' Deprecated
    results = List(
        default=[], scope=Scope.user_state,
        help="The student's results for each question",
    )
    '''
    results = []

    answers = List(
        default=[], scope=Scope.user_state,
        help="Answers entered by the student",
    )

    quiz = []
    quiz_cuetimes = []

    def load_quiz(self):
        """Load all questions of the quiz from file located at path."""

        # purge quiz and cue times in case it already contains elements
        del self.quiz[:]
        del self.quiz_cuetimes[:]

        print("Loading quiz ...")

        # grab questions, answers, etc from form
        for line in self.quiz_content.split(';'):

            '''
            each line will contain the following:
                trigger time
                question kind (text, radio, checkbox)
                question
                optionA|optionB|optionC
                answerA|answerB
                explanation
                tries
            '''

            tmp = line.strip('\n').split(" ~ ")

            # populate trigger times for each question
            self.quiz_cuetimes.append(tmp[0])

            # populate container for quiz questions
            self.quiz.append(QuizQuestion(tmp[1], tmp[2], tmp[3].split("|"), tmp[4].split("|"), tmp[5], int(tmp[6])))
            # Check if the student records were already populated for this quiz

            #if len(self.tries) < len(self.quiz) and len(self.results) < len(self.quiz):
            if len(self.results) < len(self.quiz):
                #self.tries.append(int(tmp[6]))
                self.results.append(0)

    @XBlock.json_handler
    def get_to_work(self, data, suffix=''):
        """Perform the actions below when the module is loaded."""

        # return cue time triggers and tell whether or not the quit was loaded
        return {"vid_url": self.href, "cuetimes": self.quiz_cuetimes, "quiz_loaded": len(self.quiz) > 0,
                "correct": self.runtime.local_resource_url(self, 'public/img/correct-icon.png'),
                "incorrect": self.runtime.local_resource_url(self, 'public/img/incorrect-icon.png')}

    def grab_current_question(self):
        """Return data relevant for each refresh of the quiz form."""

        print(self.index)

        content = {
                   "index": self.index,
                   "question": self.quiz[self.index].question,
                   "kind": self.quiz[self.index].kind,
                   "options": self.quiz[self.index].options,
                   "answer": self.quiz[self.index].answer,  # originally blank to prevent cheating
                   "explanation": self.quiz[self.index].explanation,
                   "student_tries": self.quiz[self.index].tries,
                   "result": self.results[self.index]
                   }

        ''' Old code; intended to prevent students from grabbing the answer if they did not answer correctly

        # Send out answers ONLY IF the student answered correctly
        if self.results[self.index] == 5:
            content["answer"] = self.quiz[self.index].answer
        else:
            content["answer"] = "if you see this, you cheated! begone!"

        '''

        return content

    def answer_validate(self, left, right):
        """Validate student answer and return true if the answer is correct, false otherwise."""

        result = False

        if self.quiz[self.index].kind == "text":

            if left in right:
                result = True

        if self.quiz[self.index].kind == "radio":

            if left != "blank":

                # Grab only the first answer in the array returned; prevent cheating
                if left[0]['value'] in right:
                    result = True

        if self.quiz[self.index].kind == "checkbox":

            new_left = []
            for x in left:
                new_left.append(x['value'])

            result = new_left == right

        return result

    @XBlock.json_handler
    def answer_submit(self, data, suffix=''):
        """Accept, record and validate student input, and generate a mark."""

        '''
            Question states being used below:
               0 = student did not touch this question yet
               1 = failed, with tries left
               2 = tries ran out; will fail; used for initial feedback; will be set to 4 afterwards
               3 = passed; used for initial feedback; will be set to 5 afterwards
               4 = failed, with no tries left
               5 = passed
        '''

        # make sure the question is of a familiar kind
        if self.quiz[self.index].kind in ["text", "radio", "checkbox"]:

            # record student answers; might be useful for professors
            self.answers.append([self.index, data["answer"]])

            # are there any tries left?
            if self.quiz[self.index].tries > 0:

                # glitch/cheat avoidance here
                if not self.results[self.index] > 1:

                    # decrease number of tries
                    self.quiz[self.index].tries -= 1

                    # student enters valid answer(s)
                    if self.answer_validate(data["answer"], self.quiz[self.index].answer):
                        self.results[self.index] = 3
                    # student enters invalid answer, but may still have tries left
                    else:
                        self.results[self.index] = 1

        else:
            print("Unsupported kind of question in this quiz.")

        # If the tries ran out, mark this answer as failed
        if self.quiz[self.index].tries == 0 and self.results[self.index] == 1:
            self.results[self.index] = 2

        content = self.grab_current_question()

        # mark this question as attempted, after preparing output
        # ensures student is not alerted too early of completing the question in the past
        if self.results[self.index] in range(2, 4):
            self.results[self.index] += 2  # set to state 4 (failed) or 5 (passed)

        return content

    @XBlock.json_handler
    def index_goto(self, data, suffix=''):
        """Retrieve index from JSON and return quiz question strings located at that index."""

        print(data['index'])
        print(self.index)

        self.index = data['index']

        print(self.index)

        return self.grab_current_question()

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Studio only: Accepts course author input if any (no validation), and updates fields to contain current data.
        """

        # if some data is sent in, update it
        if len(data) > 0:

            # There is no validation! Enter your data carefully!

            self.title = data["vid_title"]
            self.quiz_content = data["quiz_content"]
            self.href = data["href"]
            self.height = data["height"]
            self.width = data["width"]

            print("submitted data")
            print(data["vid_title"])
            print(data["quiz_content"])
            print(data["href"])
            print(data["height"])
            print(data["width"])

        # prepare current module parameters for return
        content = {
            "vid_title": self.title,
            "quiz_content": self.quiz_content,
            "href": self.href,
            "width": self.width,
            "height": self.height,
        }

        return content

    # = edX related stuff ============================================================================================ #

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of VideoQuiz, shown to students.
        """

        # load contents of quiz
        if self.quiz_content != "":
            self.load_quiz()

        print("Loading Student View")
        print("====================")
        print(">> Parameters: ")
        print(self.quiz_content)
        print(self.href)
        print(self.width)
        print(self.height)
        print(">> Filled data")
        print("Quiz entries: " + str(self.quiz))
        print("Quiz cue times: " + str(self.quiz_cuetimes))
        print("Answers: " + str(self.answers))
        print("Results: " + str(self.results))
        # print("Tries: " + str(self.tries))

        fragment = Fragment()
        fragment.add_content(render_template('templates/html/vidquiz.html', {'self': self}))
        fragment.add_css(load_resource('static/css/vidquiz.css'))
        fragment.add_javascript(load_resource('static/js/vidquiz.js'))
        fragment.initialize_js('VideoQuiz')

        return fragment

    def studio_view(self, context=None):
        #def student_view(self, context=None):
        #def student_view(self, context=None):
        """
        The studio view of VideoQuiz, shown to course authors.
        """

        fragment = Fragment()
        fragment.add_content(render_template('templates/html/vidquiz_studio.html', {'self': self}))
        fragment.add_css(load_resource('static/css/vidquiz.css'))
        fragment.add_javascript(load_resource('static/js/vidquiz_studio.js'))

        fragment.initialize_js('VideoQuizStudio')

        return fragment

    @staticmethod
    def workbench_scenarios():
        """Workbench scenario for development and testing"""
        return [
            #("VideoQuiz", """<vidquiz href="http://videos.mozilla.org/serv/webmademovies/popcornplug.ogv" quiz_content="http://127.0.0.1/sample_quiz.txt" width="640" height="400"/>"""),
            ("VideoQuiz", """<vidquiz title="Test VidQuiz" href="http://www.youtube.com/watch?v=CxvgCLgwdNk" width="480" height="270" quiz_content="1 ~ text ~ Is this the last question? ~ yes|no|maybe ~ no ~ this is the first question ~ 5;2 ~ checkbox ~ Is this the first question? ~ yes|no|maybe ~ no|maybe ~ this is the second question ~ 5;3 ~ radio ~ Is this the second question? ~ yes|no|maybe ~ no ~ this is the third question ~ 5"/>"""),
        ]

