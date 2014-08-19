VidQuiz XBlock
==============

About
-----

This XBlock is a YouTube video player module for the edX platform, which can also used to display questions at pre-set
times, and awaits student input. Three types of questions are supported so far: simple answers, multiple choice
(radio boxes) and also multiple answers (check boxes). Once a student answers correctly, or runs out of tries, the
student can also view an explanation dialog for the current question. At the end of the video playback, the students get
a small statistic as well, showing the percentage of completed questions.

On the edX Studio side of this module, the professor has to input a title (both the navigation bar in edX, and the
header within the module, a full HTTPS link to a YouTube video, without extra parameters (though they can technically
work), and the content for the questions. The syntax for the quiz content is as follows:

    trigger time ~ question ~ option1|option2|option3 ~ answer1|answer2|answer3 ~ explanation

You can have one or more options and answers for each questions. Options and all but the first answer will be ignored
for text answers.

This module was made for Seneca College, but you may of course use and adapt this code as you wish. There are still
hidden left-overs from development which you can also use. Initially grading was supposed to implemented, the number of
tries would be shown to students and the size of the video could be controlled. The quiz content was also in a separate
file. Initially only HTML5 videos were also support, but we have migrated to YouTube for less cross-platform hassles.

This module uses JQuery, JQueryUI and Popcorn.js. Everything else is just stock XBlock features.

Setup
-----

vidquiz-xblock installs just like any other XBlock module. Here is a list of commands that you should run on your edX
ssh terminal:

    sudo rm -r vidquiz-xblock/ # in case you have an older version
    git clone https://github.com/uw-ray/vidquiz-xblock.git
    sudo -u edxapp /edx/bin/pip.edxapp install --upgrade vidquiz-xblock/ # --upgrade only if you have an older version


Sample Quiz
-----------

YouTube Video URL:

    https://www.youtube.com/watch?v=CxvgCLgwdNk (Popcorn.js demo video)

Quiz content:

    1 ~ text ~ Is this the last question? ~ yes|no|maybe ~ no ~ this is the first question
    2 ~ checkbox ~ Is this the first question? ~ yes|no|maybe ~ no|maybe ~ this is the second question
    3 ~ radio ~ Is this the second question? ~ yes|no|maybe ~ no ~ this is the third question
