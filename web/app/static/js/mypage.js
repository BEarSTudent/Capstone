function mypage() {
    let board_num = document.getElementById("board_num");
    board_num.innerHTML = user_board_data.length + "개";
    let savebox_num = document.getElementById("savebox_num");
    savebox_num.innerHTML = user_savebox_data.length + "개";

    user_board();
}

function user_board() {
    select[0].classList.add("selected");
    select[1].classList.remove("selected");

    clear_board();

    last_num = 0;
    board_data = user_board_data;

    load_boards();
}

function user_savebox() {
    select[0].classList.remove("selected");
    select[1].classList.add("selected");

    clear_board();

    last_num = 0;
    board_data = user_savebox_data;

    load_boards();
}

function clear_board() {
    boards.innerHTML = ''
}

function check_pw() {
    // clear
    let profile_box = document.getElementById("profile");
    let block = document.getElementById("user_text");
    block.innerHTML = "";
    let edit_button = document.getElementById("profile_edit");
    profile_box.removeChild(edit_button);

    // check pw form
    let check_pw_explain = document.createElement("div");
    check_pw_explain.setAttribute("id", "check_pw_explain");
    check_pw_explain.innerHTML = "비밀번호 확인이 필요합니다.";
    block.appendChild(check_pw_explain);

    let pw_input = document.createElement("input");
    pw_input.setAttribute("id", "pw_input")
    pw_input.setAttribute("type", "password");
    pw_input.setAttribute("onkeypress", "check_input_pw(event)");
    block.appendChild(pw_input);
    pw_input.focus();

    let password_check_text = document.createElement("div");
    password_check_text.setAttribute("id", "password_check_text");
    block.appendChild(password_check_text);
}

async function check_input_pw(e) {
    if (e.keyCode == 13) {
        let pw_input = document.getElementById("pw_input").value;
        
        const response_data = await fetch("/mypage/pwcheck", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'check_pw': pw_input})
        })
        .then(res => res.json())
        
        let password_check_text = document.getElementById("password_check_text")
        if (response_data.pw_match){
            edit_profile(response_data.user_data);
        }
        else{
            password_check_text.innerHTML = "비밀번호가 일치하지 않습니다."
        }
    }
}

function edit_profile(user_data) {
    // clear
    // let profile_box = document.getElementById("profile");
    let block = document.getElementById("user_text");
    block.innerHTML = "";

    // profile form
    let profile_form = document.createElement("form");

    let form_name_label = document.createElement("label");
    form_name_label.setAttribute("id", "form_name_label")
    form_name_label.innerHTML = "이름: ";

    let form_name_text = document.createElement("input");
    form_name_text.setAttribute("id", "form_name_text");
    form_name_text.setAttribute("type", "text");
    form_name_text.setAttribute("value", user_data[1]);

    let profile_submit = document.createElement("input");
    profile_submit.setAttribute("id", "profile_submit");
    profile_submit.setAttribute("type", "submit");
    profile_submit.value = "저장";
    profile_submit.setAttribute("onclick", "save_profile()");

    form_name_label.appendChild(form_name_text);
    profile_form.appendChild(form_name_label);
    profile_form.appendChild(profile_submit);

    block.appendChild(profile_form);
}

function save_profile() {
    let input_user_name = document.getElementById("user_name_text").value;

    fetch("/mypage/editprofile", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'user_name': input_user_name})
    })

    location.href = '/mypage';
}
