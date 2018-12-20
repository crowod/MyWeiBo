var useravatar ;
var username;
$(document).ready(function () {
    $.ajax({
        url: '/users/me',
        type: 'GET',
        data: '',
        success: function (result) {
                document.querySelector('.user-profile-main-screen-name').innerHTML = result['data']['username'];
                document.querySelector('.user-profile-main-item').innerHTML = 'Earned ' + result['data']['likes_earn'] + ' likes';
                document.querySelector('#following > span:nth-child(2)').innerHTML = result['data']['following_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];
                document.querySelector('.user-profile .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                document.querySelector('.site-header-right .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                username = document.querySelector('.user-profile-main-screen-name').innerHTML;
                useravatar = result['data']['avatar_url'];
            }
    })

});