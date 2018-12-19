$(document).ready(function () {
    $.ajax({
        url: '/users/me',
        type: 'GET',
        data: '',
        success: function (result) {
            if (result['status'] === 200) {
                document.querySelector('.user-profile-main-screen-name').innerHTML = result['data']['username'];
                document.querySelector('#following > span:nth-child(2)').innerHTML = result['data']['following_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];
            }

        }
    })
});

$(document).ready(function () {
    $.ajax({
        url: '/posts/wangyang',
        type: 'GET',
        data: '',
        success: function (result) {
            if (result['status'] === 200) {
                posts_update(result)
            }
        }
    })
});

function posts_update(result) {
        for (var i in result['data']) {
            var date = new Date(result['data'][i]['datetime']);
            date = date.getFullYear() + '/' + date.getMonth() + '/' + date.getDay();
            $('#append').append(
                $(
                    `<div class="user-activity-container">
                        <div class="user-activity">
                            <div class="user-activity-header is-flex">
                                <div class="user-activity-header-left">
                                    <div class="user-activity-header-left-avatar">
                                        <span>
                                            <div class="user-avatar ">
                                                <div class="user-avatar-content" style="background-image: url(&quot;../static/image/avatar.png&quot;);"></div>
                                            </div>
                                        </span>
                                    </div>
                                </div>
                                <div class="user-activity-header-main">
                                    <h1 class="user-name">
                                        <a href="" id="id_username">${result['data'][i]['user'][0]['username']}</a>
                                    </h1>
                                    <p class="post-time"><span>${date}</span></p>
                                </div>
                                <div class="user-activity-header-right">
                                    <svg class="symbol dropdown-trigger">
                                        <use xlink:href="#symbol-trash"></use>
                                    </svg>
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
                                            <svg class="symbol symbol-dig">
                                                <use xlink:href="#symbol-dig"></use>
                                            </svg>
                                            ${result['data'][i]['total_liked']}
                                        </a>
                                    </div>
                                    <div class="op-item ">
                                        <a>
                                            <svg class="symbol symbol-comment">
                                                <use xlink:href="#symbol-comment"></use>
                                            </svg>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                )
            )
        }
    }