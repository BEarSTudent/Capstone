function delete_top_button() {    
    if (board_data.length <= 3) {
        let top_button = document.getElementsByClassName("to_top")[0];
        let footer = top_button.parentElement;
        footer.removeChild(top_button);
    }
}

function to_the_top(){
    const position = document.documentElement.scrollTop || document.body.scrollTop;
    if (position) {
        window.requestAnimationFrame(() => {
            window.scrollTo(0, position - position / 10);
            to_the_top();
        });
    }
}
