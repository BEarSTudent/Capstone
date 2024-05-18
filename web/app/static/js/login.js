// var id_duplication_check = false;
// var password_pass = false;

// window.onload = function() {
//     var join = document.join; // form 데이터를 모두 join 변수에 저장
//     var input = document.querySelectorAll('.check');
//     var errorId = ["id_error", "pw_error", "pw_check_error", "name_error"];

//     document.join.addEventListener("keydown", evt => {
//         if (evt.code === "Enter") evt.preventDefault();
//     });

//     join.user_id.onkeyup = validateUserId;
//     join.user_pw.onkeyup = validatePassword;
// };

// function validateUserId() {
//     var idLimit = /^[a-zA-Z0-9~!@#$%^&*()_-]{2,16}$/;
//     var userId = document.getElementById('user_id').value;
//     if (!idLimit.test(userId)) {
//         id_duplication_check = false;
//         document.getElementById('id_error').innerHTML = "2~16자의 영문 소대문자, 숫자와 특수기호'~!@#$%^&*()_-'만 사용 가능합니다.";
//     } else if (!id_duplication_check) {
//         document.getElementById('id_error').innerHTML = "중복 확인이 필요합니다";
//     } else {
//         id_duplication_check = true
//         document.getElementById('id_error').innerHTML = " ";
//     }
// }

// function validatePassword() {
//     var pwLimit = /^[a-zA-Z0-9~!@#$%^&*()_-]{8,16}$/;
//     var password = document.getElementById('user_pw').value;
//     if (!pwLimit.test(password)) {
//         password_pass = false;
//         document.getElementById('pw_error').innerHTML = "8~16자리 숫자, 특수문자(~!@#$%^&*()_-), 영어로 작성해주세요";
//     } else {
//         password_pass = true;
//         document.getElementById('pw_error').innerHTML = " ";
//     }
//     validatePasswordMatch(); // 비밀번호가 변경되면 비밀번호 확인도 다시 검사
// }

async function go2register(event) {
    event.preventDefault();  // 기본 폼 제출 동작을 막음
    window.location.href = '/register';
}

async function postdata(event) {
    event.preventDefault();  // 기본 폼 제출 동작을 막음

    const user_id = document.getElementById('user_id').value;
    const user_pw = document.getElementById('user_pw').value;
    
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: user_id, pw: user_pw}),
    });
    const result = await response.json();

    if (result.exists) {
        if (result.pw_match) {
            document.getElementById('state_message').innerHTML = '<font color=blue>로그인 성공</font>';
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            document.getElementById('state_message').innerHTML = '<font color=red>비밀번호가 틀렸습니다</font>';
        }
    } else {
        document.getElementById('state_message').innerHTML = '<font color=red>등록된 사용자가 아닙니다</font>';
    }
}
