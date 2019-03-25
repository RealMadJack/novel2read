/* Project specific Javascript goes here. */

(function () {

  var swiper = new Swiper('.swiper-container', {
      pagination: '.swiper-pagination',
      effect: 'coverflow',
      // grabCursor: true,
      centeredSlides: true,
      loop: true,
      slidesPerView: 'auto',
      coverflow: {
          rotate: 0,
          stretch: 0,
          depth: 250,
          modifier: 1,
          slideShadows : true
      },
      //preventClicks: false,
      //preventClicksPropagation: false,
      slideToClickedSlide: true
  });

})();

