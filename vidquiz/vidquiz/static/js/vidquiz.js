function VideoQuiz(runtime, element) {

    var cue_times = []; // store cue times for each quiz question
    var quiz_loaded = false; // was the quiz loaded?
    var icon_correct = "";
    var icon_incorrect = "";
    var cur_question_kind = "";

    /*
    Resets question form to a blank state
    */
    function quizReset() {

        // Clear fields and reset their visibility
        $(".question").text("");
        $(".answer").text("");
        $(".tries").text("").show();
        $(".btn_submit").val("Submit").show();
        $(".btn_next").val("Skip");
        $(".answer_icon").hide();
        $(".answer_feedback").hide();
        $(".student_answer").empty();

    }

    /* Update contents of quiz field to those received from quiz_content */
    function quizUpdate(quiz_content) {

        /* Question states being used below:
               0 = student did not touch this question yet
               1 = failed, with tries left
               2 = tries ran out; will fail; used for initial feedback; will be set to 4 afterwards
               3 = passed; used for initial feedback; will be set to 5 afterwards
               4 = failed, with no tries left
               5 = passed
        */

        quizReset(); // refresh quiz form; not the most optimal way, but it does the job

        cur_question_kind = quiz_content.kind;

        $('.index', element).text(quiz_content.index);
        $('.question', element).text(quiz_content.question);

        // Just a simple answer
        if (cur_question_kind == "text") {

            $(".student_answer").append(
                $("<p>").append(
                    $("<input />", {
                            type: cur_question_kind,
                            class: "answer_simple"
                        }
                    )
                )
            );

        // Student may choose from an array of answers
        } else if (cur_question_kind == "radio" || cur_question_kind == "checkbox") {

            $.each(quiz_content.options, function() {
                $(".student_answer").append(
                    $("<li>").text(this).append(
                        $('<input />', {
                            type: cur_question_kind,
                            class: 'answer_multi_' + this,
                            name: 'answer_multi',
                            value: this
                        })
                    )
                );
            });

        // Notify student that there is an error and this question will not work
        } else {

            $(".question").text("Invalid question type for question ID=" + quiz_content.index + ". Please contact your" +
                " professor.");
            $(".btn_submit").hide();
            $(".tries").hide();

        }

        // Display feedback if student already attempted or completed this question
        if (quiz_content.result >= 4) {

            $('.btn_submit').hide();
            $('.btn_next').val("Continue");
            $('.tries').hide();
            $(".student_answer").empty();

            if (cur_question_kind == "radio" || cur_question_kind == "checkbox") {
                $.each(quiz_content.options, function() {
                    $(".student_answer").append(
                        $("<li>").text(this)
                    );
                });
            }

            if (quiz_content.result == 5) {

                var out = "You have already answered this question. The valid answer";

                if (quiz_content.answer.length > 1) {
                    out += "s were: ";
                } else {
                    out += " was: "
                }

                $(".answer_feedback").show().text(out + quiz_content.answer + ".");

            } else {

                $(".answer_feedback").show().text("You have already attempted this question.");

            }

        // Question isn't a "finalized" stage yet
        } else {

            // Provide feedback on the given answer

            // Right answer
            if (quiz_content.result == 3) {

                $(".answer_icon").show().attr("src", icon_correct);
                $(".answer_feedback").show().text("Your answer is correct!");

                $('.tries').hide();
                $('.btn_submit').hide();
                $('.btn_next').val("Continue");
                $(".student_answer").empty();

            // Wrong answer
            } else if (quiz_content.result == 1) {

                $(".answer_icon").show().attr("src", icon_incorrect);
                $(".answer_feedback").show().text("Sorry, your answer is not correct!");
                $(".btn_submit").val("Resubmit");
                $('.btn_next').val("Continue");

            } else if (quiz_content.result == 2) {

                // *crickets*

            }

            // Output tries left
            if (quiz_content.student_tries > 0) {
                $(".tries").text("Tries left: " + quiz_content.student_tries);

            // Tries ran out
            } else {

                $(".student_answer").empty();
                $(".tries").text("Sorry, you ran out of tries.");
                $(".btn_submit").hide();
                $(".btn_next").val("Continue");

            }

        }

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
                quiz_loaded = result.quiz_loaded;
                icon_correct = result.correct;
                icon_incorrect = result.incorrect;
            }

        });

    }

    /* Load question at index i, from vidquiz.py->self.quiz */
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

        // Is a video file assigned to vid_lecture?
        if ($(".vidsrc").attr("src") != "") {

            // Load quiz questions and grab their cue times
            getToWork();

            if (quiz_loaded) {

                // Load Popcorn js
                $.getScript("http://cdn.popcornjs.org/code/dist/popcorn.min.js", function(){

                    // Popcorn object that affects video lecture
                    var corn = Popcorn(".vid_lecture");

                    // Set trigger times for each quiz question, and attach controls the quiz
                    //elements (ie buttons, text field, etc)
                    Popcorn.forEach(cue_times, function (v, k, i) {
                        corn.cue(v, function () {
                            corn.pause();
                            $(".vid_lecture").hide();
                            $(".quiz_space").show();
                            quizGoto(k);
                        });
                    });

                    // Clicked Submit/Resubmit
                    $('.btn_submit').click(function (eventObject) {

                        var out = [];

                        if (cur_question_kind == "text") {
                            out = $('.answer_simple').val();
                        }

                        if (cur_question_kind == "checkbox") {
                            out = $('input:checkbox').serializeArray();
                        }

                        if (cur_question_kind == "radio") {
                            out = $('input:radio').serializeArray();
                            if (out.length == 0) out = "blank"; // still need to pass something to the server
                        }

                        $.ajax({
                            type: "POST",
                            url: runtime.handlerUrl(element, 'answer_submit'),
                            data: JSON.stringify({
                                "answer": out
                            }),
                            success: quizUpdate
                        });

                    });

                    // Clicked Skip/Continue
                    $('.btn_next').click(function (eventObject) {
                        $(".vid_lecture").show();
                        $(".quiz_space").hide();
                        corn.play();
                    });


                });

            } else {

                $(".vid_lecture").hide();
                $(".quiz_space").hide();
                $(".novid").hide();
                $(".noquiz").show();

            }

        } else {

            $(".vid_lecture").hide();
            $(".quiz_space").hide();
            $(".novid").show();

        }

    });

}