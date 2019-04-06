/* Project specific Javascript goes here. */

(function () {

// CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


// Swiper Slider config
let slides = window.innerWidth > 1400 ? 2 : 'auto'

var swiper = new Swiper('.swiper-container', {
    pagination: '.swiper-pagination',
    effect: 'coverflow',
    // grabCursor: true,
    centeredSlides: true,
    loop: true,
    slidesPerView: slides,
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',
    coverflow: {
        rotate: 0,
        stretch: 0,
        depth: 250,
        modifier: 1,
        slideShadows : true
    },
    //preventClicks: false,
    //preventClicksPropagation: false,
    slideToClickedSlide: true,
});



})();

