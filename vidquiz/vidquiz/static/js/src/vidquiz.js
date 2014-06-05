/* Javascript for VideoQuiz. */
function VideoQuiz(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {


        // IDs of elements that make up the question form
        elements = ["quiz_space", "question", "answer",	"student_answer",
                    "tries", "btn_submit", "btn_skip", "btn_continue",
                    "vid_lecture", "answer_icon"];

        // Popcorn object that affects video lecture
        var corn = Popcorn("#vid_lecture");

/** this will need some work **/
corn.footnote({
start: 2,
end: 6,
text: "Pop!",
target: "question"
});

        printall = function() {

            console.log("test");

        }


    });
}