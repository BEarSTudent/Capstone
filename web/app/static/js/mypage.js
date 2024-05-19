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
