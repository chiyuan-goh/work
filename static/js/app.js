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
    //text1 text2 is html
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

//TODO: there is some bug here when highlighting breaks on paragraph :(
var drawModal = function(text1, text2, opcodes){
    var t1 = "<div class='col-md-6 modal-right'><p>";
    var t2 = "<div class='col-md-6'><p>";

    var changIdx = 1;

    for (var i = 0; i < opcodes.length; i++){
        var op = opcodes[i][0];
        var t1s = opcodes[i][1];
        var t1e = opcodes[i][2];
        var t2s = opcodes[i][3];
        var t2e = opcodes[i][4];

        if (op == 'replace'){
            t1 += "<font class='compare-rep'>" + text1.substring(t1s, t1e) + "<sup>" + changIdx + "</sup></font>" + " ";
            t2 += "<font class='compare-rep'>" + text2.substring(t2s, t2e) + "<sup>" + changIdx + "</sup></font>" + " ";
            changIdx++;
        }
        else if (op == 'delete'){
            t1 += "<font class='compare-del'>" + text1.substring(t1s, t1e) + "</font> ";
        }
        else if (op == 'insert'){
            t2 += "<font class='compare-add'>" + text2.substring(t2s, t2e) + "</font> ";
        }
        else if (op == 'equal'){
            t1 += text1.substring(t1s, t1e) + " ";
            t2 += text2.substring(t2s, t2e) + " ";
        }
    }

    t1 += "</p></div>";
    t2 += "</p></div>";
    t1 = t1.replace('\n', "</p><p>");
    t2 = t2.replace('\n', "</p><p>");


    // for (var i = 0; i < t1.length; i++){
    //     if (t1.charAt(i) == '\n')
    //         t1 = t1.substring(0, i) + "</p><p>" + t1.substring(i + 1);
    // }
    //
    //     for (var i = 0; i < t2.length; i++){
    //     if (t2.charAt(i) == '\n')
    //         t2 = t2.substring(0, i) + "</p><p>" + t2.substring(i + 1);
    // }

    $(".modal-body").html(t1 + "<hr>" + t2);
}

$(document).ready(function(){
    var selected_cls = 'bg-info';

    $("td").click(function(){
        $(this).toggleClass(selected_cls);
    });

    $("#match").click(function(){
        $("sup").toggleClass("hide");
    });

    $("html").keypress(function(event){
        if (event.charCode == 99){
            var td_tags = $("." + selected_cls);

            if(td_tags.length != 2){
                alert("You must select exactly 2 clause content to compare!");
            }
            else {
                //step 1: run this through
                var text1 = $(td_tags[0]).html();
                var text2 = $(td_tags[1]).html();

                text1 = text1.substring(3, text1.length-4);
                text2 = text2.substring(3, text2.length-4);
                text1 = text1.replace("</p><p>", "\n");
                text2 = text2.replace("</p><p>", "\n");

                var opcodes = run_compare(text1, text2);
                drawModal(text1.trim(), text2.trim(), opcodes);
                $('#diffModal').modal();
            }
            //console.log("key is pressed. preform compare");

        }

    });
});