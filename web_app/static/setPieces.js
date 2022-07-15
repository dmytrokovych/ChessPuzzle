function set_piece(piece_name, position){
    let left = parseInt(position[0]);
    let top = parseInt(position[1]);
    html = `<div class="piece ${piece_name} square-${left}${top}" onmousedown="setDraggingState(${left}${top})" style="left: ${(left-1)*12.5}%; top: ${(8-top)*12.5}%"></div>`;

    return html;
}

position_html = "";

for(piece of pieces){
    position_html += set_piece(piece[0], piece[1]) + "\n";
}

function render_html(){
    board = document.querySelector(".board");
    board.innerHTML = position_html;
}

window.onload = render_html;