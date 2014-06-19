console.log("hello1");

function VideoQuiz(runtime, element) {

    console.log("hello2");

    var cue_times = []; // store cue times for each quiz question
    var quiz_loaded = false; // was the quiz loaded?
    var icon_correct = "";
    var icon_incorrect = "";

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

    // TODO STUFF BELOW
    // function createMultipleChoiceElement(name, type=MC/MA/LI)


    /* Update contents of quiz field to those received from quiz_content */
    function quizUpdate(quiz_content) {

        quizReset(); // refresh quiz form; not the most optimal way, but it does the job

        $('.index', element).text(quiz_content.index);
        $('.question', element).text(quiz_content.question);

        // Draw multiple choice or checkbox options
        if (quiz_content.kind == "SA") {
            $(".student_answer_simple").show();

        } else if (quiz_content.kind == "MC" || quiz_content.kind == "MA") {

            var kind = "";

            if (quiz_content.kind == "MC") kind = "radio";
            else kind = "checkbox";

            console.log(kind);


            // TODO FINISH THIS!
/*

            $(".student_answer_simple").hide();

            for (var i = 0; i < quiz_content.options.length; i++) {

                if (quiz_content.kind == "MC") {

                    $('.options').append(
                            "<p><input type=\"radio\" class=\"opt" + i + "\" value=\"" +
                                quiz_content.options[i] + "\">" + quiz_content.options[i] + "</p>");

                } else {

                    $('.options').append(
                            "<p><input type=\"checkbox\" class=\"opt" + i + "\" value=\"" +
                                quiz_content.options[i] + "\">" + quiz_content.options[i] + "</p>");

                }

            }
*/
            //$('.options', element).text(quiz_content.options);

        } else {

            $(".question").text("Invalid question type for question ID=" + quiz_content.index + ". Please contact your" +
                " professor.");
            $(".btn_submit").hide();
            $(".tries").hide();
            $(".student_answer_simple").hide();

        }

        // Display feedback if student already attempted or completed this question
        if (quiz_content.result >= 4) {

            $('.btn_submit').hide();
            $('.btn_next').val("Continue");
            $('.tries').hide();
            $('.student_answer_simple').hide();

            // TODO LIST ALL CHOICES FOR MC AND MA HERE, WITHOUT CHECKBOXES/RADIOS

            if (quiz_content.result == 5) {
                $(".answer_feedback").show().text("You have already answered this question. Valid answers were: "
                    + quiz_content.answer);
            } else {
                $(".answer_feedback").show().text("You have already attempted this question.");
            }

        } else {

            // Output tries left
            if (quiz_content.student_tries > 0) {
                $(".tries").text("Tries left: " + quiz_content.student_tries);

                // Provide feedback on the given answer

                // Right answer
                if (quiz_content.result == 3) {

                    $(".answer_icon").show().attr("src", icon_correct);
                    $(".answer_feedback").show().text("Your answer is correct!");

                    $('.tries').hide();
                    $('.btn_submit').hide();
                    $('.student_answer_simple', element).hide();
                    $('.btn_next').val("Continue");

                // Wrong answer
                } else if (quiz_content.result == 1) {

                    $(".answer_icon").show().attr("src", icon_incorrect);
                    $(".answer_feedback").show().text("Sorry, your answer is not correct!");
                    $(".btn_submit").val("Resubmit");
                    $('.btn_next').val("Continue");

                }

            // Tries ran out
            } else {

                $(".tries").text("Sorry, you ran out of tries.");
                $(".btn_submit").hide();
                $(".btn_next").val("Continue");
                $(".student_answer_simple").hide();

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

        console.log("JavaScript loading");

        if ($(".vidsrc").attr("src") != "") {

            console.log("Got a video");

            // Load quiz questions and grab their cue times
            getToWork();

            console.log(quiz_loaded);

            if (quiz_loaded) {

                console.log("Got a quiz");

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

                    $.ajax({
                        type: "POST",
                        url: runtime.handlerUrl(element, 'answer_submit'),
                        data: JSON.stringify({
                            "answer": $('.student_answer_simple').val()
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