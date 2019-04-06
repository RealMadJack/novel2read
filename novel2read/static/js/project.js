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
var csrftoken_cookie = getCookie('csrftoken');
var csrftoken = $("[name=csrfmiddlewaretoken]").val();

// Setup ajax connections safetly
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            csrftoken = csrftoken_cookie ? csrftoken_cookie : csrftoken;
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
    var btn = $(this);
    $.ajax({
        url: btn.attr("data-vote-url"),
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.is_valid) {
                $(".js-bvotes").html(data.book_votes)
                $(".js-uvotes").html(data.user_votes)
            } else {
                alert(data.info_msg)
            }
        },
        error: function (data) {
            console.log(data.error)
        },
    });
})

$(".js-lib-btn").click(function () {
    var btn = $(this);
    $.ajax({
        url: btn.attr("data-lib-url"),
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.is_valid) {
                if (data.in_lib) {
                    btn.html('<i class="fas fa-check"></i> In Library')
                } else {
                    btn.html('Add to Library')
                }
            } else {
                alert(data.info_msg)
            }
        },
        error: function (data) {
            console.log(data.error)
        },
    });
})

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

