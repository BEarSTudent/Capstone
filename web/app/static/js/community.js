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
    const IS_END = (window.innerHeight + window.scrollY >= document.body.offsetHeight);
    
    if (IS_END && !isFetching) {
        load_more();
    }
});
