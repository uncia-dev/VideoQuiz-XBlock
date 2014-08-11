/* Javascript for VideoQuiz, Studio page. */
function VideoQuizStudio(runtime, element) {

    /* Update fields of the form to the current values */
    function formUpdate(data) {

        $(".vid_title").val(data.vid_title);
        $(".quiz_content").val(data.quiz_content);
        $(".href").val(data.href);
        $(".width").val(data.width);
        $(".height").val(data.height);

    }

    /* Page is loaded. Do something. */
    $(function($) {

        // Grab current values and update the fields
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'studio_submit'),
            data: JSON.stringify({}),
            success: formUpdate
        });

        // Clicked Submit
        $('.btn_submit').click(function(eventObject) {

            $.ajax({
                type: "POST",
                url: runtime.handlerUrl(element, 'studio_submit'),
                data: JSON.stringify({
                    "vid_title": $('.vid_title').val(),
                    "quiz_content": $('.quiz_content').val(),
                    "href": $('.href').val(),
                    "width": $('.width').val(),
                    "height": $('.height').val()
                }),
                success: formUpdate
            });

        });

    });

}
