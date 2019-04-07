/* Project specific Javascript goes here. */

(function () {

// CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrf_form = $("[name=csrfmiddlewaretoken]").val()
let csrftoken = csrf_form ? csrf_form : getCookie('csrftoken');

// Setup ajax connections safetly
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            console.log(csrftoken)
        }
    }
});

// Ajax Votes
function btnAjaxAnimate(btn) {
    btn.setAttribute("style", "width: 100px;")
    btn.html('...')
}

$(".js-vote-btn").click(function () {
    let btn = $(this);
    $.ajax({
        url: btn.attr("data-vote-url"),
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.is_valid) {
                $(".js-bvotes").html(data.book_votes)
                $(".js-uvotes").html(data.user_votes)
            } else {
                alert(data.info_msg)  // Change
            }
        },
        error: function (xhr) {
            console.log(`${xhr.status} ${xhr.statusText}`)
        },
    });
})

$(".js-lib-btn").click(function () {
    let btn = $(this);
    $.ajax({
        url: btn.attr("data-lib-url"),
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.is_valid) {
                console.log(btn)
                if (data.in_lib) {
                    btn.html('<i class="fas fa-check"></i> In Library')
                } else {
                    btn.html('Add to Library')
                }
            } else {
                alert(data.info_msg)  // Change
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(`${xhr.status} ${xhr.statusText}`)
        },
    });
})

// Swiper Slider config
let slides = window.innerWidth > 1750 ? 'auto' : 'auto'
let slideDepth = window.innerWidth > 2000 ? 280 : 550
let swiperOptions = {
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
        depth: slideDepth,
        modifier: 1,
        slideShadows: false,
    },
    //preventClicks: false,
    //preventClicksPropagation: false,
    slideToClickedSlide: true,
}
let swiper = new Swiper('.swiper-container', swiperOptions);



})();

