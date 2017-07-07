/**
 * Created by Yuzhang on 12/4/16.
 */
function changeback() {
    var currentIndex = 1;
    var totalCount = 3;

    setInterval(function () {
        if (currentIndex > totalCount)
            currentIndex = 1;

        $("body").css('background-image', 'url(../../static/images/back' + currentIndex++ + '.jpg)')
    }, 5000);
}