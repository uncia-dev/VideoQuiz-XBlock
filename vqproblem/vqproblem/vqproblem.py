"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean, List
from xblock.fragment import Fragment


class VideoQuizProblem(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    quiz_path = None

    question = String(
        default=None, scope=Scope.content,
        help="The question being asked"
    )

    type = String(
        default="SA", scope=Scope.content,
        help="The type of the problem: Simple Answer, Multiple Choice, Check Boxes (SA, MC, CB)"
    )

    options = List(
        default=None, scope=Scope.content,
        help="Options available for the student (for MC and CB)"
    )

    answer = String(
        default=None, scope=Scope.content,
        help="The answer to the question being asked"
    )

    tries = Integer(
        default=3, scope=Scope.user_state,
        help="Counter for the number of tries the student has left"
    )

    max_tries = Integer(
        default=3, scope=Scope.content,
        help="Maximum number of tries a student gets"
    )

    result = Boolean(
        default=False, scope=Scope.user_state,
        help="Student result (fail by default)"
    )

    touched = Boolean(
        default=False, scope=Scope.user_state,
        help="#Flag for whether or not student dealt with this question"
    )

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the VideoQuizProblem, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/vqproblem.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/vqproblem.css"))
        frag.add_javascript(self.resource_string("static/js/src/vqproblem.js"))
        frag.initialize_js('VideoQuizProblem')
        return frag

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

########################################################################################################################





########################################################################################################################

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("VideoQuizProblem",
             """
                <vqproblem question="What is the question"/>

             """),
        ]