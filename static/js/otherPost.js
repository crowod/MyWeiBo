var like_post_id = [];
var useravatar ;
var username;
$(document).ready(function () {
    $.ajax({
        url: '/users/me',
        type: 'GET',
        data: '',
        success: function (result) {
           document.querySelector('.site-header-right .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
            $('#welcome')[0].innerText = 'Welcome ' + result['data']['username'] + "!"
        }
    })
});
$(document).ready(function () {
    username = document.querySelector('.user-profile-main-screen-name').innerHTML;
    $("#post").attr("href", "/" + username + "/post");
    $("#following").attr("href", "/" + username + "/following");
    $("#follower").attr("href", "/" + username + "/follower");
    $.ajax({
        url: '/users/' + username,
        type: 'GET',
        data: '',
        success: function (result) {
            $('#avatar').css('background-image', `url(${result['data']['avatar_url']})`);
            document.querySelector('.user-profile-main-item').innerHTML = 'Earned ' + result['data']['likes_earn'] + ' likes';
            document.querySelector('#followings > span:nth-child(2)').innerHTML = result['data']['following_num'];
            document.querySelector('#followers > span:nth-child(2)').innerHTML = result['data']['follower_num'];
            like_post_id = result['data']['like_post_id']
            useravatar = result['data']['avatar_url'];
            if(result['is_following'] === false){
                document.querySelector('.user-profile-operation-subscribe-primary').innerHTML = "Unfollowing";
                document.querySelector('.user-profile-operation-subscribe-danger').innerHTML = "Following";
            }else if(result['is_following'] === true){
                document.querySelector('.user-profile-operation-subscribe-primary').innerHTML = "Following";
                document.querySelector('.user-profile-operation-subscribe-danger').innerHTML = "Unfollowing";
            }
        }
    })
    $.ajax({
        url: '/posts/' + username,
        type: 'GET',
        data: '',
        success: function (result) {
            posts_update(result)
        }
    })

});

function posts_update(result) {
    for (var i in result['data']) {
        var date = new Date(result['data'][i]['datetime']);
        date = date.getFullYear() + '/' + date.getMonth() + '/' + date.getDay();
        $('#append').append(
            $(
                `<div class="user-activity-container" id=${result['data'][i]['id']}>
                    <div class="user-activity">
                        <div class="user-activity-header is-flex">
                            <div class="user-activity-header-left">
                                <div class="user-activity-header-left-avatar">
                                    <span>
                                        <div class="user-avatar ">
                                            <div class="user-avatar-content avatar"></div>
                                        </div>
                                    </span>
                                </div>
                            </div>
                            <div class="user-activity-header-main">
                                <h1 class="user-name">
                                    <a href="/${username}/post" id="id_username">${username}</a>
                                </h1>
                                <p class="post-time"><span>${date}</span></p>
                            </div>
                        </div>
                        <div class="user-activity-body">
                            <div class="user-activity-content">
                                <div class="user-activity-post">
                                    <div class="readable-content">
                                        <div class="readable-content-collapse">
                                            <span>${result['data'][i]['content']}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="user-activity-footer">
                            <div class="op-wrap">
                                <div class="op-item ">
                                    <a>
                                        <svg class="symbol symbol-dig like">
                                            <use xlink:href="#symbol-dig"></use>
                                        </svg>
                                        <p>${result['data'][i]['total_liked']}</p>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`
            )
        )
    }
    $('.user-activity-container').each(function () {
        if (like_post_id.indexOf(parseInt($(this)[0].id)) !== -1) {
            $(this).find('.like').parent().parent().addClass('is-active');
        }
        $('.avatar').css('background-image', 'url(' + useravatar + ') ');
    });
}

$(document).on('click', '.like', function () {
    var post_id = $(this).parents('.user-activity-container')[0].id;
    var element = $(this).parent().parent();
    var data = new URLSearchParams();
    data.append('post_id', post_id);
    $.ajax({
        url: '/like',
        type: 'POST',
        data: data.toString(),
        success: function (result) {
            if (element.hasClass('is-active'))
                element.removeClass('is-active');
            else
                element.addClass('is-active');
            element.find('p').text(result['total_like']);
        }
    })
});

$(document).on('click', '.user-profile-operation-subscribe', function () {
    var data = new URLSearchParams();
    data.append('following_name', username);
    if(document.querySelector('.user-profile-operation-subscribe-primary').innerHTML === "Unfollowing"){
        $.ajax({
            url: '/following/add',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                document.querySelector('.user-profile-operation-subscribe-primary').innerHTML = "Following";
                document.querySelector('.user-profile-operation-subscribe-danger').innerHTML = "Unfollowing";
            }
        })
    }else if(document.querySelector('.user-profile-operation-subscribe-primary').innerHTML === "Following"){
        $.ajax({
            url: '/following/cancel',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                document.querySelector('.user-profile-operation-subscribe-primary').innerHTML = "Unfollowing";
                document.querySelector('.user-profile-operation-subscribe-danger').innerHTML = "Following";
            }
        })
    }

});