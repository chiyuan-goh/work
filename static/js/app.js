var map2string = function(text) {
    var start = 0;
    var mapping = [];
    var wait_start = false;

    for (var i = 0; i < text.length; i++){
        var c = text.charAt(i);

        if (/\s/.test(c)){
            if (!wait_start) {
                mapping.push([start, i]);
                wait_start = true;
            }
        }
        else {
            if (wait_start){
                wait_start = false;
                start = i;
            }
        }
    }

    mapping.push([start, text.length]);
    return mapping;
}

var run_compare = function(text1, text2){
    var t1 = text1.trim();
    var t2 = text2.trim();

    var t1_array = text1.match(/[^\s]+/g);//t1.split(/\s/);
    var t2_array = text2.match(/[^\s]+/g);//t2.split(/\s/);

    var t1_mapping = map2string(t1);
    var t2_mapping = map2string(t2);
    opcodes = new difflib.SequenceMatcher(t1_array, t2_array, false).get_opcodes();

    console.log("t1 mapping:" + t1_mapping.length);
    console.log("t2 mapping:" + t2_mapping.length);
    console.log("length of opcodes: " + opcodes.length);

    for (var i = 0; i < opcodes.length; i++){
        console.log("i:" + i);
        console.log(opcodes[i]);
        opcodes[i][1] = t1_mapping[opcodes[i][1]][0];
        opcodes[i][2] = t1_mapping[opcodes[i][2]-1][1];
        opcodes[i][3] = t2_mapping[opcodes[i][3]][0];
        opcodes[i][4] = t2_mapping[opcodes[i][4]-1][1];
    }

    return opcodes;
}

var drawModal = function(text1, text2, opcodes){
    var t1 = "<div>";
    var t2 = "<div>";

    for (var i = 0; i < opcodes.length; i++){
        var op = opcodes[i][0];
        var t1s = opcodes[i][1];
        var t1e = opcodes[i][2];
        var t2s = opcodes[i][3];
        var t2e = opcodes[i][4];

        if (op == 'replace'){
            t1 += "<span class='compare-rep'>" + text1.substring(t1s, t1e) + "</span>" + " ";
            t2 += "<span class='compare-rep'>" + text2.substring(t2s, t2e) + "</span>" + " ";
        }
        else if (op == 'delete'){
            t1 += "<span class='compare-del'>" + text1.substring(t1s, t1e) + "</span>" + " ";
            t2 += text2.substring(t2s, t2e) + " ";
        }
        else if (op == 'insert'){
            t1 += text1.substring(t1s, t1e) + " ";
            t2 += "<span class='compare-add'>" + text2.substring(t2s, t2e) + "</span>" + " ";
            console.log("im here");
        }
        else if (op == 'equal'){
            t1 += text1.substring(t1s, t1e) + " ";
            t2 += text2.substring(t2s, t2e) + " ";
        }
    }

    t1 += "</div>";
    t2 += "</div>";

    $(".modal-body").html("<p>" + t1 + "</p>" + "<hr>" + "<p>" + t2 + "</p>");
}

$(document).ready(function(){
    var selected_cls = 'bg-info';

    $("td").click(function(){
        $(this).toggleClass(selected_cls);
    });

    $("html").keypress(function(event){
        if (event.charCode == 99){
            var td_tags = $("." + selected_cls);

            if(td_tags.length != 2){
                alert("You must select exactly 2 clause content to compare!");
            }
            else {
                //step 1: run this through
                var text1 = $(td_tags[0]).text();
                var text2 = $(td_tags[1]).text();

                var opcodes = run_compare(text1, text2);
                drawModal(text1.trim(), text2.trim(), opcodes);
            }
            //console.log("key is pressed. preform compare");
            $('#diffModal').modal();
        }

    });
});