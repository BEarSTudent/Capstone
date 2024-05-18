let lastNum = 0;
let isFetching = false;

async function load_more() {
    isFetching = true;
    const response_data = await fetch("/community/load", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'last': lastNum})
    })
    .then(res => res.json())
    
    show_boards(response_data.boards);
}

function show_boards(board_data) {
    let boards = document.getElementsByClassName("boards")[0];
    
    if (board_data.length + lastNum <= 3) {
        let top_button = document.getElementsByClassName("to_top")[0];
        let footer = top_button.parentElement;
        footer.removeChild(top_button);
    }
    
    if (board_data.length + lastNum == 0) {
        let empty_text = document.createElement("div");
        empty_text.setAttribute("class", "empty_text")
        empty_text.innerHTML = "아직 게시물이 없습니다.";
        boards.appendChild(empty_text);
        return
    }
    
    for(let i = 0; i < board_data.length; i++) {
        let board_block = document.createElement("div");
        board_block.setAttribute("class", "board_block");
        
        let board_image = document.createElement("img");
        board_image.setAttribute("class", "board_image");
        board_image.setAttribute("src", board_data[i][1]);
        
        let board_title = document.createElement("div");
        board_title.setAttribute("class", "board_title");
        board_title.innerHTML = board_data[i][2];
        
        board_block.appendChild(board_image);
        board_block.appendChild(board_title);
        
        boards.appendChild(board_block);
    }

    lastNum += board_data.length;
    isFetching = false;
}

window.addEventListener("scroll", function () {
    const IS_END = (window.innerHeight + window.scrollY > document.body.offsetHeight);
    
    if (IS_END && !isFetching) {
        load_more();
    }
});

function to_the_top(){
    const position = document.documentElement.scrollTop || document.body.scrollTop;
    if (position) {
        window.requestAnimationFrame(() => {
            window.scrollTo(0, position - position / 10);
            to_the_top();
        });
    }
}
