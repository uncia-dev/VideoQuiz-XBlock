edx-vidquiz
===========

Text below is outdated! Will update soon!

About
-----

This module creates a video player that at pre-set times asks the user questions, and awaits an answers. Upon answering,
the student receives feedback, and gets graded.

Will update these soon
//The studio portion of this module asks for a link to a quiz file (see below), a link to a video file, the width and
//height of the video being displayed.

//The quiz file can be any text file, but its first two lines must contain the following:

//    #vidquiz_file
//    #Syntax for this file: cue time ~ question kind ~ question ~ optionA|optionB|optionC ~ answerA|answerB ~ tries

This module was made for Seneca College, but you may use the code for your own purposes.

This module is WIP and may take a while longer to complete.

What is not complete yet
------------------------

- Multiple choice and multiple answer questions (partially done logic)
- Grading (publish() method not written yet
- MP4/webM support (this part was done in a hurry)


Setup
-----

vidquiz-xblock installs just like any other XBlock module. Here is a list of commands that you should run on your edX
ssh terminal:

    sudo rm -r vidquiz-xblock/
    git clone https://github.com/uw-ray/vidquiz-xblock.git
    sudo -u edxapp /edx/bin/pip.edxapp install --upgrade vidquiz-xblock/