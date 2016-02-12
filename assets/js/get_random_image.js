function updateActiveSlide(index) {
    $.get("pictures/get-random-picture", function(data, status){
        if (status == 'success') {
            // case when we don't have any images
            if (!data.result.id) {
                $(document)[0].body.innerHTML = '<br><br><br><br><p align="center">No images yet...</p>';
            }
            $('#active-slide').css(
                'background',
                'url(' + data.result.url + ')'
            );
            if (!data.result.title) {
                $('.swiper-container').css(
                    'height',
                    '95%'
                );
                $('.swiper-slide-title').css(
                    'display',
                    'none'
                );
            } else {
                $('.swiper-container').css(
                    'height',
                    '75%'
                );
                $('.swiper-slide-title').css(
                    'display',
                    'table'
                );
                $('.slide-title')[0].innerHTML = data.result.title;
            };
            $('.likes')[0].innerHTML = 'likes: ' + data.result.likes;
            $('.score')[0].innerHTML = 'score: ' + data.result.score;
            // let's store image id here
            $('.score')[0].id = data.result.id;
        };
    });
};

function likeSlide(is_liked) {
    if (!$('.score')[0]) return;
    var id= $('.score')[0].id;
    if (id) {
        $.post("pictures/like-picture/"+ id, {is_liked: is_liked}, function(data, status){});
    }
};

function updateSlides(swiper) {
    if (swiper.previousIndex == swiper.activeIndex) {
        return;
    };
    if (swiper.previousIndex < swiper.activeIndex) {
        likeSlide(true);
    } else {
        likeSlide(false);
    };
    swiper.removeAllSlides()
    updateActiveSlide();
    swiper.appendSlide('<div class="swiper-slide"><div class="swiper-slide-content" id="active-slide"></div></div>');
    swiper.appendSlide('<div id="like" class="swiper-slide"></div>');
    swiper.prependSlide('<div id="dislike" class="swiper-slide"></div>');
}

$(document).ready(function () {
    var mySwiper = new Swiper ('.swiper-container', {
        onTransitionEnd: function (swiper) {
            updateSlides(swiper);
        },
        initialSlide: 1,
        grabCursor: true,
        keyboardControl: true,
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
    });
});
