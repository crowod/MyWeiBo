$(document).ready(function () {
    $.ajax({
        url: '/users/me',
        type: 'GET',
        data: '',
        success: function (result) {
           document.querySelector('.site-header-right .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
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

});