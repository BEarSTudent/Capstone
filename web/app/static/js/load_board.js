function load_boards() {
    if (board_data.length <= 0) {
        let empty_text = document.createElement("div");
        empty_text.setAttribute("class", "empty_text")
        empty_text.innerHTML = "아직 사진이 없습니다.";
        boards.appendChild(empty_text);
        return
    }

    let start_num = last_num;

    if (last_num + 9 <= board_data.length) {
        last_num += 9;
    } else {
        last_num = board_data.length;
    }

    for(i = start_num; i < last_num; i++) {
        let board_block = document.createElement("div");
        board_block.setAttribute("class", "board_block");
        board_block.setAttribute("id", board_data[i][0]);
        
        let board_image = document.createElement("img");
        board_image.setAttribute("class", "board_image");
        board_image.setAttribute("src", board_data[i][1]);
        
        board_block.appendChild(board_image);

        if(board_data[i][2] != undefined) {
            let board_title = document.createElement("div");
            board_title.setAttribute("class", "board_title");
            board_title.innerHTML = board_data[i][2];
            
            board_block.appendChild(board_title);
        }
        
        boards.appendChild(board_block);
    }
    isFetching = false;
}

window.addEventListener("scroll", function () {
    const IS_END = (window.innerHeight + window.scrollY > document.body.offsetHeight);
    
    if (IS_END && !isFetching) {
        load_boards();
    }
});
