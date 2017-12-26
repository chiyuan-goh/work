var map2string = function(text) {
    var start = 0;
    var mapping = [];
    var wait_start = false;

    for (var i = 0; i < text.length; i++){
        var c = text.charAt(i);

        if (/\s/.test(c)){
            if (!wait_start) {
                mapping.push([start, i - 1]);
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

    mapping.push([start, text.length - 1]);
    return mapping;
}

var run_compare = function(text1, text2){
    var t1 = text1.trim();
    var t2 = text2.trim();

    var t1_array = t1.split(/\s/);
    var t2_array = t2.split(/\s/);

    var t1_mapping = map2string(t1);
    var t2_mapping = map2string(t2);
    opcodes = difflib.SequenceMatcher(t1_array, t2_array, false);

    for (var i = 0; i < opcodes.length; i++){
        opcodes[i][1] = t1_mapping[opcodes[i][1]][0];
        opcodes[i][2] = t1_mapping[opcodes[i][2]][1];
        opcodes[i][3] = t2_mapping[opcodes[i][3]][0];
        opcodes[i][4] = t2_mapping[opcodes[i][4]][1];
    }

    return opcodes;
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
                var text1 = td_tags[0].text();
                var text2 = td_tags[1].text();

                run_compare(text1, text2);
            }
            //console.log("key is pressed. preform compare");
            //$('#diffModal').modal();
        }

    });
});