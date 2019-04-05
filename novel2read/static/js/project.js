/* Project specific Javascript goes here. */

(function () {

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

