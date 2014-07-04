edx-vidquiz
===========

About
-----

This module creates a video player that at pre-set times asks the user questions, and awaits an answers. Upon answering,
the student receives feedback, and gets graded.

The studio portion of this module asks for a link to a quiz file (see below), a link to a video file, the width and
height of the video being displayed.

The quiz file can be any text file, but its first two lines must contain the following:

    #vidquiz_file
    #Syntax for this file: cue time ~ question kind ~ question ~ optionA|optionB|optionC ~ answerA|answerB ~ tries

This module was made for Seneca College, but you may use the code for your own purposes.

This module is WIP and may take a while longer to complete.

What is not complete yet
------------------------

- Multiple choice and multiple answer questions (partially done logic)
- Grading (publish() method not written yet
- MP4/webM support (this part was done in a hurry)


Setup
-----

Install just like any other XBlock module. Did not try the current version in the Production Stack yet, but it work in
the earlier stages when it was only a video player.