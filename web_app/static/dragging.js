function setDraggingState(square_num){
    piece_name = ".square-" + square_num;
    piece = document.querySelector(piece_name);
    piece.classList.add("dragging");

    function onMouseUp(){
        moveCheck(square_num);
        document.removeEventListener("mousemove", onDrag);
        piece.classList.remove("dragging");
        document.removeEventListener("mouseup", onMouseUp);
    }

    document.addEventListener("mousemove", onDrag);
    document.addEventListener("mouseup", onMouseUp);
}


function onDrag({offsetX, offsetY}){

    drag_piece = document.querySelector(".dragging");

    let getStyle = window.getComputedStyle(drag_piece);
    let left = parseInt(getStyle.left);
    let top = parseInt(getStyle.top);
    let width = parseInt(getStyle.width);
    let height = parseInt(getStyle.height);

    drag_piece.style.left = `${left + offsetX - width/2}px`;
    drag_piece.style.top = `${top + offsetY - height/2}px`;
}


function setPiecePosition(piece, col, row){
    piece.style.left = `${(col-1)*12.5}%`;
    piece.style.top = `${(8-row)*12.5}%`;
}


function onCorrectAswer(col, row){
    analysis_field = document.querySelector(".message");
    next_button_html = `<form method="post">
                            <input type="submit" value="NEXT"/>
                            <input type="hidden" id="fen" name="fen" value="${fen}">
                        </form>`;
    
    analysis_field.innerHTML = '<h1 style="color: #7ea650;">Correct!</h1>\n' + next_button_html;


    piece_name = ".square-" + String(col) + String(row);
    captured_piece = document.querySelector(piece_name);
    if(captured_piece != null){
        captured_piece.style.display = "none";
    }
}


function moveCheck(initial_pos){
    moved_piece = document.querySelector(".dragging");
    board = document.querySelector(".board");

    // if(moved_piece != null){
        let pieceStyle = window.getComputedStyle(moved_piece);
        let boardStyle = window.getComputedStyle(board);
        
        let piece_x = parseInt(pieceStyle.left) + parseInt(pieceStyle.width) / 2;
        let piece_y = parseInt(pieceStyle.top) + parseInt(pieceStyle.height) / 2;
        let cell_size = parseInt(boardStyle.width) / 8;
        let col = parseInt(piece_x / cell_size) + 1; 
        let row = 8 - parseInt(piece_y / cell_size);
        let move = String(initial_pos) + String(col) + String(row);
        console.log('move is legal: ' + legal_moves.includes(move));

        if(move == answer){
            onCorrectAswer(col, row);
            setPiecePosition(moved_piece, col, row);
        }
        else{
            if(legal_moves.includes(move)){
                analysis_field = document.querySelector(".message");
                analysis_field.innerHTML = '<h1 style="color: #e43131;">WRONG. TRY AGAIN</h1>\n';
            }
            
            setPiecePosition(moved_piece, parseInt(initial_pos.toString()[0]), parseInt(initial_pos.toString()[1]));
            
        }
    // }
 
}