"""
TO-DO: Write a description of what this XBlock is.
"""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

from urlparse import urlparse
from xblock.fragment import Fragment


class VideoQuiz(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    href = String(
        help="URL of the video page at the provider",
        default=None, scope=Scope.content
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
        default='', scope=Scope.content
    )

    quiz_file = String(
        help="Path to the quiz file being read",
        default='', scope=Scope.content
    )



    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

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
        frag.add_javascript(self.resource_string("static/js/src/jquery.min.js"))
        frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        frag.initialize_js('VideoQuiz')
        return frag

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}


    def studio_view(self, context):

        html = self.resource_string("static/html/vidquiz.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vidquiz.css"))
        frag.add_javascript(self.resource_string("static/js/src/vidquiz.js"))
        frag.add_javascript(self.resource_string("static/js/src/jquery.min.js"))
        frag.add_javascript(self.resource_string("static/js/src/popcorn-complete.min.js"))
        frag.initialize_js('VideoQuiz')
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("VideoQuiz",
             """<vertical_demo>
                <vidquiz href="http://videos.mozilla.org/serv/webmademovies/popcornplug.ogv" width="480" height="320"/>
                </vertical_demo>
             """),
        ]


class QuizQuestion():

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

    def __init__(question = '', type = 'SA', options = [], answer = [], tries = 3):
        print("x");

    ''' Getter for tries '''
    def get_tries(self):
        return self.tries

    ''' Getter for question '''
    def get_question(self):
        return self.question

    ''' Getter for answer '''
    def get_answers (self):
        return self.answers

    ''' Getter for result '''
    def get_result(self):
        return self.result

    ''' Getter for touched '''
    def get_touched(self):
        return self.touched

    ''' Set status of this question to touched '''
    def touch(self):
        touched = True

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
    def get_vars(self):
        '''

        return "[Question: " + question + ", Answer: " + answer + ", Result: " + result +
        ", Tries left: " + tries + ", Was it attempted? " + touched + "]"


        '''

        return False
