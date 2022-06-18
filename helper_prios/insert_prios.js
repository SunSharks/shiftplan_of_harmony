let prio_ids = [];


function add_prio_id(id){
  prio_ids.push(id);
}

function placeholder_to_value() {
  // console.log(prio_ids);
  let wl = document.getElementById('workload');
  if (wl.value.length === 0) {
    wl.value = wl.placeholder;
  }
  let br = document.getElementById('breakinp');
  if (br.value.length === 0) {
    br.value = br.placeholder;
  }
  let elem;
  for (let i = 0; i < prio_ids.length; i++){
    elem = document.getElementById('prioinp'+prio_ids[i].toString());
    if (elem.value.length === 0) {
        elem.value = elem.placeholder;
    }
  }
    return true;
}


let multiple_selected = new Set();

function select_entry(id){
  multiple_selected.add(id);
  selbtn = document.getElementById("selbtn"+id.toString());
  selbtn.style.display = "none";
  unselbtn = document.getElementById("unselbtn"+id.toString());
  unselbtn.style.display = "inline";
  console.log("select");
  console.log(multiple_selected);
}

function unselect_entry(id){
  multiple_selected.delete(id);
  let selbtn = document.getElementById("selbtn"+id.toString());
  selbtn.style.display = "inline";
  let unselbtn = document.getElementById("unselbtn"+id.toString());
  unselbtn.style.display = "none";
  console.log("unselect");
  console.log(multiple_selected);
}

function on_input(trig_id){
  let trig_val = document.getElementById('prioinp'+trig_id.toString()).value;
  let ms_ar = Array.from(multiple_selected);
  for (let i=0; i<ms_ar.length; i++){
    document.getElementById('prioinp'+ms_ar[i].toString()).value = trig_val;
    // unselect_entry(ms_ar[i])
  }
}

function unselect_all(){
  let ms_ar = Array.from(multiple_selected);
  for (let i=0; i<ms_ar.length; i++){
    unselect_entry(ms_ar[i])
  }
}
