/* Javascript for VideoQuiz. */
function VideoQuiz(runtime, element) {

    var cue_times = []; // store cue times for each quiz question

    /*
    Resets question form to a blank state
    */
    function quizReset() {

        // Clear fields and reset their visibility
        $(".question").text("");
        $(".options").text("");
        $(".answer").text("");
        $(".tries").text("").show();
        $(".btn_submit").val("Submit").show();
        $(".btn_next").val("Skip");
        $(".answer_icon").hide();
        $(".answer_feedback").hide();
        $(".student_answer_simple").val("").show();

    }

    /* Update contents of quiz field to those received from quiz_content */
    function quizUpdate(quiz_content) {

        quizReset();

        $('.index', element).text(quiz_content.index);
        $('.question', element).text(quiz_content.question);

        // Draw multiple choice or checkbox options
        if (quiz_content.kind != "SA") {
            // draw the list here
            // TODO: TEMPORARY
            $('.options', element).text(quiz_content.options);
        }

        /*
        // Display feedback if student already attempted or completed this question
        if (quiz_content.attempted) {

            $('.btn_submit').hide();
            $('.btn_next').val("Continue");
            $('.tries').hide();
            $('.student_answer_simple').hide();

            if (quiz_content.result) {
                $(".answer_feedback", element).show().text("You have already answered this question. The answer was: "
                    + quiz_content.answer);
            } else {
                $(".answer_feedback", element).show().text("You have already attempted this question.");
            }

        } else {
        */

        // TODO indent this further once you can get around the attempted questions issue

        // Output tries left
        if (quiz_content.student_tries > 0) {

            $(".tries").text("Tries left: " + quiz_content.student_tries);

        } else {

            $(".tries").text("Sorry, you ran out of tries.");
            // don't bother attempting to cheat here, the server will just refuse to validate further input
            $(".btn_submit").hide();
            $(".btn_next").val("Continue");
            $(".student_answer_simple").hide();

        }

        // TODO finish part below

        if (quiz_content.result) {

            $(".answer_icon").show().attr("src", "/resource/equality_demo/public/images/correct-icon.png");
            $(".answer_feedback").show().text("Your answer is correct!");

            $('.tries', element).hide();
            $('.btn_submit', element).hide();
            $('.btn_next').val("Continue");
            $('.student_answer_simple', element).hide();

        } else {

            /*
            $(".answer_icon").show().attr("src", "/resource/equality_demo/public/images/incorrect-icon.png");
            $(".answer_feedback").show().text("Sorry, your answer is not correct!");
            $(".btn_submit").val("Resubmit");

            if (quiz_content.tries > 0) {

                $('.tries', element).text("Tries left: " + quiz_content.student_tries);
                $('.btn_submit', element).show();
                $('.student_answer', element).show();

            } else {

                $('.tries', element).text("Sorry, you ran out of tries.");
                $('.btn_submit', element).hide();
                $('.student_answer', element).hide();

            }

            $('.btn_next', element).val("Continue");
            */

        }

        //}

    }

    /* Begin quiz session */
    function getToWork(eventObject) {

        // Load quiz questions and grab their cue times
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, "get_to_work"),
            data: JSON.stringify({}),
            async: false,
            success: function(result) {
                cue_times = result.cuetimes;
            }

        });

    }

    /* Load question at index i, from vidquiz.py->self.quiz.quiz_questions */
    function quizGoto(index, eventObject) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, "index_goto"),
            data: JSON.stringify({"index": index}),
            success: quizUpdate
        });
    }

    /* Page is loaded. Do something. */
    $(function($) {

        // Load quiz questions and grab their cue times
        getToWork();

        // Popcorn object that affects video lecture
        var corn = Popcorn(".vid_lecture");

        // Set trigger times for each quiz question, and attach controls the quiz
        //elements (ie buttons, text field, etc)
        Popcorn.forEach(cue_times, function(v, k, i) {
            corn.cue(v, function() {
                corn.pause();
                $(".vid_lecture").hide();
                $(".quiz_space").show();
                quizGoto(k);
            });
        });

        // Clicked Submit/Resubmit
        $('.btn_submit').click(function(eventObject) {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'answer_submit'),
                data: JSON.stringify({"answer": $('.student_answer_simple').val()}),
                success: quizUpdate
            });

        });

        // Clicked Skip/Continue
        $('.btn_next').click(function(eventObject) {
            $(".vid_lecture").show();
            $(".quiz_space").hide();
            corn.play();
        });

    });

}