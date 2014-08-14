/* Javascript for VideoQuiz, Studio page. */
function VideoQuizStudio(runtime, element) {

    /* Update fields of the form to the current values */
    function formUpdate(data) {

        $(".vq_header_studio").val(data.vq_header);
        $(".quiz_content").val(data.quiz_content);
        $(".vid_url").val(data.vid_url);
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
                    "vq_header": $('.vq_header_studio').val(),
                    "quiz_content": $('.quiz_content').val(),
                    "vid_url": $('.vid_url').val(),
                    "width": $('.width').val(),
                    "height": $('.height').val()
                }),
                success: formUpdate
            });

            location.reload();

        });

    });

}
